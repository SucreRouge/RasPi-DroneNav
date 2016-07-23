#!python2
# -*- coding: UTF-8 -*-

from threading import Thread
import logging


class DroneStateMachine:
    def __init__(self, resolution=(320, 240), framerate=60):
        self.possibleStates = {'default': 0, 'ascending': 1,
                               'rotating': 2, 'movingToPoint': 3,
                               'landing': 4, 'hovering': 5,
                               'hoveringOnPoint': 6}
        self.state = self.possibleStates['default']
        self.running = False

        # logging
        self.class_logger = logging.getLogger('droneNav.StateMachine')

    def start(self):
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        while self.running:
            if self.state == self.possibleStates['default']:
                print('default')
            elif self.state == self.possibleStates['ascending']:
                print('ascending')
            elif self.state == self.possibleStates['rotating']:
                print('rotating')
            elif self.state == self.possibleStates['movingToPoint']:
                print('moving to point')
            elif self.state == self.possibleStates['landing']:
                print('landing')
            elif self.state == self.possibleStates['hovering']:
                print('hovering')
            elif self.state == self.possibleStates['hoveringOnPoint']:
                print('hovering on Point')

    def stop(self):
        self.running = False

    def setState(self, goalState):
        self.state = goalState
        return
