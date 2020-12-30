import os
import shutil
import argparse
import subprocess
from ..command import Command
from ..changelog import Changelog
from ..configurations import ACTION_PUBLISH_RELEASE_ON_TAG, BUMPVERSION_CONFIG


def is_git_initialized():
    try:
        subprocess.check_call(['git', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False


def commit_configuration():
    try:
        subprocess.call(['git', 'add', 'docs/', '.github/', 'setup.cfg'])
        subprocess.check_call(['git', 'commit', '-m', 'Initialize devops configuration files'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print('Devops configuration files added to git')
    except subprocess.CalledProcessError:
        pass


class SetupCommand(metaclass=Command):
    def parser():
        parser = argparse.ArgumentParser('git setup')

        parser.add_argument('--changelog-path', type=str, default='docs/changelog.md', help='Path to changelog.md')
        parser.add_argument('--releases-directory', type=str, default='docs/releases', help='Directory where releases individuals changelogs are stored')
        parser.add_argument('--no-github-action', action='store_true', help='Create github action to automagically document releases on github')

        return parser

    def run(*, changelog_path='docs/changelog.md', releases_directory='docs/releases', no_github_action=False):
        # create releases_directory and add a .gitkeep to ensure it wont be empty
        release_gitkeep_path = os.path.join(releases_directory, '.gitkeep')
        try:
            open(release_gitkeep_path)
            print('[Warning] GitHub action already exists. Make sure it contains configuration to document changes on release.')
        except FileNotFoundError:
            os.makedirs(releases_directory, exist_ok=True)
            with open(release_gitkeep_path, 'w') as gitkeep:
                pass
            print('Releases directory created in:', releases_directory)
        
        # create changelog if it doesn't exists
        try:
            changelog = Changelog.parse(changelog_path)
        except FileNotFoundError:
            directory = os.path.dirname(os.path.abspath(changelog_path))
            os.makedirs(directory, exist_ok=True)
            changelog = Changelog.parse(changelog_path)

        if not no_github_action:
            os.makedirs('.github/workflows', exist_ok=True)
            try:
                open('.github/workflows/release-tag.yml')
            except FileNotFoundError:
                with open('.github/workflows/release-tag.yml', 'w') as action_file:
                    action_file.write(ACTION_PUBLISH_RELEASE_ON_TAG)
                print('Github action created in: github/workflows/release-tag.yml')

        try:
            open('setup.cfg')
            print('[Warning] setup.cfg already exists, make sure that bumpversion section exists and neither commit nor tag options are enabled...')
        except FileNotFoundError:
            with open('setup.cfg', 'w') as setup:
                setup.write(BUMPVERSION_CONFIG)
            print('Created versioning configuration in: setup.cfg')

        if not is_git_initialized():
            subprocess.call(['git', 'init'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print('Git repository initialized...')
        
        commit_configuration()
