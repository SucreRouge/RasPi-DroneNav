#!python2
# -*- coding: UTF-8 -*-

# REQUIREMENTS:
#
# pip install picamera[array]
# pip install imutils
#
#

# import the necessary packages
from __future__ import print_function
# from imutils.video.pivideostream import PiVideoStream
from piVideoStream.pivideostream import PiVideoStream
# from imutils.video import FPS
# from picamera.array import PiRGBArray
# from picamera import PiCamera
import argparse
import imutils
import time
import cv2
import Queue
import sys
import logging

from shapeDetector.shapedetector import ShapeDetector
from CLInterface.CLInterface import CLInterface
from SerialCom.serialcom import serialcom


def main():

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--display", type=int, default=-1,
                    help="Whether or not frames should be displayed")
    args = vars(ap.parse_args())

    logger = logging.getLogger('droneNav')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('./log')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(module)s %(levename)s %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # objects used
    queue = Queue.Queue()
    # vs = PiVideoStream().start()
    vs = PiVideoStream((320, 240), 60)
    vs.start()
    sd = ShapeDetector()
    cli = CLInterface()
    cli.start()
    serialPort = serialcom(queue)
    serialPort.start()

    time.sleep(2.0)
    working = True

    verts = []
    n = 0
    settings = {'dispThresh': False, 'dispContours': False,
                'dispVertices': False, 'dispNames': False,
                'dispCenters': False, 'dispTHEcenter': False,
                'erodeValue': 0, 'lowerThresh': 40, 'working': True}

    # loop over some frames...this time using the threaded stream
    while working:
        start_time = time.time()
        prev = settings['dispThresh']
        settings = cli.read()
        working = settings['working']

        # grab the frame from the threaded video stream and resize it
        frame = vs.read()
        # frame = imutils.resize(frame, width=600)
        frame = cv2.flip(frame, 0)
        # frame = cv2.copyMakeBorder(frame, 3, 3, 3, 3,
        #                            cv2.BORDER_CONSTANT, value=(255, 255, 255))
        frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frameBlurred = cv2.GaussianBlur(frameGray, (5, 5), 0)
        frameThresh = cv2.threshold(frameBlurred, settings['lowerThresh'], 255,
                                    cv2.THRESH_BINARY_INV)[1]
        frameThresh = cv2.erode(frameThresh, None,
                                iterations=settings['erodeValue'])
        frameThresh = cv2.dilate(frameThresh, None,
                                 iterations=settings['erodeValue'])
        frameThresh = cv2.copyMakeBorder(frameThresh, 3, 3, 3, 3,
                                         cv2.BORDER_CONSTANT, value=(0, 0, 0))
        frameFinal = frameThresh

        # FIND CONTOURS
        cnts = cv2.findContours(frameFinal.copy(),
                                cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        cntsCount = len(cnts)

        n = n + 1

        for c in cnts:
            M = cv2.moments(c)
            try:
                cX = int((M['m10'] / M['m00']))
                cY = int((M['m01'] / M['m00']))
                shape, verts = sd.detect(c)
            except:
                continue

            c = c.astype('float')
            c = c.astype('int')

            if settings['dispContours']:
                cv2.drawContours(frame, [c], -1, (0, 255, 0), 1)
            if settings['dispNames']:
                cv2.putText(frame, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 255, 255), 1)
            if settings['dispVertices']:
                for i in range(0, len(verts)):
                    cv2.circle(frame, tuple(verts[i]), 4, (255, 100, 100), 1)
            if settings['dispCenters']:
                cv2.circle(frame, (cX, cY), 2, (50, 255, 50), 1)

        if settings['dispTHEcenter']:
            cv2.circle(frame, (320 / 2, 240 / 2), 2, (50, 50, 255), 1)

        # HIGH GUI DISPLAY AND CONTROL
        if args['display'] > 0:
            cv2.imshow('Frame', frame)

            if settings['dispThresh']:
                cv2.imshow('Thresholded', frameFinal)
            if prev is True and settings['dispThresh'] is False:
                cv2.destroyWindow('Thresholded')

            key = cv2.waitKey(1) & 0xFF

            # input handling - ONLY IF HIGH GUI WINDOWS EXIST
            if key == 27:
                working = False

        end_time = time.time()
        logger.info('Loop dt: {0}'.format(end_time - start_time))

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()
    cli.stop()
    sys.exit(0)


# try:
main()
# except Exception as e:
#     print(e)
#     sys.exit(0)
