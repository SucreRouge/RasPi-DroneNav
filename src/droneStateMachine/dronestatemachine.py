#!python2
# -*- coding: UTF-8 -*-

from threading import Thread, Timer
import logging
import array
import time


class DroneStateMachine:
    def __init__(self, q1, q2):
        self.possibleStates = {'onTheGround': 0, 'ascending': 1,
                               'rotating': 2, 'movingToPoint': 3,
                               'landing': 4, 'hovering': 5,
                               'hoveringOnPoint': 6}
        self.state = self.possibleStates['onTheGround']
        self.running = True
        self.autoMode = False
        self.queueSTM = q1
        self.queueSRL = q2
        self.objs = []
        self.lastStateLogged = False
        self.frequency = 50
        self.compute = False
        self.startTime = 0.0
        self.dt = 0.0
        self.resolution = (320, 240)
        self.dx = 0
        self.dy = 0

        # TODO: check the names below
        # throttle
        self.pwm0 = 100
        # yaw
        self.pwm1 = 150
        # pitch
        self.pwm2 = 150
        # roll
        self.pwm3 = 150
        # accessory 1
        self.pwm4 = 150
        # accessory 2
        self.pwm5 = 150

        self.values = [int(self.pwm0),
                       int(self.pwm1),
                       int(self.pwm2),
                       int(self.pwm3),
                       int(self.pwm4),
                       int(self.pwm5)]

        # logging
        self.class_logger = logging.getLogger('droneNav.StateMachine')

    def start(self):
        self.class_logger.info('Starting state machine.')
        t = Thread(target=self.update, args=())
        # t = Timer(0.02, self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        while self.running:
            if self.autoMode:
                self.lastStateLogged = False

                # getting the objects seen by camera
                if self.queueSTM.empty():
                    self.compute = False
                else:
                    self.objs = self.queueSTM.get()
                    if isinstance(self.objs, dict):
                        self.compute = True
                    self.queueSTM.task_done()

                if self.compute:
                    if self.state == self.possibleStates['onTheGround']:
                        if not self.lastStateLogged:
                            self.class_logger.info('onTheGround state.')
                            self.lastStateLogged = True
                            self.startTime = time.time()

                        # if 3 seconds from start elapsed
                        self.dt = time.time() - self.startTime
                        if self.dt > 3:
                            self.set_state(self.possibleStates['ascending'])

                    elif self.state == self.possibleStates['ascending']:
                        if not self.lastStateLogged:
                            self.class_logger.info('Ascending state.')
                            self.lastStateLogged = True
                            self.startTime = time.time()

                        self.dt = time.time() - self.startTime
                        # not seeing anything logical
                        if len(self.objs > 3) or len(self.objs < 1):
                            logText = '{0}:{1}:{2}'.format('Ascending',
                                                           'not seeing obj'
                                                           ' of interest',
                                                           self.values)
                            self.class_logger.info(logText)
                            if self.dt > 1:
                                self.startTime = time.time()
                            #     self.pwm0 = self.pwm0 + 1

                            # if self.pwm0 > 150:
                            #     self.pwm0 = 150

                        # seeing 1 2 or 3 objects
                        else:
                            logText = '{0}:{1}:{2}:{3}'.format('Ascending',
                                                               'seeing objs:',
                                                               len(self.objs),
                                                               self.values)
                            self.class_logger.info(logText)
                            if len(self.objs == 1):
                                self.dx = self.resolution[0] -self.objs[0]['center'][0]
                                self.dy = self.resolution[1] - self.objs[0]['center'][1]
                            if len(self.objs == 2):
                                self.dx = self.resolution[0] - self.objs[0]['center'][0]
                                self.dy = self.resolution[1] - self.objs[0]['center'][1]
                            if len(self.objs == 3):
                                self.dx = self.resolution[0] - self.objs[0]['center'][0]
                                self.dy = self.resolution[1] - self.objs[0]['center'][1]

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

                    # send control commands
                    self.values = [int(self.pwm0),
                                   int(self.pwm1),
                                   int(self.pwm2),
                                   int(self.pwm3),
                                   int(self.pwm4),
                                   int(self.pwm5)]
                    valuesHexString = self.build_data_hex_string(self.values)
                    self.queueSRL.put(valuesHexString)

            elif not self.autoMode:
            self.lastStateLogged = False
                # send control commands
                if not self.lastStateLogged:
                    self.class_logger.info('Auto mode off - landing.')
                    self.lastStateLogged = True
                self.values = [100, 150, 150, 150, 150, 150]
                valuesHexString = self.build_data_hex_string(self.values)
                self.queueSRL.put(valuesHexString)

    def set_mode(self, mode):
        self.autoMode = mode
        return

    def stop(self):
        self.running = False
        return

    def set_state(self, goalState):
        self.state = goalState
        self.lastStateLogged = False
        return

    def calculate_control(self, goalPos):
        # TODO: fill this function
        return

    def build_data_hex_string(self, valueList):
        valueList.insert(0, 0xAA)  # add preamble
        s = array.array('B', valueList).tostring()
        return s
