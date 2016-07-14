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
    s = 'a{0}b{1}c{2}d{3}e{4}f{5}g{6}h{7}i'.format(*valueList)
    return s


pwm0 = 120
pwm1 = 120
pwm2 = 120
pwm3 = 120
pwm4 = 120
pwm5 = 120
pwm6 = 120
pwm7 = 120


def main():

    global pwm0
    global pwm1
    global pwm2
    global pwm3
    global pwm4
    global pwm5
    global pwm6
    global pwm7

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass

            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                pwm0 = 240
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                pwm1 = 240
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                pwm2 = 240
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                pwm3 = 240
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                pwm4 = 240
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                pwm5 = 240
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pwm6 = 240
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                pwm7 = 240

            if event.type == pygame.KEYUP and event.key == pygame.K_e:
                pwm0 = 120
            if event.type == pygame.KEYUP and event.key == pygame.K_d:
                pwm1 = 120
            if event.type == pygame.KEYUP and event.key == pygame.K_f:
                pwm2 = 120
            if event.type == pygame.KEYUP and event.key == pygame.K_s:
                pwm3 = 120
            if event.type == pygame.KEYUP and event.key == pygame.K_w:
                pwm4 = 120
            if event.type == pygame.KEYUP and event.key == pygame.K_r:
                pwm5 = 120
            if event.type == pygame.KEYUP and event.key == pygame.K_q:
                pwm6 = 120
            if event.type == pygame.KEYUP and event.key == pygame.K_a:
                pwm7 = 120

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print('esc')

        values = [pwm0, pwm1, pwm2, pwm3, pwm4, pwm5, pwm6, pwm7]
        valuesString = buildDataString(values)
        print(valuesString)
        # queue.put(valuesString)

        screen.blit(background, (0, 0))
        pygame.display.flip()
        clock.tick(50)

main()
