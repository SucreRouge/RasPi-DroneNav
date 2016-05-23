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
        # self.data = {}
        self.settings = {'dispThresh': False, 'dispContours': True,
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
            elif key == ord('w'):
                settings['dispContours'] = not settings['dispContours']
            elif key == ord('e'):
                settings['dispVertices'] = not settings['dispVertices']
            elif key == ord('r'):
                settings['dispNames'] = not settings['dispNames']
            elif key == ord('a'):
                settings['lowerThresh'] = settings['lowerThresh'] + 2
                if settings['lowerThresh'] > 255:
                    settings['lowerThresh'] = 255
            elif key == ord('z'):
                settings['lowerThresh'] = settings['lowerThresh'] - 2
                if settings['lowerThresh'] < 0:
                    settings['lowerThresh'] = 0
            elif key == ord('s'):
                settings['erodeValue'] = settings['erodeValue'] + 1
                if settings['erodeValue'] > 255:
                    settings['erodeValue'] = 255
            elif key == ord('x'):
                settings['erodeValue'] = settings['erodeValue'] - 1
                if settings['erodeValue'] < 0:
                    settings['erodeValue'] = 0

        endwin()

    def write(self, dataIn):
        self.data = dataIn

    def read(self):
        return self.data

    def printData(self):
        wclear(self.window)
        box(self.window)
        wmove(self.window, 0, 1)
        waddstr(self.window, 'Drone navigation - vision based.\n', A_BOLD)
        waddstr(self.window, '\n')
        waddstr(self.window, 'Parameters of the vision processing:\n', A_BOLD)
        waddstr(self.window, 'Display contours: {0} \n'.
                             format(settings['dispContours']))
        waddstr(self.window, 'Display vertices: {0} \n'.
                             format(settings['dispVertices']))
        waddstr(self.window, 'Display names: {0} \n'.
                             format(settings['dispNames']))
        waddstr(self.window, 'Threshold {0} - 255\n'.
                             format(self.data['lowerThresh']))
        waddstr(self.window, 'Erode: {0}\n'.format(self.data['erodeValue']))

    def stop(self):
        endwin()
        return
