#!python2
# -*- coding: UTF-8 -*-

from threading import Thread
import logging


class DroneStateMachine:
    def __init__(self, q1, q2):
        self.possibleStates = {'default': 0, 'ascending': 1,
                               'rotating': 2, 'movingToPoint': 3,
                               'landing': 4, 'hovering': 5,
                               'hoveringOnPoint': 6}
        self.state = self.possibleStates['default']
        self.running = False
        self.queueSTM = q1
        self.queueSRL = q2
        self.objs = []
        self.lastStateLogged = False

        # logging
        self.class_logger = logging.getLogger('droneNav.StateMachine')

    def start(self):
        self.class_logger.info('Starting state machine.')
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        while self.running:

            if not self.queueSTM.empty():
                self.objs = self.queueSTM.get()
                self.queueSTM.task_done()
            else:
                pass

            if self.state == self.possibleStates['default']:
                if not self.lastStateLogged:
                    self.class_logger.info('Default state.')
                    self.lastStateLogged = True
            elif self.state == self.possibleStates['ascending']:
                if not self.lastStateLogged:
                    self.class_logger.info('Ascending state.')
                    self.lastStateLogged = True
            elif self.state == self.possibleStates['rotating']:
                if not self.lastStateLogged:
                    self.class_logger.info('Rotating state.')
                    self.lastStateLogged = True
            elif self.state == self.possibleStates['movingToPoint']:
                if not self.lastStateLogged:
                    self.class_logger.info('Moving to point state.')
                    self.lastStateLogged = True
            elif self.state == self.possibleStates['landing']:
                if not self.lastStateLogged:
                    self.class_logger.info('Landing state.')
                    self.lastStateLogged = True
            elif self.state == self.possibleStates['hovering']:
                if not self.lastStateLogged:
                    self.class_logger.info('Hovering state.')
                    self.lastStateLogged = True
            elif self.state == self.possibleStates['hoveringOnPoint']:
                if not self.lastStateLogged:
                    self.class_logger.info('Hovering on point state.')
                    self.lastStateLogged = True

    def stop(self):
        self.running = False

    def setState(self, goalState):
        self.state = goalState
        return
