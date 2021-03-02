import os
import shutil
import argparse
import subprocess
from ...command import Command
from ...changelog import Changelog
from ..template import setup_project


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


def path(string):
    return os.path.abspath(os.path.expanduser(string))


def template(string):
    from ..template import TemplateManifest
    from ..shell import format_table
    manifest = TemplateManifest(os.path.expanduser("~/.git-templates"))
    if string not in manifest.templates:
        print("Template '%s' not found...\nPlease choose one of the following, or install a new template:\n\n%s"%(string, format_table(manifest.templates)))
        exit(0)
    return string


class SetupCommand(metaclass=Command):
    def parser():
        parser = argparse.ArgumentParser('git setup')

        parser.add_argument('directory', type=path, default=".")
        parser.add_argument('--template', type=template, help='Template used to initiate project structure')
        parser.add_argument('-v', '--verbose', action='store_true', help='Display information about created files')

        return parser

    def run(*, directory=".", template=None, verbose=False):
        
        releases_directory='docs/releases'
        changelog_path='docs/changelog.md'
        no_github_action=False

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


        if not is_git_initialized():
            subprocess.call(['git', 'init'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.call(['git', 'branch -m master main'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print('Git repository initialized...')
        
        commit_configuration()

        # setup templates
        if template is not None:
            setup_project(template=template, destination=directory)
