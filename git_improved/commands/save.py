import argparse
import subprocess
from ..command import Command


class SaveCommand(metaclass=Command):
    def parser():
        parser = argparse.ArgumentParser()
        parser.add_argument("description", nargs="?", help="Commit message")
        return parser

    def run(*, description=None):
        if not description:
            description = input("description: ")
        
        subprocess.call(['git', 'add', '.'])
        subprocess.call(['git', 'commit', '-m', description])
    