import argparse
import subprocess
from ..menu import Menu
from ..command import Command
from ..git import get_local_branches, get_remote_branches, get_current_branch, delete_branch


def select_branches():
    branches = set(get_local_branches() + get_remote_branches())
    try:
        branches.remove("main")
    except KeyError:
        pass

    select_branches_menu = Menu(choices=list(branches))
    return select_branches_menu.prompt("Select branches to delete")


class CancelCommand(metaclass=Command):
    def parser():
        parser = argparse.ArgumentParser("git cancel")
        parser.add_argument("-i", "--interactive", action='store_true', help="Prompt names of multiple branches to delete")
        return parser

    def run(interactive=False):
        """
        Delete current branch from local and remote
        """
        current_branch = get_current_branch()

        if interactive:
            branches_to_delete = select_branches()
        else:
            if current_branch == 'main':
                raise Exception("Can't delete branch main...")
            input("Branch '%s' will be deleted. Press [enter] to continue..."%current_branch)
            branches_to_delete = [current_branch]
        
        for unwanted_branch in branches_to_delete:
            if unwanted_branch == current_branch:
                # switch to main branch as you can't cancel a checked out branch
                subprocess.call(['git', 'checkout', 'main'])
            
            delete_branch(unwanted_branch)
