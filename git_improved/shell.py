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
