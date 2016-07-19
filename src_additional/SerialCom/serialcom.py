#!python2
# -*- coding: UTF-8 -*-

from threading import Thread
import serial
import time
import platform


class serialcom():
    """docstring for CLInfo"""
    def __init__(self, q):
        self.BaudRate = 115200
        self.Running = True
        self.numericals = []
        self.queue = q
        self.data = 'a\n'
        self.system = platform.system()
        self.PortNo = 4

    def start(self):
        if self.system == 'Windows':
            self.SP = serial.Serial("COM" + str(self.PortNo),
                                    self.BaudRate,
                                    timeout=5)
        else:
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
                temp = self.SP.read()
                if temp == 'ok\n':
                    print('AVR received the data.')
                self.queue.task_done()
            elif self.queue.empty():
                pass

        self.stop()

    def read(self):
        return self.numericals

    def stop(self):
        self.SP.close()
        return
