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
        self.frequency = 50
        self.compute = False
        self.stateStartTime = 0.0
        self.dt = 0.0
        self.resolution = (320, 240)
        self.dx = 0
        self.dy = 0

        self.log_state_once = self.run_once(self.log_state)

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
        self.stateStartTime = time.time()
        t.daemon = True
        t.start()
        return self

    def update(self):
        while self.running:
            if self.autoMode:

                # getting the objects seen by camera
                if self.queueSTM.empty():
                    self.compute = False
                else:
                    self.objs = self.queueSTM.get()
                    if isinstance(self.objs, list):
                        self.compute = True
                    self.queueSTM.task_done()

                if self.compute:
                    if self.state == self.possibleStates['onTheGround']:
                        self.log_state_once()

                        # if 3 seconds from start elapsed
                        self.dt = time.time() - self.stateStartTime
                        if self.dt > 5:
                            self.set_state(self.possibleStates['ascending'])

                    elif self.state == self.possibleStates['ascending']:
                        self.log_state_once()

                        self.dt = time.time() - self.stateStartTime
                        # not seeing anything logical
                        if len(self.objs > 3) or len(self.objs < 1):
                            logText = '{0}:{1}:{2}'.format('Ascending',
                                                           'not seeing obj'
                                                           ' of interest',
                                                           self.values)
                            self.class_logger.info(logText)
                            if self.dt > 1:
                                self.stateStartTime = time.time()
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
                        self.log_state_once()

                    elif self.state == self.possibleStates['movingToPoint']:
                        self.log_state_once()

                    elif self.state == self.possibleStates['landing']:
                        self.log_state_once()

                    elif self.state == self.possibleStates['hovering']:
                        self.log_state_once()

                    elif self.state == self.possibleStates['hoveringOnPoint']:
                        self.log_state_once()

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
                # send control commands
                self.values = [100, 150, 150, 150, 150, 150]
                valuesHexString = self.build_data_hex_string(self.values)
                self.queueSRL.put(valuesHexString)

    def log_state(self, state):
        if state == self.possibleStates['onTheGround']:
            logText = '{:16s}: dt {2.3f}'.format('onTheGround', self.dt)
        elif state == self.possibleStates['ascending']:
            logText = '{:16s}'.format('ascending')
        elif state == self.possibleStates['rotating']:
            logText = '{:16s}'.format('rotating')
        elif state == self.possibleStates['movingToPoint']:
            logText = '{:16s}'.format('movingToPoint')
        elif state == self.possibleStates['landing']:
            logText = '{:16s}'.format('landing')
        elif state == self.possibleStates['hovering']:
            logText = '{:16s}'.format('hovering')
        elif state == self.possibleStates['hoveringOnPoint']:
            logText = '{:16s}'.format('hoveringOnPoint')

        self.class_logger.info(logText)
        return

    def set_mode(self, mode):
        self.autoMode = mode
        self.log_state_once.has_run = False
        return

    def stop(self):
        self.running = False
        self.log_state_once.has_run = False
        return

    def set_state(self, goalState):
        self.state = goalState
        self.stateStartTime = time.time()
        self.log_state_once.has_run = False
        return

    def calculate_control(self, goalPos):
        # TODO: fill this function
        return

    def build_data_hex_string(self, valueList):
        valueList.insert(0, 0xAA)  # add preamble
        s = array.array('B', valueList).tostring()
        return s

    def run_once(self, f):
        def wrapper(*args, **kwargs):
            if not wrapper.has_run:
                wrapper.has_run = True
                return f(*args, **kwargs)
        wrapper.has_run = False
        return wrapper
