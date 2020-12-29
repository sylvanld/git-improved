import re
import argparse
import subprocess
from ..changelog import Changelog
from ..constants import CATEGORIES_ICONS


def version(text):
    try:
        version_pattern = re.compile('^\d+\.\d+\.\d+$')
        if version_pattern.match(text):
            return text
    except Exception:
        pass
    raise ValueError("Not a valid version: %s"%text)


def parse_args():
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--version', type=version, help='Publish a release with given VERSION')
    group.add_argument('--patch', action='store_true', help='Publish a release of type "patch" (auto-increment current version)')
    group.add_argument('--minor', action='store_true', help='Publish a release of type "minor" (auto-increment current version)')
    group.add_argument('--major', action='store_true', help='Publish a release of type "major" (auto-increment current version)')

    args = parser.parse_args()
    if not args.patch and not args.minor and not args.major and not args.version:
        parser.print_help()
        exit(0)
    return args


def increment_version(version=None, patch=False, minor=False, major=False):
    incremented_part = 'patch'*patch + 'minor'*minor + 'major'*major

    # an incremented part is always required, even if a version is specified
    if not incremented_part:
        incremented_part = 'patch'
    
    bump_command = ['bump2version']
    if version:
        bump_command.extend(['--new-version', version])
    bump_command.append(incremented_part)

    try:
        subprocess.check_call(bump_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print('Cant increment version, working tree has uncommited changes.')
        exit(1)

    # parse new version from setup.cfg
    with open('setup.cfg') as setup_file:
        rows = setup_file.read().split('\n')
    
    for row in rows:
        if row.startswith('current_version'):
            return row.split('=')[1].strip()
    
    # fail if no version is found
    raise Exception("Version not found in setup.cfg")


def get_current_branch():
    result = subprocess.Popen(['git', 'branch', '--show-current'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.read().decode('utf-8').strip()


def assert_branch_is_main():
    current_branch = get_current_branch()
    if current_branch != 'main':
        raise Exception('Releases can only be deployed from branch "main". Current branch: %s' % current_branch)


def commit_version_files(version):
    subprocess.call(['git', 'add', '.'])
    subprocess.call(['git', 'commit', '-m', '%s Release version %s'%(CATEGORIES_ICONS['Release'], version)])
    subprocess.call(['git', 'tag', version, '-m' 'Release version %s'%version])
    subprocess.call(['git', 'push', '-u', 'origin', 'main', '--follow-tags'])


def release_command():
    args = parse_args()

    assert_branch_is_main()
    new_version = increment_version(version=args.version, patch=args.patch, minor=args.minor, major=args.major)
    
    changelog = Changelog.parse('docs/changelog.md')
    release = changelog.get_unreleased()
    changelog.create_release(new_version, release_file="docs/releases/%s.md"%new_version)
    changelog.save('docs/changelog.md')

    commit_version_files(new_version)
