#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 定义一些GH小工具, 将计算逻辑与工具逻辑分开
import rhinoscriptsyntax as rs
from geometry import Point2D, Vector, Polyline, VectorTwoPts
class GHDisplay:
    '数据类型和GH的转换类'
    """
    根据实例对象来调用display方法, 但需要在逻辑代码中传入这个父类, 又需要导入rs, 暂时放放
    def display(self):
        if isinstance(self, Point2D):
            self.displayPoint()
        elif isinstance(self, Vector):
            self.displayVector()
        elif isinstance(self, Polyline):
            self.displayPolyline()

    def displayPoint(self):
        # 根据对象实例, 在gh中绘制point
        return rs.CreatePoint(self.x, self.y)

    def displayVector(self):
        return

    def displayPolyline(self):
        # 根据对象实例, 在gh中绘制polyline
        start_pt_x, start_pt_y = self.start_pt.x, self.start_pt.y
        vec_lst = self.vec_lst[:]
        pt = rs.CreatePoint(start_pt_x, start_pt_y)
        pt_lst = [pt]
        for vec in vec_lst:
            start_pt_x += vec.x; start_pt_y += vec.y
            pt = rs.CreatePoint(start_pt_x, start_pt_y)
            pt_lst.append(pt)
        poly = rs.AddPolyline(pt_lst)
        return poly
    """

    @staticmethod
    def displayPoint(pt):
        # 根据对象实例, 在gh中绘制point
        if not isinstance(pt, Point2D): return
        return rs.CreatePoint(pt.x, pt.y)

    @staticmethod
    def displayVector(vec):
        if not isinstance(pt, Vector): return
        return

    @staticmethod
    def displayPolyline(poly):
        # 根据对象实例, 在gh中绘制polyline, rectangle继承polyline
        if not isinstance(poly, Polyline): return
        start_pt_x, start_pt_y = poly.start_pt.x, poly.start_pt.y
        vec_lst = poly.vec_lst[:]
        pt = rs.CreatePoint(start_pt_x, start_pt_y)
        pt_lst = [pt]
        for vec in vec_lst:
            start_pt_x += vec.x; start_pt_y += vec.y
            pt = rs.CreatePoint(start_pt_x, start_pt_y)
            pt_lst.append(pt)
        poly = rs.AddPolyline(pt_lst)
        return poly
        


    @staticmethod
    def createPolyline(poly_gh):
        # 将gh的polyline转化成构造的polyline实例
        poly_pt_lst = rs.PolylineVertices(poly_gh)
        start_pt = Point2D(poly_pt_lst[0][0], poly_pt_lst[0][1])
        vec_lst = []
        for i in range(len(poly_pt_lst)-1):
            pt1 = poly_pt_lst[i]; pt2 = poly_pt_lst[i+1]
            vec = Vector(pt2[0]-pt1[0], pt2[1]-pt1[1])
            vec_lst.append(vec)
        polyline = Polyline(start_pt, vec_lst)
        return polyline
    
    @staticmethod
    def creatrecpointvec(rec1,rec2):
        rec1 = rs.PolylineVertices(rec1)
        origin_point1 = rec1[0]
        point1 = rec1[1]
        point_end = rec1[-2]
        vecx1 = [point1[0]-origin_point1[0],point1[1]-origin_point1[1]]
        vecy1 = [point_end[0]-origin_point1[0],point_end[1]-origin_point1[1]]

        rec2 = rs.PolylineVertices(rec2)
        origin_point2 = rec2[0]
        point1 = rec2[1]
        point_end = rec2[-2]
        vecx2 = [point1[0]-origin_point2[0],point1[1]-origin_point2[1]]
        vecy2 = [point_end[0]-origin_point2[0],point_end[1]-origin_point2[1]]
        
        return origin_point1,vecx1,vecy1,origin_point2,vecx2,vecy2


    @staticmethod
    def creatrecpoint(rec1_point,rec2_point):
        return rs.CreatePoint(rec1_point),rs.CreatePoint(rec2_point)

    """
    @staticmethod
    def creatpolyline(polyline):
        start_pt = polyline.start_pt[:]
        origin_point = rs.AddPoint(start_pt[0],start_pt[1],0)
        vec_lst = polyline.vec_lst
        point_list = [origin_point]
        for i in vec_lst:
            start_pt[0] += i[0]
            start_pt[1] += i[1]
            temp_point = rs.AddPoint(start_pt[0],start_pt[1],0)
            point_list.append(temp_point)
        poly = rs.AddPolyline(point_list)
        return poly
    """

