import os
import shutil
import argparse
import subprocess
from ..templates import TEMPLATES
from ..command import Command
from ..changelog import Changelog
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
        setup_project(template=template, destination=directory)
