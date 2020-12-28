import re
import uuid
import subprocess
from ..constants import BRANCHES_PREFIXES
from ..changelog import Changelog


def ensure_git_initialized():
    try:
        subprocess.check_call(['git', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        raise Exception("Not in a git repository.")


def ensure_working_tree_clean():
    result = subprocess.Popen(['git', 'status', '--porcelain'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stdout.read() != b"":
        raise Exception("Working directory is not clean, please commit or stash changes and retry.")


def get_current_branch():
    result = subprocess.Popen(['git', 'branch', '--show-current'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.read().decode('utf-8').strip()


def ensure_branch_mergeable():
    try:
        current_branch = get_current_branch()
        branch_prefix, branch_description = current_branch.split('/')
    except ValueError:
        raise Exception("Can't perform magic merge on branch %s"%current_branch)
    
    if branch_prefix not in BRANCHES_PREFIXES:
        raise Exception("Can't perform magic merge on branch of type %s"%branch_prefix)


def get_current_branch_commits():
    LOG_COMMIT_PATTERN = re.compile("(?:^|\n)commit\s+(?P<commit_sha>\w+).+\nAuthor:\s+(?P<author>.+)\nDate:\s+(?P<date>.+)\n\n\s+(?P<message>.+)")
    result = subprocess.Popen(['git', 'log', 'main..HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return [m.groupdict() for m in LOG_COMMIT_PATTERN.finditer(result.stdout.read().decode('utf-8'))]

def merge_squash(merged_branch, message=None):
    if message is None:
        message = "Merge branch %s"%merged_branch

    print([merged_branch])
    
    subprocess.call(['git', 'checkout', 'main'])
    subprocess.call(['git', 'pull', '--rebase', 'origin', 'main'])
    subprocess.call(['git', 'merge', '--squash', merged_branch])
    input('Check that everything was ok, then press [enter] to commit and delete WIP branch.')

    subprocess.call(['git', 'commit', '-m', message])
    subprocess.call(['git', 'push', '-u', 'origin', 'main'])
    subprocess.call(['git', 'branch', '-D', merged_branch])
    subprocess.call(['git', 'push', '--delete', 'origin', merged_branch])

def done_command():
    ensure_git_initialized()
    ensure_working_tree_clean()
    ensure_branch_mergeable()
    
    current_branch = get_current_branch()
    branch_type, branch_description = current_branch.split('/')
    branch_description = branch_description.strip().replace('_', ' ')
    commits = get_current_branch_commits()

    # parse changelog and add branch changes to [unreleased] appropriate section
    changelog = Changelog.parse('docs/changelog.md')
    changelog.add_change(branch_type, branch_description, [commit['message'] for commit in commits])
    changelog.save('docs/changelog.md')

    # open changelog for editing
    subprocess.call(['code', 'docs/changelog.md'])
    input("Edit changelog if required. Then press [enter] to continue...")

    # parse file to ensure syntax is valid
    changelog = Changelog.parse('docs/changelog.md')
    changelog.save('docs/changelog.md')

    subprocess.call(['git', 'add', '.'])
    subprocess.call(['git', 'commit', '-m', 'update changelog'])

    squash_description = branch_description + "\n" + "\n".join(["- %s"%commit['message'] for commit in commits])
    merge_squash(current_branch, message=squash_description)
