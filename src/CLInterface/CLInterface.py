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
        self.data = {'dispThresh': False, 'dispContours': True,
                     'dispVertices': True, 'dispNames': True,
                     'erodeValue': 0, 'lowerThresh': 0}
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
            self.printData()

            self.keyPressed = wgetch(self.window)
            if self.keyPressed == 27:
                wmove(self.stdscr, self.max_y, self.max_x)
                waddstr(self.window, '\nESC interrupt.\n', A_BOLD)
                wgetch(self.window)
                self.running = False
        endwin()

    def write(self, dataIn):
        self.data = dataIn

    def printData(self):
        wclear(self.window)
        box(self.window)
        wmove(self.window, 0, 1)
        waddstr(self.window, 'Drone navigation - vision based.\n')
        waddstr(self.window, '\n')
        waddstr(self.window, 'Parameters of the vision processing:\n')
        waddstr(self.window, 'Threshold {0} - 255'.format(self.data['lowerThresh']))

    def stop(self):
        endwin()
        return
