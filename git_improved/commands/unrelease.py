import re
import argparse
import subprocess
from ..changelog import Changelog

def parse_args():
    parser = argparse.ArgumentParser('git unrelease')
    parser.add_argument('version', nargs='?', help='coma separated list of versions to delete')
    parser.add_argument('-i', '--interactive', action='store_true', help="Interactively prompt list of releases to delete.")


    args =  parser.parse_args()

    # XOR
    if (args.interactive == False) == (args.version is None):
        parser.print_help()
        print('\nEither version, or interactive mode is required. Not both...')
        exit(0)

    return args


def delete_release(version):
    subprocess.call(['git', 'tag', '-d', version])
    subprocess.call(['git', 'push', '--delete', 'origin', version])

    changelog = Changelog.parse('docs/changelog.md')
    changelog.delete_release(version)
    changelog.save('docs/changelog.md')


def unrelease_command():
    args = parse_args()
    
    if args.interactive:
        raise NotImplementedError("Interactive mode is not implemented for this feature.")
    else:
        delete_release(args.version)
