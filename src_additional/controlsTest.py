#!python2
# -*- coding: UTF-8 -*-

from SerialCom.serialcom import serialcom
import pygame
import Queue
import time
import sys
import argparse
import math

ap = argparse.ArgumentParser()
ap.add_argument("-m", "--mode", type=int, default=0,
                help="Direct control = 0,"
                     "Sinus on all = 1,"
                     "Sinus one by one = 2")
args = vars(ap.parse_args())

queue = Queue.Queue()
serialPort = serialcom(queue, 4)
serialPort.start()
time.sleep(2.0)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Controls test for drone.')
pygame.mouse.set_visible(1)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))


def buildDataString(valueList):
    s = 'a{0}b{1}c{2}d{3}e{4}f{5}g\n'.format(*valueList)
    return s


pwm0_low = 100
pwm1_low = 100
pwm2_low = 100
pwm3_low = 100
pwm4_low = 100
pwm5_low = 100

pwm0_neutral = 500
pwm1_neutral = 500
pwm2_neutral = 500
pwm3_neutral = 500
pwm4_neutral = 500
pwm5_neutral = 500

pwm0_high = 900
pwm1_high = 900
pwm2_high = 900
pwm3_high = 900
pwm4_high = 900
pwm5_high = 900

pwm0 = pwm0_neutral
pwm1 = pwm1_neutral
pwm2 = pwm2_neutral
pwm3 = pwm3_neutral
pwm4 = pwm4_neutral
pwm5 = pwm5_neutral

frameNumber = 0
sinusSpeed = 0.001
pwmNumber = 0
valuesString = ''


def main():

    global frameNumber
    global sinusSpeed
    global pwmNumber
    global valuesString

    global pwm0
    global pwm1
    global pwm2
    global pwm3
    global pwm4
    global pwm5

    global pwm0_low
    global pwm1_low
    global pwm2_low
    global pwm3_low
    global pwm4_low
    global pwm5_low

    global pwm0_neutral
    global pwm1_neutral
    global pwm2_neutral
    global pwm3_neutral
    global pwm4_neutral
    global pwm5_neutral

    global pwm0_high
    global pwm1_high
    global pwm2_high
    global pwm3_high
    global pwm4_high
    global pwm5_high

    print('Waiting for 3 seconds.')
    time.sleep(3)
    print('Lesgo!')

    # FIRST MODE
    if args['mode'] == 0:
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pass

                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    pwm0 = pwm0_high
                if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                    pwm0 = pwm0_low
                if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                    pwm1 = pwm1_high
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    pwm1 = pwm1_low
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    pwm2 = pwm2_high
                if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    pwm2 = pwm2_low
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    pwm3 = pwm3_high
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    pwm3 = pwm3_low
                if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                    pwm4 = pwm4_high
                if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                    pwm4 = pwm4_low
                if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                    pwm5 = pwm5_high
                if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                    pwm5 = pwm5_low

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
                    serialPort.stop()
                    sys.exit(0)

            frameNumber += 1

            values = [pwm0, pwm1, pwm2, pwm3, pwm4, pwm5]
            valuesString = buildDataString(values)
            print(valuesString)
            queue.put(valuesString)

            screen.blit(background, (0, 0))
            pygame.display.flip()
            clock.tick(50)

    # SECOND MODE
    elif args['mode'] == 1:
        while 1:
            pwm0 = int(pwm0_neutral + (pwm0_high - pwm0_neutral) * math.sin(sinusSpeed * frameNumber * math.pi))
            pwm1 = pwm2 = pwm3 = pwm4 = pwm5 = pwm0

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    serialPort.stop()
                    sys.exit(0)

            frameNumber += 1

            values = [pwm0, pwm1, pwm2, pwm3, pwm4, pwm5]
            valuesString = buildDataString(values)
            print(valuesString)
            queue.put(valuesString)

            screen.blit(background, (0, 0))
            pygame.display.flip()
            clock.tick(50)

    elif args['mode'] == 2:
        while 1:
            sinusSpeed = 0.01
            sinusArgument = sinusSpeed * frameNumber * math.pi

            if pwmNumber == 0:
                pwm0 = int(pwm0_neutral + (pwm0_high - pwm0_neutral) * math.sin(sinusArgument))
            elif pwmNumber == 1:
                pwm1 = int(pwm1_neutral + (pwm1_high - pwm1_neutral) * math.sin(sinusArgument))
            elif pwmNumber == 2:
                pwm2 = int(pwm2_neutral + (pwm2_high - pwm2_neutral) * math.sin(sinusArgument))
            elif pwmNumber == 3:
                pwm3 = int(pwm3_neutral + (pwm3_high - pwm3_neutral) * math.sin(sinusArgument))
            elif pwmNumber == 4:
                pwm4 = int(pwm4_neutral + (pwm4_high - pwm4_neutral) * math.sin(sinusArgument))
            elif pwmNumber == 5:
                pwm5 = int(pwm5_neutral + (pwm5_high - pwm5_neutral) * math.sin(sinusArgument))

            # if the argument is multipication of 2 pi
            # frame number condition so that it doesn't jump to pwmNumber 2 at the start
            if sinusArgument % (2 * math.pi) == 0 and frameNumber > 10:
                pwmNumber += 1

            if pwmNumber > 5:
                pwmNumber = 0

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    serialPort.stop()
                    sys.exit(0)

            frameNumber += 1

            values = [pwm0, pwm1, pwm2, pwm3, pwm4, pwm5]
            valuesString = buildDataString(values)
            print(valuesString)
            queue.put(valuesString)

            screen.blit(background, (0, 0))
            pygame.display.flip()
            clock.tick(50)

    elif args['mode'] == 3:
        step = 1
        stage = 0
        sinusArgument = 0.00001
        print('Starting LEFT up down.')
        while 1:
            # left up down
            if stage == 0:
                pwm5 = int(pwm5 + step)
                if pwm5 > pwm5_high or pwm5 < pwm5_low:
                    step = -step

                if pwm5 == pwm5_neutral:
                    stage = 9
                    print('Starting accessory1.')
                    time.sleep(5)
            # right left right
            elif stage == 1:
                pwm4 = int(pwm4 + step)
                if pwm4 > pwm4_high or pwm4 < pwm4_low:
                    step = -step

                if pwm4 == pwm4_neutral:
                    stage = 5
                    print('Starting accessory0.')
                    time.sleep(5)
            # right up down
            elif stage == 2:
                pwm2 = int(pwm2 + step)
                if pwm2 > pwm2_high or pwm2 < pwm2_low:
                    step = -step

                if pwm2 == pwm2_neutral:
                    stage = 3
                    print('Starting LEFT left right.')
                    time.sleep(5)
            # left left right
            elif stage == 3:
                pwm3 = int(pwm3 + step)
                if pwm3 > pwm3_high or pwm3 < pwm3_low:
                    step = -step

                if pwm3 == pwm3_neutral:
                    stage = 4
                    print('Starting flight mode.')
                    time.sleep(5)
            # flight mode
            elif stage == 4:
                pwm1 = pwm1 + step
                if pwm1 > pwm1_high or pwm1 < pwm1_low:
                    step = -step

                if pwm1 == pwm1_neutral:
                    stage = 2
                    print('Starting RIGHT up down.')
                    time.sleep(5)
            # accessory0
            elif stage == 5:
                pwm0 = pwm0 + step
                if pwm0 > pwm0_high or pwm0 < pwm0_low:
                    step = -step

                if pwm0 == pwm0_neutral:
                    stage = 1
                    print('Starting RIGHT left right.')
                    time.sleep(5)
            # center all
            elif stage == 9:
                pwm0 = pwm0_neutral
                pwm1 = pwm1_neutral
                pwm2 = pwm2_neutral
                pwm3 = pwm3_neutral
                pwm4 = pwm4_neutral
                pwm5 = pwm5_neutral
                if pwm5 == pwm5_neutral:
                    stage = 10
                    print('Starting everything to max.')
                    time.sleep(5)
            # evertyhing to max in all directions
            elif stage == 10:
                pwm0 = int(pwm0_neutral + (pwm0_high - pwm0_neutral) * math.sin(sinusArgument))
                pwm1 = pwm2 = pwm3 = pwm4 = pwm5 = pwm0
                sinusArgument = sinusSpeed * frameNumber * math.pi
                if sinusArgument % (2 * math.pi) == 0 and frameNumber > 10:
                    stage = 11
            elif stage == 11:
                print('We done here')
                time.sleep(5)
                sys.exit()

            frameNumber += 1

            values = [int(pwm0), int(pwm1), int(pwm2), int(pwm3), int(pwm4), int(pwm5)]
            valuesString = buildDataString(values)
            print(valuesString)
            queue.put(valuesString)

            screen.blit(background, (0, 0))
            pygame.display.flip()
            clock.tick(50)

main()
