import re
import subprocess
from .shell import check_output, silent_call
from .constants import BRANCHES_PREFIXES

LOG_COMMIT_PATTERN = re.compile("(?:^|\n)commit\s+(?P<commit_sha>\w+).+\nAuthor:\s+(?P<author>.+)\nDate:\s+(?P<date>.+)\n\n\s+(?P<message>.+)")


def ensure_git_initialized():
    try:
        subprocess.check_call(['git', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        raise Exception("Not in a git repository.")


def ensure_working_tree_clean():
    result = subprocess.Popen(['git', 'status', '--porcelain'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stdout.read() != b"":
        raise Exception("Working directory is not clean, please commit or stash changes and retry.")


def ensure_main_branch():
    current_branch = get_current_branch()
    if current_branch != 'main':
        raise Exception('Releases can only be deployed from branch "main". Current branch: %s' % current_branch)


def ensure_branch_mergeable():
    try:
        current_branch = get_current_branch()
        branch_prefix, branch_description = current_branch.split('/')
    except ValueError:
        raise Exception("Can't perform magic merge on branch %s"%current_branch)
    
    if branch_prefix not in BRANCHES_PREFIXES:
        raise Exception("Can't perform magic merge on branch of type %s"%branch_prefix)


def count_changes_from_remote():
    current_branch = get_current_branch()
    changes_count = int(check_output("git", "rev-list", "{0}..origin/{0}".format(current_branch), "--count"))
    return changes_count


def get_current_branch():
    result = subprocess.Popen(['git', 'branch', '--show-current'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.read().decode('utf-8').strip()


def get_current_branch_commits():
    result = subprocess.Popen(['git', 'log', 'main..HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return [m.groupdict() for m in LOG_COMMIT_PATTERN.finditer(result.stdout.read().decode('utf-8'))]


def get_remote_origin():
    return check_output('git', 'remote', 'get-url', 'origin')

def get_local_branches():
    return [branch.split()[-1] for branch in check_output("git", "branch", rows=True)]


def get_remote_branches():
    silent_call("git", "fetch")
    return [branch[7:] for branch in check_output("git", "branch", "--remote", rows=True)]


def get_releases():
    silent_call("git", "fetch")
    return check_output("git", "tag", rows=True)


def delete_branch(branch_name, local=True, remote=True):
    if local:
        subprocess.call(['git', 'branch', '-D', branch_name])
    if remote:
        subprocess.call(['git', 'push', '--delete', 'origin', branch_name])


def merge_squash(merged_branch, message=None):
    if message is None:
        message = "Merge branch %s"%merged_branch
    
    subprocess.call(['git', 'checkout', 'main'])
    subprocess.call(['git', 'pull', '--rebase', 'origin', 'main'])
    subprocess.call(['git', 'merge', '--squash', merged_branch])
    input('Check that everything was ok, then press [enter] to commit and delete WIP branch.')

    subprocess.call(['git', 'commit', '-m', message])
    subprocess.call(['git', 'push', '-u', 'origin', 'main'])
    subprocess.call(['git', 'branch', '-D', merged_branch])
    subprocess.call(['git', 'push', '--delete', 'origin', merged_branch])
