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
            elif self.keyPressed == ord('q'):
                self.settings['dispThresh'] = not self.settings['dispThresh']
            elif self.keyPressed == ord('w'):
                self.settings['dispContours'] = not self.settings['dispContours']
            elif self.keyPressed == ord('e'):
                self.settings['dispVertices'] = not self.settings['dispVertices']
            elif self.keyPressed == ord('r'):
                self.settings['dispNames'] = not self.settings['dispNames']
            elif self.keyPressed == ord('a'):
                self.settings['lowerThresh'] = self.settings['lowerThresh'] + 2
                if self.settings['lowerThresh'] > 255:
                    self.settings['lowerThresh'] = 255
            elif self.keyPressed == ord('z'):
                self.settings['lowerThresh'] = self.settings['lowerThresh'] - 2
                if self.settings['lowerThresh'] < 0:
                    self.settings['lowerThresh'] = 0
            elif self.keyPressed == ord('s'):
                self.settings['erodeValue'] = self.settings['erodeValue'] + 1
                if self.settings['erodeValue'] > 255:
                    self.settings['erodeValue'] = 255
            elif self.keyPressed == ord('x'):
                self.settings['erodeValue'] = self.settings['erodeValue'] - 1
                if self.settings['erodeValue'] < 0:
                    self.settings['erodeValue'] = 0

        endwin()

    def write(self, dataIn):
        self.settings = dataIn

    def read(self):
        return self.settings

    def printData(self):
        wclear(self.window)
        box(self.window)
        wmove(self.window, 0, 1)
        waddstr(self.window, 'Drone navigation - vision based.\n', A_BOLD)
        wmove(self.window, 1, 1)
        waddstr(self.window, '\n')
        wmove(self.window, 2, 1)
        waddstr(self.window, 'Parameters of the vision processing:\n', A_BOLD)
        wmove(self.window, 3, 1)
        waddstr(self.window, 'Display mask     <q>   : {0} \n'.
                             format(self.settings['dispThresh']))
        wmove(self.window, 4, 1)
        waddstr(self.window, 'Display contours <w>: {0} \n'.
                             format(self.settings['dispContours']))
        wmove(self.window, 5, 1)
        waddstr(self.window, 'Display vertices <e>: {0} \n'.
                             format(self.settings['dispVertices']))
        wmove(self.window, 6, 1)
        waddstr(self.window, 'Display names    <r>: {0} \n'.
                             format(self.settings['dispNames']))
        wmove(self.window, 7, 1)
        waddstr(self.window, 'Threshold      <a,z> {0} - 255\n'.
                             format(self.settings['lowerThresh']))
        wmove(self.window, 8, 1)
        waddstr(self.window, 'Erode          <s,x>: {0}\n'.format(self.settings['erodeValue']))

    def stop(self):
        endwin()
        return
