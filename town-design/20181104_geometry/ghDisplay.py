#!/usr/bin/env python
#-*- coding: utf-8 -*-
# 定义一些GH小工具, 将计算逻辑与展示逻辑分开
# 将rhinoscriptsyntax, geometry, rectangleArrange, rectangleShortestPath 作为lib
import rhinoscriptsyntax as rs
from geometry import Point2D, Vector, Polyline, Rectangle, Domain, Arch
import rectangleArrange
import rectangleShortestPath

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
        if not isinstance(vec, Vector): return
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
    def displaychoicepointvec(rec,edge_index,length):
        #根据一个矩形,以及矩形上面的边号和长度,输出该点的向量
        remove_index = [1,2,3,0]
        vec_list = []
        for i in rec.vec_lst:
            i_temp = i.unit()
            temp_ve = rs.CreateVector(i_temp.x,i_temp.y,0)
            vec_list.append(temp_ve)
        if length == 0:
            return vec_list
        else:
            del vec_list[remove_index[edge_index]]
            return vec_list
        
    @staticmethod   
    def displaychoicepoint(rec,edge_index,length):
        #根据一个矩形,以及矩形上面的边号和长度,输出gh上的点
        temp_vec = rec.vec_lst[edge_index].unit().amplify(length)
        pt = rec.pt_lst[edge_index]
        new_pt = pt.addVec(temp_vec)
        return rs.AddPoint(new_pt.x,new_pt.y,0)
    @staticmethod   
    def displayrecedgenumber(rec):
        #根据一个矩形,输出gh上矩形的中点和显示的文本
        all_text = []
        all_point = []
        for i in range(0,len(rec.pt_lst)):
            pt = rs.AddPoint((rec.pt_lst[i].x+rec.pt_lst[(i+1)%4].x)/2,(rec.pt_lst[i].y+rec.pt_lst[(i+1)%4].y)/2)
            text = str(i)
            all_text.append(text)
            all_point.append(pt)
        return all_text,all_point

    @staticmethod
    def displaypolyveclength(polyline):
        #根据一个多段线，输出gh中点的列表和向量的列表,和需要表现得长度得txt与点
        corner_list = [] #角点列表
        vector_list = [] #向量列表 
        txt_length = [] #长度txt列表
        median_point = [] #文字标记点得列表
        for i in range(0,len(polyline.vec_lst)):
            temp_point = polyline.pt_lst[i]
            temp_vec = polyline.vec_lst[i]
            corner_list.append(rs.CreatePoint(temp_point.x,temp_point.y,0))
            vector_list.append(rs.CreateVector(temp_vec.x,temp_vec.y,0))
            txt_length.append(str(temp_vec.getLength()))
            median_point.append(rs.CreatePoint(temp_point.x+temp_vec.x/2,temp_point.y+temp_vec.y/2,0))
        return corner_list,vector_list,txt_length,median_point
    


    @staticmethod
    def createPolyline(poly_gh):
        # 将gh的polyline转化成构造的polyline实例
        poly_pt_lst = rs.PolylineVertices(poly_gh)
        start_pt = Point2D([poly_pt_lst[0][0], poly_pt_lst[0][1]])
        vec_lst = []
        for i in range(len(poly_pt_lst)-1):
            pt1 = poly_pt_lst[i]; pt2 = poly_pt_lst[i+1]
            vec = Vector(pt2[0]-pt1[0], pt2[1]-pt1[1])
            vec_lst.append(vec)
        polyline = Polyline(start_pt, vec_lst)
        return polyline
    
    @staticmethod
    def creatrec(rec1):
        #输入一个gh里的矩形,输出矩形类
        rec1 = rs.PolylineVertices(rec1)
        origin_point1 = Point2D([rec1[0][0],rec1[0][1]])
        point1 = rec1[1]
        point_end = rec1[-2]
        vecx1 = Vector(point1[0]-origin_point1.x,point1[1]-origin_point1.y)
        vecy1 = Vector(point_end[0]-origin_point1.x,point_end[1]-origin_point1.y)
        vecx1_na = vecx1.reverse()
        vecy1_na = vecy1.reverse()
        now_rec1 = Rectangle(origin_point1, [vecx1,vecy1,vecx1_na,vecy1_na])
        return now_rec1

    @staticmethod
    def creatrecpoint(point):
        #输入gh的点类,返回一个point2D
        return Point2D(point[0],point[1])


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

    @staticmethod
    def convertRec(rects):
        # 将gh里的rectangle转换成起始点和四个向量
        start_pt = []
        vect = []
        for i in range (len(rects)):
            pt_lst = rs.PolylineVertices(rects[i])
            start_pt.append(pt_lst[0])
            vec = [[],[],[],[]]
            for z in range(4):
                ve = rs.CreateVector([ pt_lst[z+1][0]-pt_lst[z][0] , pt_lst[z+1][1]-pt_lst[z][1] , 0 ])
                vec[z].append(ve)
            vect.append(vec)
        vec_lst = []
        for i in range(len(rects)):
            for z in range(4):
                vec_lst = vect[i][z][0]

    @staticmethod
    def displayArrangeArchWithEdgePoly(poly_gh,
                                       area_lst, dist_lst,
                                       length_domain_left_lst, length_domain_right_lst,
                                       width_domain_left_lst, width_domain_right_lst,
                                       length_lst, width_lst, flag_lst,
                                       arrangeClass_lst):
        """
        展示根据地块边界多段线布置建筑
        @params:
        input:
            poly_gh: gh中的边界多段线
            area_lst: 每个建筑的面积列表
            dist_lst: 每个建筑的间距列表
            length_left(right)_domain_lst: 每个建筑的宽度值域区间左(右)列表
            width_left(right)_domain_lst: 每个建筑的深度值域区间左(右)列表
            length_lst: 每个建筑的宽列表
            width_lst: 每个建筑的深度列表
            flag_lst: 每个建筑先决定宽or深, 0->宽, 1->深
            arrangeClass_lst: 每个建筑排列性质, 0->出头就排到下一段满足的
        output:
            poly_gh_lst: 每个建筑在gh里的多段线
        """
        edge = GHDisplay.createPolyline(poly_gh)  # ?这里只是polyine, 不具备edge属性, 到时再改
        length_domain_lst = [Domain(length_domain_left_lst[i], length_domain_right_lst[i]) for i in range(len(length_domain_left_lst))]
        width_domain_lst = [Domain(width_domain_left_lst[i], width_domain_right_lst[i]) for i in range(len(width_domain_left_lst))]
        arch_lst = []
        for i in range(len(area_lst)):
            arch = Arch(area_lst[i], length_domain_lst[i], width_domain_lst[i], length_lst[i], width_lst[i], flag_lst[i], arrangeClass_lst[i])
            arch_lst.append(arch)
        poly_index_lst, poly_lengthToStart_lst = rectangleArrange.computeArchPosition(edge, dist_lst, arch_lst)
        # 建筑对象实例列表
        new_arch_lst = rectangleArrange.arrangeAllArchs(arch_lst, edge, poly_index_lst, poly_lengthToStart_lst)
        #print(arch_lst[0].area)
        #print(poly_index_lst)
        #print(poly_lengthToStart_lst)
        #print(new_arch_lst)
        # 转换成gh多段线实例
        poly_gh_lst = [GHDisplay.displayPolyline(arch) for arch in new_arch_lst]
        return poly_gh_lst
