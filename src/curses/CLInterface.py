#!python2

from curses import *


class CLInterface:
    def __init__(self):
        self.stdscr = initscr()
        keypad(stdscr, True)
        curs_set(False)
        timeout(-1)
        cbreak()
        start_color()
        noecho()
        self.max_y, self.max_x = getmaxyx(stdscr)

        self.window = newwin(self.max_y, self.max_x, 0, 0)
        box(self.window)

    def update():
        # wrefresh(window)
        wclear(window)
        waddstr(window, 'Test.')
