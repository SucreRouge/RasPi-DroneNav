#!python2

from unicurses import *
from threading import Thread


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

        self.running = True
        self.data = []
        self.keyPressed = 0

        self.window = newwin(self.max_y, self.max_x, 0, 0)
        box(self.window)

    def start(self):
        # start the thread
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        while Running:
            # wrefresh(window)
            wclear(self.window)
            waddstr(self.window, 'Test.')

            self.keyPressed = wgetch(self.window)
            if self.keyPressed == 27:
                waddstr(self.window, '\nESC interrupt.\n', uCu.A_BOLD)
                wgetch(self.window)
                self.running = False
        endwin()

    def write(self, dataIn):
        self.data = dataIn

    def stop(self):
        return
