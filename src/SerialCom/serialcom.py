#!python2
# -*- coding: UTF-8 -*-

from threading import Thread
import serial
import re
import time


class serialcom():
    """docstring for CLInfo"""
    def __init__(self, q):
        self.BaudRate = 115200
        self.Running = True
        self.numericals = []
        self.queue = q
        self.data = 7

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
            self.SP.write(self.data)
            time.sleep(1)

            # # ile bajtow czeka
            # self.bytesToRead = self.SP.inWaiting()
            # # czyta dane jako byte object
            # self.data_received = self.SP.readline()
            # # wyswietla z decodowaniem ascii - type unicode
            # self.data_ascii = self.data_received.decode('ascii')

            # # extracting numerical values
            # try:
            #     self.tmp = re.split('[:]', self.data_ascii)
            #     self.tmp = self.tmp[1]
            #     self.tmp = re.split('[,]', str(self.tmp))
            #     self.tmp = [x.rstrip() for x in self.tmp]
            #     self.numericals = [float(i) for i in self.tmp]
            #     # print(self.numericals)
            #     self.queue.put(self.numericals)
            # except:
            #     # print('Failing at data munching [or/and] putting data into q.')
            #     pass

        self.stop()

    def read(self):
        return self.numericals

    def stop(self):
        self.SP.close()
        return
