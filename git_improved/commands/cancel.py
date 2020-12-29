import subprocess

def get_current_branch():
    result = subprocess.Popen(['git', 'branch', '--show-current'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.read().decode('utf-8').strip()

def cancel_command():
    """
    Delete current branch from local and remote
    """
    unwanted_branch = get_current_branch()
    
    subprocess.call(['git', 'checkout', 'main'])
    subprocess.call(['git', 'branch', '-D', unwanted_branch])
    subprocess.call(['git', 'push', '--delete', 'origin', unwanted_branch])
