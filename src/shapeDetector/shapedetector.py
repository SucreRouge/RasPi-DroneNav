#!python2
# -*- coding: UTF-8 -*-

"""
A module which approximates the contour (input), gives it a name
based on number of vertices and returns simplified contour with it's
vertices, area and name .

.. moduleauthor:: Michal Ciesielski <ciesielskimm@gmail.com>

"""

import cv2


class ShapeDetector:
    def __init__(self):
        """
        An __init__ function that does nothing.
        """
        pass

    def detect(self, c):
        """
        This functiion simplifies the contour, identifies shape by name,
        unpacks vertices, computes area. Then it returns a dictionary with
        all of this data.

        :param c: Contour to be approximated.
        :type c: OpenCV2 contour.
        :returns: dictionary -- shape name, vertices, approximated contour,
        approximated area.
        :rtype: dictionary.
        """
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approxPerimeter = cv2.approxPolyDP(c, 0.04 * peri, True)
        verts = []
        vrt = []
        approxPerimeterArea = cv2.contourArea(approxPerimeter)

        # #####################################################################
        # GETTING THE VERTICES COORDINATES
        # #####################################################################
        for i in range(0, len(approxPerimeter)):
            # iterate over vertices (needs additional [0]
            vrt = []
            for j in range(0, 2):
                vrt.append(int(approxPerimeter[i][0][j]))
            verts.append(vrt)
        # #####################################################################

        # #####################################################################
        # NAMING THE OBJECT
        # #####################################################################
        # if the shape is a triangle, it will have 3 vertices
        if len(approxPerimeter) == 3:
            shape = "triangle"

        # if the shape has 4 vertices, it is either a square or
        # a rectangle
        elif len(approxPerimeter) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approxPerimeter)
            ar = w / float(h)

            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

        # if the shape is a pentagon, it will have 5 vertices
        elif len(approxPerimeter) == 5:
            shape = "pentagon"

        # otherwise, we assume the shape is a circle
        else:
            shape = "circle"
        # #####################################################################

        return {'shapeName': shape,
                'verts': verts,
                'approxPerimeter': approxPerimeter,
                'approxPerimeterArea': approxPerimeterArea}
