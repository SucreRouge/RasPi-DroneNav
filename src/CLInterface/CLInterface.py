#!python2
# -*- coding: UTF-8 -*-

from unicurses import *
from threading import Thread


class CLInterface:
    def __init__(self):
        self.stdscr = initscr()
        keypad(self.stdscr, True)
        curs_set(False)
        timeout(-1)
        cbreak()
        start_color()
        noecho()
        self.max_y, self.max_x = getmaxyx(self.stdscr)

        self.running = True
        self.data = []
        self.keyPressed = 0

        self.window = newwin(self.max_y, self.max_x, 0, 0)

    def start(self):
        # start the thread
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        while self.running:
            # wrefresh(window)
            wclear(self.window)
            box(self.window)
            waddstr(self.window, 'Drone navigation - vision based.\n')
            waddstr(self.window, 'data')

            self.keyPressed = wgetch(self.window)
            if self.keyPressed == 27:
                wmove(self.stdscr, self.max_y, self.max_x)
                waddstr(self.window, '\nESC interrupt.\n', A_BOLD)
                wgetch(self.window)
                self.running = False
        endwin()

    def write(self, dataIn):
        self.data = dataIn

    def stop(self):
        endwin()
        return
