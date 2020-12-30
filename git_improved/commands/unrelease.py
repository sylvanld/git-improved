import re
import argparse
import subprocess
from ..command import Command
from ..changelog import Changelog
from ..exceptions import ValidationError


def delete_release(version):
    subprocess.call(['git', 'tag', '-d', version])
    subprocess.call(['git', 'push', '--delete', 'origin', version])

    changelog = Changelog.parse('docs/changelog.md')
    changelog.delete_release(version)
    changelog.save('docs/changelog.md')


class UnreleaseCommand(metaclass=Command):
    def parser():
        parser = argparse.ArgumentParser('git unrelease')
        parser.add_argument('version', nargs='?', help='coma separated list of versions to delete')
        parser.add_argument('-i', '--interactive', action='store_true', help="Interactively prompt list of releases to delete.")

        return parser

    def validate(args):
        if (args.interactive == False) == (args.version is None):
            raise ValidationError('Either version, or interactive mode is required. Not both...')

    def run(interactive=False, version=None):
        args = parse_args()
        
        if interactive:
            raise NotImplementedError("Interactive mode is not implemented for this feature.")
        else:
            delete_release(version)
