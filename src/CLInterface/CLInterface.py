#!python2

import curses
from threading import Thread


class CLInterface:
    def __init__(self):
        self.stdscr = curses.initscr()
        # curses.keypad(stdscr, True)
        curses.curs_set(False)
        curses.timeout(-1)
        curses.cbreak()
        curses.start_color()
        curses.noecho()
        self.max_y, self.max_x = curses.getmaxyx(stdscr)

        self.running = True
        self.data = []
        self.keyPressed = 0

        self.window = curses.newwin(self.max_y, self.max_x, 0, 0)
        curses.box(self.window)

    def start(self):
        # start the thread
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        while Running:
            # wrefresh(window)
            curses.wclear(self.window)
            curses.waddstr(self.window, 'Test.')

            self.keyPressed = curses.wgetch(self.window)
            if self.keyPressed == 27:
                curses.waddstr(self.window, '\nESC interrupt.\n', uCu.A_BOLD)
                curses.wgetch(self.window)
                self.running = False
        curses.endwin()

    def write(self, dataIn):
        self.data = dataIn

    def stop(self):
        return
