#!python2
# -*- coding: UTF-8 -*-

from SerialCom.serialcom import serialcom
import pygame
import Queue
import time

queue = Queue.Queue()
serialPort = serialcom(queue)
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
    s = 'a{0}b{1}c{2}d{3}e{4}f{5}g{6}h{7}i\n'.format(*valueList)
    return s


pwm0_def = 52
pwm1_def = 52
pwm2_def = 52
pwm3_def = 52
pwm4_def = 52
pwm5_def = 52
pwm6_def = 52
pwm7_def = 52

pwm0 = pwm0_def
pwm1 = pwm1_def
pwm2 = pwm2_def
pwm3 = pwm3_def
pwm4 = pwm4_def
pwm5 = pwm5_def
pwm6 = pwm6_def
pwm7 = pwm7_def


def main():

    global pwm0
    global pwm1
    global pwm2
    global pwm3
    global pwm4
    global pwm5
    global pwm6
    global pwm7

    global pwm0_def
    global pwm1_def
    global pwm2_def
    global pwm3_def
    global pwm4_def
    global pwm5_def
    global pwm6_def
    global pwm7_def

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass

            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                pwm0 = 103
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                pwm1 = 103
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                pwm2 = 103
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                pwm3 = 103
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                pwm4 = 103
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                pwm5 = 103
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pwm6 = 103
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                pwm7 = 103

            if event.type == pygame.KEYUP and event.key == pygame.K_e:
                pwm0 = pwm0_def
            if event.type == pygame.KEYUP and event.key == pygame.K_d:
                pwm1 = pwm1_def
            if event.type == pygame.KEYUP and event.key == pygame.K_f:
                pwm2 = pwm2_def
            if event.type == pygame.KEYUP and event.key == pygame.K_s:
                pwm3 = pwm3_def
            if event.type == pygame.KEYUP and event.key == pygame.K_w:
                pwm4 = pwm4_def
            if event.type == pygame.KEYUP and event.key == pygame.K_r:
                pwm5 = pwm5_def
            if event.type == pygame.KEYUP and event.key == pygame.K_q:
                pwm6 = pwm6_def
            if event.type == pygame.KEYUP and event.key == pygame.K_a:
                pwm7 = pwm7_def

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print('esc')

        values = [pwm0, pwm1, pwm2, pwm3, pwm4, pwm5, pwm6, pwm7]
        valuesString = buildDataString(values)
        print(valuesString)
        queue.put(valuesString)

        screen.blit(background, (0, 0))
        pygame.display.flip()
        clock.tick(50)

main()
