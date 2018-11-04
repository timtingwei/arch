#!/usr/bin/env python
#-*- coding: utf-8 -*-

class Point2D(object):
    def __init__(self, coordinate):
        self.x, self.y = coordinate
        return

class Point3D(Point2D):
    def __init__(self, coordinate):
        self.x, self.y, self.z = coordinate
        return

class PointVec(Point2D):
    def __init__(self, coordinate, vec_lst):
        self.pt = Point2D(coordinate)
        self.vec_lst = vec_lst

    def __init__(self, pt, vec_lst):
        self.pt = pt
        self.vec_lst = vec_lst

class Vector(object):
    def __init__(self, vec_x, vec_y):
        self.x, self.y = vec_x, vec_y
    def __init__(self, start_pt, end_pt):
        self.x = end_pt.x - start_pt.x
        self.y = end_pt.y - start_pt.y

class Polyline(object):
    def __init__(self, pt_lst):
        self.pt_lst = pt_lst
        self.vec_lst = getVectorList()
        self.cornerYinYangProperty_lst = getYinYangProperty()

    def getVectorList(self):
        # 根据顺序点得到向量
        vec_lst = []
        for i in range(len(self.pt_lst)-1):
            vec = Vector(self.pt_lst[i], self.pt_lst[i+1])
            vec_lst.append(vec)
        vec = Vector(self.pt_lst[-1], self.pt_lst[0])
        vec_lst.append(vec)
        return vec_lst

    def getYinYangProperty(self):
        # 得到多边形的端点阴阳角性质
        cornerYinYangProperty_lst = []
        return cornerYinYangProperty_lst
