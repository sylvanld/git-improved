import argparse
import subprocess
from ..constants import BRANCHES_PREFIXES

def parse_args():
    parser = argparse.ArgumentParser("git wip")
    parser.add_argument("branch_type", type=str, choices=BRANCHES_PREFIXES.keys(), help="Category of the changes done on this branch")
    parser.add_argument("description", nargs='?', type=str, help="Description of the work done on this branch")
    return parser.parse_args()

def create_wip_branch_command():
    args = parse_args()
    if not args.description:
        branch_description = input('branch description: ')
    branch_name = args.branch_type + "/" + branch_description.replace(' ', '_').lower()
    
    subprocess.call(['git', 'checkout', 'main'])
    subprocess.call(['git', 'pull', '--rebase', 'origin', 'main'])
    subprocess.call(['git', 'checkout', '-b', branch_name])
    subprocess.call(['git', 'push', '-u', 'origin', branch_name])
