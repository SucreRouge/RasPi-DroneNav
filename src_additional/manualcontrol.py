#!python2
# -*- coding: UTF-8 -*-

"""
A module for manual controlling the drone with keyboard.
Keys used:
    E,D,S,F,I,K,J,L,X,1,2

.. moduleauthor:: Michal Ciesielski <ciesielskimm@gmail.com>

"""

from SerialCom.serialcom import serialcom
import pygame
import Queue
import time
import sys
import argparse
import array

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--port", type=int, default=4,
                help="Bluetooth = 4,"
                "USB TTL   = 13")
ap.add_argument("-t", "--throttle", type=float, default=1.0,
                help="The multiplier for output "
                "(safety switch to make drone fly slower.")
args = vars(ap.parse_args())


class ManualControl(object):
    """Class which lets control drone manually."""
    def __init__(self, portNr=args['port'], throttle=args['throttle']):

        self.queue = Queue.Queue()
        self.serialPort = serialcom(self.queue, portNr)
        self.serialPort.start()

        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((100, 100))
        pygame.display.set_caption('Controls test for drone.')
        pygame.mouse.set_visible(1)

        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((200, 200, 200))

        self.throttle = throttle
        self.working = True

        self.stepUP = 50
        self.stepDOWN = 50

        self.pwm0 = self.pwm0_neutral = 100
        self.pwm1 = self.pwm1_neutral = 150
        self.pwm2 = self.pwm2_neutral = 150
        self.pwm3 = self.pwm3_neutral = 150
        self.pwm4 = self.pwm4_neutral = 150
        self.pwm5 = self.pwm5_neutral = 150

        self.pwm4_State = 0
        self.pwm5_State = 0

    def build_data_string(self, valueList):
        s = 'a{0}b{1}c{2}d{3}e{4}f{5}g\n'.format(*valueList)
        return s

    def build_data_hex_string(self, valueList):
        valueList.insert(0, 0xAA)  # add preamble
        s = array.array('B', valueList).tostring()
        return s

    def handle_input(self, events):

        for event in events:
            if event.type == pygame.QUIT:
                pass

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHTBRACKET:
                self.throttle = self.throttle + 0.1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFTBRACKET:
                self.throttle = self.throttle - 0.1

            if self.throttle > 1:
                self.throttle = 1
            elif self.throttle < 0.1:
                self.throttle = 0.1

            # keys pressed

            # throttle
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                # self.pwm0 = self.pwm0_neutral + self.stepUP * self.throttle
                self.pwm0 = self.pwm0 + 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                # self.pwm0 = self.pwm0_neutral - self.stepDOWN * self.throttle
                self.pwm0 = self.pwm0 - 1

            if self.pwm0 < 100:
                self.pwm0 = 100
            elif self.pwm0 > 200:
                self.pwm0 = 200

            # safety switch - throttle full down
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                self.pwm0 = 100

            # rest of dofs
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.pwm1 = self.pwm1_neutral + self.stepUP * self.throttle
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                self.pwm1 = self.pwm1_neutral - self.stepDOWN * self.throttle
            if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                self.pwm2 = self.pwm2_neutral + self.stepUP * self.throttle
            if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                self.pwm2 = self.pwm2_neutral - self.stepDOWN * self.throttle
            if event.type == pygame.KEYDOWN and event.key == pygame.K_j:
                self.pwm3 = self.pwm3_neutral + self.stepUP * self.throttle
            if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                self.pwm3 = self.pwm3_neutral - self.stepDOWN * self.throttle

            # keys not pressed
            # if event.type == pygame.KEYUP and event.key == pygame.K_e:
                # self.pwm0 = self.pwm0_neutral
            # if event.type == pygame.KEYUP and event.key == pygame.K_d:
                # self.pwm0 = self.pwm0_neutral
            if event.type == pygame.KEYUP and event.key == pygame.K_s:
                self.pwm1 = self.pwm1_neutral
            if event.type == pygame.KEYUP and event.key == pygame.K_f:
                self.pwm1 = self.pwm1_neutral
            if event.type == pygame.KEYUP and event.key == pygame.K_i:
                self.pwm2 = self.pwm2_neutral
            if event.type == pygame.KEYUP and event.key == pygame.K_k:
                self.pwm2 = self.pwm2_neutral
            if event.type == pygame.KEYUP and event.key == pygame.K_j:
                self.pwm3 = self.pwm3_neutral
            if event.type == pygame.KEYUP and event.key == pygame.K_l:
                self.pwm3 = self.pwm3_neutral

            # accessories
            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                self.pwm4_State = self.pwm4_State + 1
                if self.pwm4_State > 1:
                    self.pwm4_State = -1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                self.pwm5_State = self.pwm5_State + 1
                if self.pwm5_State > 1:
                    self.pwm5_State = -1

            self.pwm4 = self.pwm4_neutral + self.pwm4_State * self.stepDOWN
            self.pwm5 = self.pwm5_neutral + self.pwm5_State * self.stepDOWN

            # closing app
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print('Stopped by user.')
                return False

        values = [int(self.pwm0),
                  int(self.pwm1),
                  int(self.pwm2),
                  int(self.pwm3),
                  int(self.pwm4),
                  int(self.pwm5)]
        valuesString = self.build_data_string(values)
        valuesHexString = self.build_data_hex_string(values)
        print("Data {0}, and throttle {1}".format(valuesString, self.throttle))
        # self.queue.put(valuesString)
        self.queue.put(valuesHexString)

        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
        self.clock.tick(50)

    def main(self):

        print('Starting with settings: port {0}, throttle {1}'.format(args['port'], args['throttle']))
        time.sleep(1)
        print('Lesgo!')

        while self.working:
            e = pygame.event.get()
            t = self.handle_input(e)

            if t is False:
                pygame.quit()
                self.serialPort.stop()
                self.working = False


if __name__ == "__main__":
    ctrl = ManualControl(portNr=args['port'], throttle=args['throttle'])
    ctrl.main()
