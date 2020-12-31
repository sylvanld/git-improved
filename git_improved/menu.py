import os


KEY_SPACE = "KEY_SPACE"
KEY_UP = "KEY_UP"
KEY_DOWN = "KEY_DOWN"
KEY_ENTER = "KEY_ENTER"


def _getkeycode():
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return ord(ch)

def _getkey():
    code = _getkeycode()
    if code == 13:
        return KEY_ENTER
    elif code == 32:
        return KEY_SPACE
    elif code == 27:
        print(_getkeycode())
        if True:
            arrow_code = _getkeycode()
            if arrow_code == 65:
                return KEY_UP
            elif arrow_code == 66:
                return KEY_DOWN
    return None


class Menu:
    def __init__(self, *, choices):
        if not choices or len(choices) == 0:
            raise ValueError("You must provide a non empty list of choices (strings) to Menu")

        self.choices = choices
        self.length = len(choices)
        self.selected = dict((i, False) for i in range(self.length))
        self.cursor = 0

    def clear(self):
        os.system('clear')

    def draw(self, message, multiple=True):
        self.clear()
        print(message)
        for i in range(len(self.choices)):
            
            if multiple:
                cursored_pattern = "[%s]" if self.cursor == i else " %s "
                selected_symbol = "*" if self.selected[i] else " "
                prefix = cursored_pattern % selected_symbol
            else:
                prefix = ">" if self.cursor == i else " "
            
            print(prefix, self.choices[i])

    def prompt(self, message, *, multiple=True):
        char = None
        while char != KEY_ENTER:
            self.draw(message, multiple=multiple)
            char = _getkey()

            if char == KEY_UP:
                self.cursor = (self.cursor - 1) % self.length
            elif char == KEY_DOWN:
                self.cursor = (self.cursor + 1) % self.length
            elif char == KEY_SPACE and multiple:
                self.selected[self.cursor] = not self.selected[self.cursor]
        
        if multiple:
            return [self.choices[i] for i in range(self.length) if self.selected[i]]
        else:
            return self.choices[self.cursor]


if __name__ == '__main__':
    menu_delete_branch = Menu(choices=["feature/useless_feature", "doc/explain_nothing", "improve/nothing_but_stupidity"])
    selection = menu_delete_branch.prompt("Select branch(es) to delete", multiple=True)
    print(selection)
