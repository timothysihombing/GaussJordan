# File GLObject.py
# Abram Perdanaputra      / 13516083
# Timothy AH Sihombing    / 13516090
#
# TUGAS BESAR 2 ALJABAR GEOMETRI

import numpy as np
import copy
import sys
import math

class Object2d(object):
    """docstring for Object2d."""

    def __init__(self, mat = np.zeros((0,0))):
        self.matrix = mat

    def copyObject(self):
        new_object = copy.deepcopy(self)
        return new_object

    def countVertex(self):
        return self.matrix.shape[1]

    def vertices(self):
        vertices = []
        for vertex in self.matrix.T:
            vertices.append((vertex[0], vertex[1]))
        return vertices

    def translate(self, dx, dy):
        new_object = self.copyObject()
        for points in new_object.matrix.T:
            points[0] += dx
            points[1] += dy
        return new_object

    def dilate(self, k):
        obj_trans = self.copyObject()
        transform = np.matrix([[k, 0],
                               [0, k]])
        temp = np.matmul(transform, obj_trans.matrix)
        for i in range(len(temp.T)):
            obj_trans.matrix[0,i] = temp[0,i]
            obj_trans.matrix[1,i] = temp[1,i]
        return obj_trans

    def rotate(self, deg, a, b):
        obj_trans = self.copyObject()
        degRad = math.radians(deg)
        transform = np.matrix([[math.cos(degRad), -1 * math.sin(degRad)],
                               [math.sin(degRad),      math.cos(degRad)]])

        obj_trans = obj_trans.translate(-a, -b)

        temp = np.matmul(transform, obj_trans.matrix)
        for i in range(len(temp.T)):
            obj_trans.matrix[0,i] = temp[0,i]
            obj_trans.matrix[1,i] = temp[1,i]

        obj_trans = obj_trans.translate(a, b)

        return obj_trans

    def reflect(self, param):
        obj_trans = self.copyObject()
        if param == "x":
            transform = np.matrix([[1,  0],
                                   [0, -1]])
            temp = np.matmul(transform, obj_trans.matrix)

            for i in range(len(temp.T)):
                obj_trans.matrix[0,i] = temp[0,i]
                obj_trans.matrix[1,i] = temp[1,i]

        elif param == "y":
            transform = np.matrix([[-1, 0],
                                   [ 0, 1]])
            temp = np.matmul(transform, obj_trans.matrix)

            for i in range(len(temp.T)):
                obj_trans.matrix[0,i] = temp[0,i]
                obj_trans.matrix[1,i] = temp[1,i]

        elif param == "y=x" or param == "x=y":
            transform = np.matrix([[0, 1],
                                   [1, 0]])
            temp = np.matmul(transform, obj_trans.matrix)

            for i in range(len(temp.T)):
                obj_trans.matrix[0,i] = temp[0,i]
                obj_trans.matrix[1,i] = temp[1,i]

        elif param == "y=-x" or param == "x=-y":
            transform = np.matrix([[0, -1],
                                   [-1, 0]])
            temp = np.matmul(transform, obj_trans.matrix)

            for i in range(len(temp.T)):
                obj_trans.matrix[0,i] = temp[0,i]
                obj_trans.matrix[1,i] = temp[1,i]

        else:
            param = param.split(",")
            xo = float(param[0])
            yo = float(param[1])

            #mencerminkan terhadap x = xo
            transform = np.matrix([[-1, 0],
                                   [ 0, 1]])

            temp = np.matmul(transform, obj_trans.matrix)

            for i in range(len(obj_trans.matrix.T)):
                obj_trans.matrix[0,i] = temp[0,i]
                obj_trans.matrix[1,i] = temp[1,i]

            obj_trans = obj_trans.translate(2 * xo, 0)

            #mencerminkan terhadap y = yo
            transform = np.matrix([[1,  0],
                                   [0, -1]])

            temp = np.matmul(transform, obj_trans.matrix)

            for i in range(len(obj_trans.matrix.T)):
                obj_trans.matrix[0,i] = temp[0,i]
                obj_trans.matrix[1,i] = temp[1,i]

            obj_trans = obj_trans.translate(0, 2 * yo)

        return obj_trans

    def shear(self, param, k):
        obj_trans = self.copyObject()
        if param == "x":
            transform = np.matrix([[1, k],
                                   [0, 1]])
        else:
            transform = np.matrix([[1, 0],
                                   [k, 1]])

        temp = np.matmul(transform, obj_trans.matrix)

        for i in range(len(temp.T)):
            obj_trans.matrix[0,i] = temp[0,i]
            obj_trans.matrix[1,i] = temp[1,i]

        return obj_trans

    def stretch(self, param, k):
        obj_trans = self.copyObject()
        if param == "x":
            transform = np.matrix([[k, 0],
                                   [0, 1]])
        else:
            transform = np.matrix([[1, 0],
                                   [0, k]])

        temp = np.matmul(transform, obj_trans.matrix)

        for i in range(len(temp.T)):
            obj_trans.matrix[0,i] = temp[0,i]
            obj_trans.matrix[1,i] = temp[1,i]

        return obj_trans

    def custom(self, a, b, c, d):
        obj_trans = self.copyObject()
        transform = np.matrix([[a, b],
                               [c, d]])

        temp = np.matmul(transform, obj_trans.matrix)

        for i in range(len(temp.T)):
            obj_trans.matrix[0,i] = temp[0,i]
            obj_trans.matrix[1,i] = temp[1,i]

        return obj_trans
