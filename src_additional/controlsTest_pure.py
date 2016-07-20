#!python2
# -*- coding: UTF-8 -*-

from SerialCom.serialcom import serialcom
import pygame
import Queue
import time
import sys
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--port", type=int, default=4,
                help="Bluetooth = 4,"
                     "USB TTL   = 13")
ap.add_argument("-t", "--throttle", type=float, default=1.0,
                help="The multiplier for output "
                     "(safety switch to make drone fly slower.")
args = vars(ap.parse_args())

queue = Queue.Queue()
serialPort = serialcom(queue, args['port'])
serialPort.start()
time.sleep(2.0)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((100, 100))
pygame.display.set_caption('Controls test for drone.')
pygame.mouse.set_visible(1)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((200, 200, 200))


def buildDataString(valueList):
    s = 'a{0}b{1}c{2}d{3}e{4}f{5}g\n'.format(*valueList)
    return s


def main():

    stepUP = 26
    stepDOWN = 26

    pwm0 = pwm0_neutral = 78
    pwm1 = pwm1_neutral = 78
    pwm2 = pwm2_neutral = 78
    pwm3 = pwm3_neutral = 78
    pwm4 = pwm4_neutral = 78
    pwm5 = pwm5_neutral = 78

    throttle = args['throttle']

    valuesString = ''

    print('Starting the program in 3 seconds.')
    time.sleep(1)
    print('Starting the program in 2 seconds.')
    time.sleep(1)
    print('Starting the program in 1 seconds.')
    time.sleep(1)
    print('Lesgo!')

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass

            if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                throttle = throttle + 0.1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_j:
                throttle = throttle - 0.1

            if throttle > 1:
                throttle = 1
            elif throttle < 0.1:
                throttle = 0.1

            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pwm0 = pwm0_neutral + stepUP * throttle
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                pwm0 = pwm0_neutral - stepDOWN * throttle
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                pwm1 = pwm1_neutral + stepUP * throttle
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                pwm1 = pwm1_neutral - stepDOWN * throttle
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                pwm2 = pwm2_neutral + stepUP * throttle
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                pwm2 = pwm2_neutral - stepDOWN * throttle
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                pwm3 = pwm3_neutral + stepUP * throttle
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                pwm3 = pwm3_neutral - stepDOWN * throttle
            if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                pwm4 = pwm4_neutral + stepUP * throttle
            if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                pwm4 = pwm4_neutral - stepDOWN * throttle
            if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                pwm5 = pwm5_neutral + stepUP * throttle
            if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                pwm5 = pwm5_neutral - stepDOWN * throttle

            if event.type == pygame.KEYUP and event.key == pygame.K_q:
                pwm0 = pwm0_neutral
            if event.type == pygame.KEYUP and event.key == pygame.K_a:
                pwm0 = pwm0_neutral
            if event.type == pygame.KEYUP and event.key == pygame.K_w:
                pwm1 = pwm1_neutral
            if event.type == pygame.KEYUP and event.key == pygame.K_s:
                pwm1 = pwm1_neutral
            if event.type == pygame.KEYUP and event.key == pygame.K_e:
                pwm2 = pwm2_neutral
            if event.type == pygame.KEYUP and event.key == pygame.K_d:
                pwm2 = pwm2_neutral
            if event.type == pygame.KEYUP and event.key == pygame.K_r:
                pwm3 = pwm3_neutral
            if event.type == pygame.KEYUP and event.key == pygame.K_f:
                pwm3 = pwm3_neutral
            if event.type == pygame.KEYUP and event.key == pygame.K_t:
                pwm4 = pwm4_neutral
            if event.type == pygame.KEYUP and event.key == pygame.K_g:
                pwm4 = pwm4_neutral
            if event.type == pygame.KEYUP and event.key == pygame.K_y:
                pwm5 = pwm5_neutral
            if event.type == pygame.KEYUP and event.key == pygame.K_h:
                pwm5 = pwm5_neutral

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print('Stopped by user.')
                serialPort.stop()
                sys.exit(0)

        values = [int(pwm0),
                  int(pwm1),
                  int(pwm2),
                  int(pwm3),
                  int(pwm4),
                  int(pwm5)]
        valuesString = buildDataString(values)
        print("Data {0}, and throttle {1}".format(valuesString, throttle))
        queue.put(valuesString)

        screen.blit(background, (0, 0))
        pygame.display.flip()
        clock.tick(50)

main()
