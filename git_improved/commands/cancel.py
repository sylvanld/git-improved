import argparse
import subprocess

def silent_call(*args):
    subprocess.call(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def check_output(*args, rows=False):
    result = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.read().decode('utf-8')
    if rows:
        return [row.strip() for row in output.strip().split('\n')]
    else:
        return output.strip()

def get_local_branches():
    return [branch.split()[-1] for branch in check_output("git", "branch", rows=True)]

def get_remote_branches():
    silent_call("git", "fetch")
    return [branch[7:] for branch in check_output("git", "branch", "--remote", rows=True)]

def get_current_branch():
    result = subprocess.Popen(['git', 'branch', '--show-current'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.read().decode('utf-8').strip()

def parse_args():
    parser = argparse.ArgumentParser("git cancel")
    parser.add_argument("-i", "--interactive", action='store_true', help="Prompt names of multiple branches to delete")
    return parser.parse_args()

def select_branches():
    print('EXISTING BRANCHES')
    branches = set(get_local_branches() + get_remote_branches())
    try:
        branches.remove("main")
    except KeyError:
        pass
    branches = list(branches)

    for i in range(len(branches)):
        print('[%s] %s'%(i, branches[i]))
    
    unwanted_indexes = input("\nBranches to delete? (coma separated): ")
    unwanted_indexes = [int(i) for i in unwanted_indexes.replace(' ', '').strip().strip(',').split(',')]
    return [branches[i] for i in unwanted_indexes]

def delete_branch(branch_name, remote=True):
    subprocess.call(['git', 'branch', '-D', branch_name])
    subprocess.call(['git', 'push', '--delete', 'origin', branch_name])

def cancel_command():
    """
    Delete current branch from local and remote
    """

    args = parse_args()
    current_branch = get_current_branch()

    if args.interactive:
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
