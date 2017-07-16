import sys, tty, termios
from formatter import *

class Table:
    def __init__(self, name):
        self.name = name
        self.columns = []

class Column:
    def __init__(self, heading, formatter=NumberFormatter(), values=[]):
        self.heading = heading
        self.values = values
        self.formatted_values = formatter.format_all(heading, values)
        print(self.formatted_values)
        self.width = 0 
        self.layout()

    def layout(self):
        self.width = max(
            len(self.heading),
            *map(len, self.formatted_values)
        )

    def render(self, x=0, y=0):
        print("\033[%d;%dH" % (y,x), end="")
        print("\033[4m", end="") # underline on
        print("%-*s" % (self.width, self.heading), end="")
        print("\033[24m", end="") # underline off

        for i, value in enumerate(self.formatted_values):
            print("\033[%d;%dH" % (y+i+1,x), end="")
            print("%*s" % (self.width, value), end="")

class Screen:
    def __init__(self):
        self.table = Table(name="Hello World")
        self.table.columns = [
            Column("Item Description", TextFormatter(), ["Apple", "Bear", "Cat"]),
            Column("Price", 
                NumberFormatter(prefix='$ ', comma=',', precision=2, 
                    negation=Accounting, decimal_align=True), 
                [1.00, -2.24, 3000.1714]
            )
        ]

    def render(self):
        print("\033[2J", end="") # erase all
        sys.stdout.flush()

        if not self.table:
            pass

        print("\033[1;1H", end="") # goto (1,1)
        print("\033[7m", end="") # inverse
        print(self.table.name, end="")
        print("\033[0m", end="") # normal
        sys.stdout.flush()

        # print columns
        dc = 1
        for column in self.table.columns:
            column.render(x=dc, y=3)
            dc += column.width + 1

        sys.stdout.flush()

if __name__ == "__main__":
    print("\033[?1049h", end="") # enter alternate screen buffer
    sys.stdout.flush()

    fd = sys.stdin.fileno()
    settings = termios.tcgetattr(fd)
    scr = Screen()

    try:
        tty.setraw(sys.stdin.fileno())
        while 1:
            scr.render()
            ch = sys.stdin.read(1)
            if ch == 'q':
                break
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, settings)
        print("\033[?1049l", end="") # leave alternate screen buffer

