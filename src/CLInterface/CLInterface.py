#!python2
# -*- coding: UTF-8 -*-

from unicurses import *
from threading import Thread
import os
import ConfigParser
import logging


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
        self.window = newwin(self.max_y, self.max_x, 0, 0)

        self.running = True
        self.keyPressed = 0

        self.settings = {'dispThresh': False, 'dispContours': False,
                         'dispVertices': False, 'dispNames': True,
                         'erodeValue': 0, 'lowerThresh': 0, 'working': True}

        # configuration parser
        self.configFilePath = ('./config.ini')
        self.configPars = ConfigParser.ConfigParser()

        # logging
        logging.basicConfig(filename='./log', format='%(asctime)s %(message)s', level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    def readConfig(self, cfg, path, setts):
        self.logger.info('Reading config file.')
        cfg.read('config.ini')

        setts['dispThresh'] = cfg.getboolean('VisionParams', 'dispThresh')
        setts['dispContours'] = cfg.getboolean('VisionParams', 'dispContours')
        setts['dispVertices'] = cfg.getboolean('VisionParams', 'dispVertices')
        setts['dispNames'] = cfg.getboolean('VisionParams', 'dispNames')
        setts['erodeValue'] = cfg.getint('VisionParams', 'erodeValue')
        setts['lowerThresh'] = cfg.getint('VisionParams', 'lowerThresh')

    def writeConfig(self, cfg, path, setts):
        self.logger.info('Writing config file.')
        configFile = open(path, 'w')

        cfg.add_section('VisionParams')
        # append all the dict in the config
        for key in setts:
            cfg.set('VisionParams', key, setts[key])

        cfg.write(configFile)
        configFile.close()

    def start(self):
        # create or load config file
        if os.path.isfile(self.configFilePath):
            self.logger.debug('The config.ini does exist.')
            self.readConfig(self.configPars,
                            self.configFilePath,
                            self.settings)
        else:
            self.logger.debug('The config file doesnt exist.')
            self.writeConfig(self.configPars,
                             self.configFilePath,
                             self.settings)

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
            elif self.keyPressed == ord('p'):
                self.writeConfig(self.configPars, self.configFilePath, self.settings)
            elif self.keyPressed == ord('o'):
                self.readConfig(self.configPars, self.configFilePath, self.settings)
            # escape key
            elif self.keyPressed == 27:
                self.settings['working'] = not self.settings['working']

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
        waddstr(self.window, 'Display mask     <q>: {0} \n'.
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
        waddstr(self.window, 'Threshold      <a,z>: {0} - 255\n'.
                             format(self.settings['lowerThresh']))
        wmove(self.window, 8, 1)
        waddstr(self.window, 'Erode          <s,x>: {0}\n'.format(self.settings['erodeValue']))
        wmove(self.window, 10, 1)
        waddstr(self.window, 'Store values to config.ini   <p>\n')
        wmove(self.window, 11, 1)
        waddstr(self.window, 'Restore values from config.ini   <o>\n')
        wmove(self.window, 14, 1)
        waddstr(self.window, 'Process working     : {0} \n'.
                             format(self.settings['working']))

    def stop(self):
        endwin()
        return
