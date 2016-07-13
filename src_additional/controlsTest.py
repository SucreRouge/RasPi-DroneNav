#!python2
# -*- coding: UTF-8 -*-

from SerialCom.serialcom import serialcom
import pygame
import Queue
import time

queue = Queue.Queue()
serialPort = serialcom(queue)
# serialPort.start()
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


def main():
    while 1:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                print('e')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                print('d')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                print('f')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                print('s')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                print('w')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                print('r')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                print('q')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                print('a')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print('esc')
            else:
                pwm0 = 120
                pwm1 = 120
                pwm2 = 120
                pwm3 = 120
                pwm4 = 120
                pwm5 = 120
                pwm6 = 120
                pwm7 = 120

        values = [pwm0, pwm1, pwm2, pwm3, pwm4, pwm5, pwm6, pwm7]
        valuesString = buildDataString(values)
        print(valuesString)
        # queue.put(valuesString)


        screen.blit(background, (0, 0))
        pygame.display.flip()

main()
