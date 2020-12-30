import argparse
import subprocess
from ..command import Command
from ..constants import BRANCHES_PREFIXES


class WipCommand(metaclass=Command):
    def parser():
        parser = argparse.ArgumentParser("git wip")
        parser.add_argument("branch_type", type=str, choices=BRANCHES_PREFIXES.keys(), help="Category of the changes done on this branch")
        parser.add_argument("description", nargs='?', type=str, help="Description of the work done on this branch")
        return parser

    def run(*, branch_type, description):
        """
        Create a typed branch to work on a feature/bugfix/...
        """        
        branch_description = description or input('branch description: ')
        branch_name = branch_type + "/" + branch_description.replace(' ', '_').lower()
        
        subprocess.call(['git', 'checkout', 'main'])
        subprocess.call(['git', 'pull', '--rebase', 'origin', 'main'])
        subprocess.call(['git', 'checkout', '-b', branch_name])
        subprocess.call(['git', 'push', '-u', 'origin', branch_name])
