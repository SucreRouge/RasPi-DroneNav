#!python2
# -*- coding: UTF-8 -*-

from threading import Thread
import serial
import logging


class SerialCom():
    """docstring for CLInfo"""
    def __init__(self, q):
        self.BaudRate = 115200
        self.running = True
        self.numericals = []
        self.queueSRL = q
        self.data = 'a\n'

        self.classLogger = logging.getLogger('droneNav.SerialCom')
        self.valuesLogger = logging.getLogger('serialCom.SerialCom')

    def start(self):
        self.classLogger.debug('Starting serial com.')
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
        while self.running:
            if not self.queueSRL.empty():
                self.data = self.queueSRL.get()
                self.queueSRL.task_done()
                self.SP.write(self.data)

                try:
                    logText = '{0}:{1}:{2}:{3}:{4}:{5}'.format(ord(self.data[0]),
                                                               ord(self.data[1]),
                                                               ord(self.data[2]),
                                                               ord(self.data[3]),
                                                               ord(self.data[4]),
                                                               ord(self.data[5])
                                                               )
                    self.valuesLogger.debug(logText)
                    pass
                except Exception as e:
                    pass
            else:
                pass

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
            #     self.queueSRL.put(self.numericals)
            # except:
            #     # print('Failing at data munching [or/and] putting data into q.')
            #     pass

        self.stop()

    def read(self):
        return self.numericals

    def stop(self):
        self.SP.close()
        return
