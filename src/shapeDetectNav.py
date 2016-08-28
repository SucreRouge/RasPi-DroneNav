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
import os

from shapeDetector.shapedetector import ShapeDetector
from CLInterface.CLInterface import CLInterface
from SerialCom.serialcom import SerialCom
from droneStateMachine.dronestatemachine import DroneStateMachine


def processFrame(fr, setts):
    """ Takes frame and processes it based on settings. """
    # frame = imutils.resize(frame, width=600)
    fr = cv2.flip(fr, 0)
    # frame = cv2.copyMakeBorder(frame, 3, 3, 3, 3,
    #                            cv2.BORDER_CONSTANT, value=(255, 255, 255))
    frameGray = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    frameBlurred = cv2.GaussianBlur(frameGray, (5, 5), 0)
    frameThresh = cv2.threshold(frameBlurred, setts['lowerThresh'], 255,
                                cv2.THRESH_BINARY_INV)[1]
    frameThresh = cv2.erode(frameThresh, None,
                            iterations=setts['erodeValue'])
    frameThresh = cv2.dilate(frameThresh, None,
                             iterations=setts['erodeValue'])
    frameThresh = cv2.copyMakeBorder(frameThresh, 3, 3, 3, 3,
                                     cv2.BORDER_CONSTANT, value=(0, 0, 0))
    frameFinal = frameThresh

    return frameFinal


def createLogger(log_dir):
    """
    Takes dir for log file.
    Returns logger object with formatter and file handle.
    """
    log = logging.getLogger('droneNav')
    log.setLevel(logging.DEBUG)
    # TODO: check this new log path
    fh = logging.FileHandler(log_dir + 'log')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(module)s '
                                  '%(levelname)s %(message)s')
    fh.setFormatter(formatter)
    log.addHandler(fh)
    return log


def drawCntrsFeatures(fr, setts, obj):
    """
    Takes frame, settings, objects list and draws features (contours, names,
    vertives, centers) on frame.
    """
    if setts['dispContours']:
        cv2.drawContours(fr, [obj['contour']], -1, (0, 255, 0), 1)
    if setts['dispNames']:
        cv2.putText(fr, obj['shapeName'], obj['center'], cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 255), 1)
    if setts['dispVertices']:
        for i in range(0, len(obj['verts'])):
            cv2.circle(fr, tuple(obj['verts'][i]), 4, (255, 100, 100), 1)
    if setts['dispCenters']:
        cv2.circle(fr, (obj['center']), 2, (50, 255, 50), 1)


def main():
    """ Main program loop. """
    # #####################################################################
    # VARIABLES USED
    # #####################################################################
    main_dir = os.path.dirname(__file__)
    working = True
    objs = []
    resolution = (320, 240)
    settings = {'dispThresh': False, 'dispContours': False,
                'dispVertices': False, 'dispNames': False,
                'dispCenters': False, 'dispTHEcenter': False,
                'erodeValue': 0, 'lowerThresh': 40, 'working': True}
    # #####################################################################

    # #####################################################################
    # OBJECTS USED
    # #####################################################################
    logger = createLogger(main_dir)
    queueSRL = Queue.Queue()
    queueCLI = Queue.Queue()
    queueSTM = Queue.Queue()
    # vs = PiVideoStream().start()
    vs = PiVideoStream(resolution, 60)
    sd = ShapeDetector()
    cli = CLInterface(queueCLI, main_dir)
    serialPort = SerialCom(queueSRL)
    stm = DroneStateMachine(queueSTM, queueSRL)

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--display", type=int,
                    help="Whether or not frames should be displayed.")
    ap.add_argument("-c", "--cli", type=int,
                    help="Whether or not curses process should start.")
    args = vars(ap.parse_args())
    # #####################################################################

    print('Starting in 3...')
    time.sleep(1)
    print('Starting in 2...')
    time.sleep(1)
    print('Starting in 1...')
    time.sleep(1)

    # #####################################################################
    # STARTING
    # #####################################################################
    vs.start()
    if args['cli'] > 0:
        cli.start()
    serialPort.start()
    stm.start()
    time.sleep(2)  # necessary so camera can start properly

    # #####################################################################

    # #####################################################################
    # MAIN LOOP
    # #####################################################################
    while working:
        start_time = time.time()
        prev = settings['dispThresh']

        # settings = cli.read()
        if not queueCLI.empty():
            settings = queueCLI.get()
            queueCLI.task_done()

        working = settings['working']

        # grab the frame from the threaded video stream...
        frame = vs.read()
        # ...and process it
        frameProcessed = processFrame(frame, settings)

        # FIND CONTOURS
        cnts = cv2.findContours(frameProcessed.copy(),
                                cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        shapesCount = len(cnts)

        # clear list
        objs = []
        j = 0
        for c in cnts:
            M = cv2.moments(c)
            try:
                cX = int((M['m10'] / M['m00']))
                cY = int((M['m01'] / M['m00']))
                # shape, verts = sd.detect(c)
                objs.append(sd.detect(c))
                objs[j]['contour'] = c
                objs[j]['center'] = (cX, cY)
            except:
                continue

            c = c.astype('float')
            c = c.astype('int')

            drawCntrsFeatures(frame, settings, objs[j])
            j += 1

        # send objects to state machine
        queueSTM.put(objs)

        if settings['dispTHEcenter']:
            cv2.circle(frame, (resolution[0] / 2, resolution[1] / 2),
                       2, (50, 50, 255), 1)

        if shapesCount == 1:
            try:
                cv2.line(frame, (resolution[0] / 2, resolution[1] / 2),
                         objs[0]['center'], (255, 0, 0), 2)
            except:
                pass

        # HIGH GUI DISPLAY AND CONTROL
        if args['display'] > 0:
            cv2.imshow('Frame', frame)

            if settings['dispThresh']:
                cv2.imshow('Thresholded', frameProcessed)
            if prev is True and settings['dispThresh'] is False:
                cv2.destroyWindow('Thresholded')

            key = cv2.waitKey(1) & 0xFF

            # input handling - ONLY IF HIGH GUI WINDOWS EXIST
            if key == 27:
                working = False

        end_time = time.time()
        # logger.info('Loop dt: {0}'.format(end_time - start_time))
    # #####################################################################

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()
    cli.stop()
    sys.exit(0)


if __name__ == "__main__":
    main()
