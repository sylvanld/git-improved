import argparse
import subprocess

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("description", nargs="?", help="Commit message")
    return parser.parse_args()


def save_command():
    args = parse_args()

    description = args.description or input("description: ")
    subprocess.call(['git', 'add', '.'])
    subprocess.call(['git', 'commit', '-m', description])
    