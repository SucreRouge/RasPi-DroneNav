#!python2
# -*- coding: UTF-8 -*-

from threading import Thread
import serial
import time


class serialcom():
    """docstring for CLInfo"""
    def __init__(self, q):
        self.BaudRate = 115200
        self.Running = True
        self.numericals = []
        self.queue = q
        self.data = 'a\n'

    def start(self):
        self.SP = serial.Serial('/dev/ttyAMA0',
                                self.BaudRate,
                                timeout=5)
        self.SP.flush()
        self.SP.flushInput()

        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        while self.Running:
            if not self.queue.empty():
                self.data = self.queue.get()
                self.SP.write(self.data)
                self.queue.task_done()
            elif self.queue.empty():
                pass

        self.stop()

    def read(self):
        return self.numericals

    def stop(self):
        self.SP.close()
        return
