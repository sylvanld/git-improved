import os
import subprocess


def format_table(items):
    terminal_height, terminal_width = [int(x) for x in os.popen('stty size', 'r').read().split()]

    items = sorted(items)
    max_width = max(len(item) for item in items) + 4

    table_width = terminal_width // max_width
    table_height = len(items) // table_width + 1    
    
    string = ""
    for i in range(table_height):
        for j in range(table_width):
            index = j*table_height+i
            if index < len(items):
                item = items[index]
                string += item.ljust(max_width)
        string += "\n"
    return string


def display_table(items):
    print(format_table(items))


def silent_call(*args):
    subprocess.call(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def check_output(*args, rows=False):
    result = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.read().decode('utf-8')
    if rows:
        return [row.strip() for row in output.strip().split('\n')]
    else:
        return output.strip()
