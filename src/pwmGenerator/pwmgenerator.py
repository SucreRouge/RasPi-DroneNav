#!python2
# -*- coding: UTF-8 -*-

from threading import Thread
import serial
import re
import time
import RPi.GPIO as GPIO


class pwmgenerator():
    """Class generating pwm signalns."""
    def __init__(self, q):
        self.Running = True
        self.queue = q

        self.On0 = False
        self.On1 = False
        self.On2 = False
        self.On3 = False

        self.pwm = [103, 103, 103, 103]
        self.m = 0
        self.period = 2000

    def start(self):
        GPIO.setup(1, GPIO.OUT)
        GPIO.setup(4, GPIO.OUT)
        GPIO.setup(5, GPIO.OUT)
        GPIO.setup(6, GPIO.OUT)

        GPIO.output(1, False)
        GPIO.output(4, False)
        GPIO.output(5, False)
        GPIO.output(6, False)

        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        while self.Running:
            if not self.queue.empty():
                self.pwm = self.queue.get()
                self.queue.task_done()
            elif self.queue.empty():
                pass

            # pin 1
            if self.m <= self.pwm[0] and self.On0 is False:
                GPIO.output(1, True)
                self.On0 = True
            if self.m > self.pwm[0] and self.On0 is True:
                GPIO.output(1, False)
                self.On0 = False

            # pin 4
            if self.m <= self.pwm[1] and self.On1 is False:
                GPIO.output(4, True)
                self.On1 = True
            if self.m > self.pwm[1] and self.On1 is True:
                GPIO.output(4, False)
                self.On1 = False

            # pin 5
            if self.m <= self.pwm[2] and self.On2 is False:
                GPIO.output(5, True)
                self.On2 = True
            if self.m > self.pwm[2] and self.On2 is True:
                GPIO.output(5, False)
                self.On2 = False

            # pin 6
            if self.m <= self.pwm[3] and self.On3 is False:
                GPIO.output(6, True)
                self.On3 = True
            if self.m > self.pwm[3] and self.On3 is True:
                GPIO.output(6, False)
                self.On3 = False

            self.m = self.m + 1

            if self.m >= self.period:
                self.m = 0

    def stop(self):
        self.Running = False
        GPIO.output(1, False)
        GPIO.output(4, False)
        GPIO.output(5, False)
        GPIO.output(6, False)
        return
