#!/usr/bin/env python
#-*- coding: utf-8 -*-
import math

class Point2D(object):
    def __init__(self, coordinate):
        self.x, self.y = coordinate
        return
    def addVec(self, vec):
        return Point2D([self.x + vec.x, self.y + vec.y])

class PointVec(Point2D):
    '向量点构造'
    """
    def __init__(self, coordinate, vec_lst):
        self.pt = Point2D(coordinate)
        self.vec_lst = vec_lst
    """

    def __init__(self, pt, vec_lst):
        self.x, self.y = pt.x, pt.y
        self.vec_lst = vec_lst
        self.phrase_lst = []                      # 所有象限(根据矩形)
        self.isValidPhrase_lst = []               # 象限的有效性(根据矩形)

    @staticmethod
    def rayrayIntersect(pt1,vec1,pt2,vec2):
        #(暂时定义为静态方法)
        #分别给定两条射线的起始点与向量,得到交点,注意输入的不能是平行或共线的射线
        a, b, c, d = pt1.x, pt1.y, pt2.x, pt2.y
        x1, y1, x2, y2 = vec1.x, vec1.y, vec2.x, vec2.y
        t2 = (c*y1-ay1-dx1+bx1)/(y2*x1-x2*y1)
        pt = Point2D([c+x2*t2,d+y2*t2])
        return pt

    @staticmethod
    def minAngleVector(phase1, phase2, veca, vecb):
        #得到最小角度的向量
        #获取各个象限的向量
        vec1, vec2, vec3, vec4 = phase1.start_vec, phase1.end_vec, phase2.start_vec, phase2.end_vec
        #这里需要调用求向量长度的方法
        vec_list = [vec1,vec2,vec3,vec4]
        vec1_len, vec2_len, vec3_len, vec4_len = vec1.length, vec2.length, vec3.length, vec4.length
        k_2, k_3, k_4 = vec1_len/vec2_len, vec1_len/vec3_len, vec1_len/vec4_len
        #下面需要用到向量的点积算法
        angle_a1 = veca.dot(vec1)
        angle_a2 = k_2*veca.dot(vec2)
        angle_b3 = k_3*vecb.dot(vec3)
        angle_b4 = k_4*vecb.dot(vec4)
        #找到最小的角度以及对应的vector
        angle_list = [angle_a1,angle_a2,angle_b3,angle_b4]
        min_angle = angle_a1
        min_index = 0
        min_index_other = 0
        for i in range(1,4):
            if angle_list[i] < min_angle:
                min_angle = angle_list[i]
                min_index = i
        #下面需要用到向量的叉积算法
        cross_a1 = veca.cross(vec1)
        cross_a2 = veca.cross(vec2)
        cross_b3 = vecb.cross(vec3)
        cross_b4 = vecb.cross(vec4)
        cross_list = [cross_a1,cross_a2,cross_b3,cross_b4]
        #找到最小角度向量对应的另一边的向量
        if i <= 1:
            if cross_list[i] * cross_list[2] < 0:
                min_index_other = 2
            else:
                min_index_other = 3
        else:
            if cross_list[i] * cross_list[0] < 0:
                min_index_other = 0
            else:
                min_index_other = 1
        #最后按照phase1，phase2的顺序输出向量
        if min_index > min_index_other:
            return vec_list[min_index_other],vec_list[min_index]
        else:
            return vec_list[min_index],vec_list[min_index_other]


class Vector(object):
    def __init__(self, vec_x, vec_y, length = None):
        self.x, self.y = vec_x, vec_y
        self.length = self.getLength() if (length is None) else length
        return
    def unit(self):
        # 单位化一个向量
        return Vector(self.x/self.length, self.y/self.length, length = 1.0)

    def amplify(self, factor):
        # 向量扩大倍数
        return Vector(self.x * factor, self.y * factor, length = self.length * factor)

    def dot(self, vec):
        # 向量的点积
        return self.x*vec.x+self.y*vec.y

    def cross(self,vec):
        #向量的叉积
        return self.x*vec.y-self.y*vec.x

    def reverse(self):
        # 取反向量
        return Vector(-self.x, -self.y, length = self.length)  # 传值, 不会重新计算长度

    def getLength(self):
        # 向量的长度
        return math.sqrt(self.x * self.x + self.y * self.y)

    def isVectorParallel(self, vec):
        # 判断实例向量和vec之间是否平行
	if self.cross(self, vec) == 0: return True
	else: return False

class VectorTwoPts(Vector):
    '两点向量构造'
    def __init__(self, start_pt, end_pt):
        self.x, self.y = end_pt.x - start_pt.x, end_pt.y - start_pt.y
        self.length = self.getLength()        # 向量长度, 调用父类的求长度方法
        return

class RectangleCornerPoint(PointVec):
    '矩形角上 向量点构造'
    def __init__(self, rec, corner_index):
        # 将一个普通的点, 根据矩形角点编号构造成向量角点
        self.x, self.y = rec.pt_lst[corner_index].x, rec.pt_lst[corner_index].y
        self.vec_lst = rec.pt_lst[corner_index].vec_lst
        self.phrase_lst = rec.phrase_lst               # 向量点的象限和矩形的相同
        self.isValidPhrase_lst = [True]*4              # 向量点的有效性
        self.isValidPhrase_lst[corner_index] = False   # 当前角点面向的象限无效

        self.rec = rec                                 # 所属于的矩形
        self.corner_index = corner_index               # 所在矩形的角点编号
        self.cornerPath_dict =  self.getRectangleCornerPath()  # 角点到各个角点的向量
        return

    def getRectangleCornerPath(self):
        # 获得矩形内部角点到各个角点的路径(向量序)
        cornerPath_dict = {}   # 构造还需要根据计算确定下
        before = 3 if self.corner_index == 0 else self.corner_index-1  # 是否需要记录属性
        after = 0 if self.corner_index == 3 else self.corner_index+1
        cross = 0 if after == 3 else after+1
        # 不记录到本点的长度
        cornerPath_dict[before] = [Polyline(self, [self.rec.vec_lst[after]]),
                                   Polyline(self.rec.pt_lst[before], [self.rec.vec_lst[cross]])]
        cornerPath_dict[after] = [Polyline(self, [self.rec.vec_lst[self.corner_index]]),
                                  Polyline(self.rec.pt_lst[after], [self.rec.vec_lst[cross]])]
        cornerPath_dict[cross] = [Polyline(self, [self.rec.vec_lst[self.corner_index], self.rec.vec_lst[after]]),
                                  Polyline(self.rec.pt_lst[cross], [self.rec.vec_lst[before], self.rec.vec_lst[cross]])]
        return cornerPath_dict

class RectangleEdgePoint(PointVec):
    '矩形边上 向量点构造'
    def __init__(self, rec, edge_index, length):
        # 将一个普通的点, 根据矩形的边号构造成向量点
        # 根据编号和长度得到坐标x, y
        pt = rec.pt_lst[edge_index]
        length_vec = rec.vec_lst[edge_index].unit().amplify(length)
        new_pt = pt.addVec(length_vec)
        self.x, self.y = new_pt.x, new_pt.y
        
        self.phrase_lst = rec.phrase_lst               # 向量点的象限和矩形的相同
        self.isValidPhrase_lst = [True]*4              # 向量点的有效性
        index = 0 if edge_index == 3 else edge_index + 1
        self.isValidPhrase_lst[edge_index] = False     # 边缘点面向的象限无效
        self.isValidPhrase_lst[index] = False          # 边缘点面向的象限无效

        self.rec = rec                                 # 该点所属的矩形
        self.edge_index = edge_index                   # 所在矩形的边号
        self.corner_start_length_vec = length_vec            # 边上点到该边头点的向量(带长度)
        self.corner_end_length_vec = length_vec.reverse()    # 边上点到该边尾的向量(带长度)
        self.cornerPath_dict = {}                              # 该边缘点到各个角点的路径 {1: [p1, r_p1]}
        self.cornerPath_dict = self.getRectangleEdgeToCornerPath()
        return


    def getRectangleEdgeToCornerPath(self):
        # 得到边上到各个角点的路径, (所有路径放在字典里, 每一个对应有两条, [边点到角点的polyline, 角点到边点的polyline])
        cornerPath_dict = {0:[], 1:[], 2:[], 3:[]}
        path_a_vec = self.corner_start_length_vec.reverse()
        path_b_vec = self.corner_end_length_vec.reverse()
        a = self.edge_index
        b = 0 if a == 3 else a+1
        after_b = 0 if b == 3 else b+1
        before_a = 0 if after_b == 3 else after_b+1

        cornerPath_dict[a] = [Polyline(self, [path_a_vec]),
                            Polyline(self.rec.pt_lst[a], [self.corner_start_length_vec])]
        cornerPath_dict[b] = [Polyline(self, [self.corner_end_length_vec]),
                            Polyline(self.rec.pt_lst[b], [path_b_vec])]
        cornerPath_dict[after_b] = [Polyline(self, [self.corner_end_length_vec, self.rec.vec_lst[b]]),
                                  Polyline(self.rec.pt_lst[after_b], [self.rec.vec_lst[before_a], path_b_vec])]
        cornerPath_dict[before_a] = [Polyline(self, [path_a_vec, self.rec.vec_lst[b]]),
                                   Polyline(self.rec.pt_lst[before_a], [self.rec.vec_lst[before_a], self.corner_start_length_vec])]
        return cornerPath_dict
        
class Point3D(Point2D):
    def __init__(self, coordinate):
        self.x, self.y, self.z = coordinate
        return

class Phrase(object):
    '象限对象'
    def __init__(self, start_vec, end_vec):
        self.start_vec = start_vec  # 起始向量
        self.end_vec = end_vec      # 结束向量
        return
    
    def isFolde(self, vec):
        # 给定一个向量，判断是否被象限两个向量两个相夹
        # 返回1就是相夹,0就是不相夹,-1就是共线
        rst = 0
        vectora, vectorb, vectorc = self.start_vec, self.end_vec, vec
        #cross_product1 = (vectora[0]*vectorb[1])-(vectora[1]*vectorb[0])
        #cross_product2 = (vectora[0]*vectorc[1])-(vectora[1]*vectorc[0])
        cross_product1 = vectora.cross(vectorb)
        cross_product2 = vectora.cross(vectorc)
        cross_product = cross_product1*cross_product2
        if cross_product > 0:   #叉积相乘大于0
            rst = 0
        else:
            #dot_product1 = (vectora[0]*vectorb[0])+(vectora[1]*vectorb[1])
            dot_product1 = vectora.dot(vectorb)
            if dot_product1 > 0:    # 在点积大于零的情况下，判断是否共线
                if cross_product == 0: rst = -1   # 共线
                else: rst = 1      # 相互夹
            else: rst = 0          # 如果点积小于零，不相夹
        return rst

    @staticmethod
    def judgeVecWithPhrase(pt, flode_vec):
        # 找到有效象限, 并判断向量与象限的两个向量是否存在平行
        phrase, isParallel = None, False
        for pi in range(4):
            if pt.isValidPhrase_lst[pi] == True:
                isf_rst = pt.phrase_lst[pi].isFlode(flode_vec)
                if isf_rst:
                    phrase = pt.phrase_lst[pi]
                    if isf_rst == -1: isParallel = True
                    break;
        return phrase, isParallel

    @staticmethod
    def getVisiablePathWithPhrase(pt1, pt2, phrase1, phrase2, isParallel1, isParallel2, flode_vec, reverse_vec):
        # 根据可见点的象限, 平行性, 指向性向量得到中间路径
        # 也许可以建立两个点的关系对象实例(结构上的优化)
        # 也许中间点的可根据角点来判断路径选择的向量(计算上的优化, 仍要建立在结构上)
        path = None
        if isParallel1 or isParallel2:
            path = Polyline(pt1, [flode_vec])
        else:
            min_vec1, min_vec2 = PointVec.minAngleVector(phrase1, phrase2, flode_vec, reverse_vec)
            mid_pt = PointVec.rayrayIntersect(pt1,min_vec1,pt2,min_vec2)  # 两个射线交点
            path_vec1 = VectorTwoPts(pt1, mid_pt)   # 两点构造有长度的向量
            path_vec2 = VectorTwoPts(mid_pt, pt2)
            path = Polyline(pt1, [path_vec1, path_vec2])  # 起始点和向量序构造一个Polyline实例
        return path

class Polyline(object):
    '多段线构造'
    def __init__(self, start_pt, vec_lst):
        self.start_pt = start_pt
        self.vec_lst = vec_lst
        self.pt_lst = self.getPointListFromVecs()
        self.length = self.getLength()
        self.cornerYinYangProperty_lst = self.getYinYangProperty()

    def getLength(self):
        # 返回polyline的每段向量长度和
        length = 0.0
        for vec in vec_lst:
            length += vec.length
        return length

    def getPointListFromVecs(self):
        # 根据向量序得到点
        return

    def getVectorListFromPts(self):
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

    def addPolylines(self, polys):
        # polys: 与之合并的其他顺序多段线list
        new_polyline = None
        return new_polyline
    

class Rectangle(Polyline):
    def __init__(self, vec_lst, start_pt):
        self.start_pt = start_pt
        self.vec_lst = vec_lst
        self.vec_length_lst = self.getVectorLengthList()
        self.pt_lst = self.getPtListFromVectors()
        self.phrase_lst = self.getFourPhrase()
        self.pt_lst = self.revisePtToPtVec()    # 根据象限和向量得到角点向量点
        self.cornerYinYangProperty_lst = [1, 1, 1, 1]

    def getVectorLengthList(self):
        # 根据所有向量将长度写入矩形实例属性
        num = len(self.vec_lst)
        length_lst = [0.0]*num
        for i in range(num):
            length_lst[i] = self.vec_lst[i].length
        return length_lst
            

    def getPtListFromVectors(self):
        # 根据初始点和所有向量得到所有点, 将角点记录成向量位点
        pt_lst = []
        pt_lst.append(self.start_pt)
        temp_pt = self.start_pt
        for vec in self.vec_lst[:-1]:
            temp_pt = temp_pt.addVec(vec)
            pt_lst.append(temp_pt)
        return pt_lst

    def getFourPhrase(self):
        # 根据x轴和y轴线得到四个象限
        vec_x, vec_y = self.vec_lst[0], self.vec_lst[1]
        rev_x, rec_y = vex_x.reverse(), vec_y.reverse()
        p1 = Phrase(vec_x, vex_y)
        p2 = Phrase(vec_y, rev_x)
        p3 = Phrase(rev_x, rev_y)
        p4 = Phrase(rev_y, vec_x)
        phrase_lst = [p1, p2, p3, p4]
        return phrase_lst

    def revisePtToPtVec(self):
        # 根据象限和向量修改普通角点为角点向量点
        corner_pt_lst = []
        for i in range(len(self.pt_lst)):
            corner_pt_lst.append(RectangleCornerPoint(self, i))  # 替换成角点的实例对象
            #corner_pt_lst.append(pt_lst[i].initPointVec_rectangle_corner(self, i))
        return corner_pt_lst

        
class RectangleRelation(object):
    ' 两个矩形的关系对象 '
    def __init__(self, rec1, rec2):
        self.rec1, self.rec2 = rec1, rec2
        self.cornerVisiable_dict = {}             # 矩形各角点间的可见性
        self.cornerShortestPath_dict  = {}        # 矩形各角点间的路径
        self.corner_vec_dict = {}                  # 矩形角点间连线
        self.cornerVisiable_dict, self.cornerShortestPath_dict, self.corner_vec_dict = getCornerVisiableAndPath()
        
        self.isParallel = judgeParallel()    # 矩形是否平行
        self.gapClass = getGapClass()        # 矩形间距分类
        self.gapDistance = getGapDistance()  # 矩形间距

        return

    def getCornerVisiableAndPath(self):
        # 计算矩形各个角点的可见性
        visiable_dict = {0:[], 1:[], 2:[], 3:[]}
        path_dict = {0:[], 1:[], 2:[], 3:[]}
        corner_vec_dict = {0:{}, 1:{}, 2:{}, 3:{}}
        for i in range(4):
            # 矩形1的四个角点序号
            for j in range(4):
                # 矩形2的四个角点序号
                pt1 = rec1.pt_lst[i], pt2 = rec2.pt_lst[j]  # 矩形对应计算的角向量点
                corner_vec = VectorTwoPts(pt1, pt2)         # 矩形1指向指向矩形2角点的向量
                corner_vec_dict[i][j] = corner_vec          # 添加两个角点之间的向量
                reverse_vec = corner_vec.reverse()          # 矩形2指向矩形1的向量
                isVisible = False
                
                phrase1, isParallel1 = Phrase.judgeVecWithPhrase(pt1, corner_vec)   # 已经抽象
                phrase2, isParallel2 = Phrase.judgeVecWithPhrase(pt2, reverse_vec)
                """
                phrase1, phrase2, parallel1, parallel2 = None, None, False, False
                for pi in range(4):
                    if pt1.isValidPhrase[pi] == True:
                        isf_rst = pt1.phrase_lst[pi].isFloder(corner_vec)
                        if isf_rst:
                            phrase1 = pt1.phrase_lst[pi]
                            if isf_rst == -1: parallel1 = True
                            break;
                for pi in range(4):
                    if pt2.isValidPhrase[pi] == True:
                        isf_rst = pt2.phrase_lst[pi].isFloder(reverse_vec)
                        if isf_rst:
                            phrase2 = pt2.phrase_lst[pi]
                            if isf_rst == -1: parallel2 = True
                            break;
                """
                if phrase1 and phrase2 : isVisible = True
                if not isVisible: continue       # 其中有一个角点被挡住
                visiable_dict[i].append(j)       # 添加可见性
                # 可抽象, 根据可见点的象限, 平行性, 指向性向量得到中间路径
                path = Phrase.getVisiablePathWithPhrase(pt1, pt2, phrase1, phrase2, isParallel1, isParallel2, corner_vec, reverse_vec)
                """
                if parallel1 or parallel2:
                    path = Polyline(pt1, [corner_vec])
                else:
                    min_vec1, min_vec2 = PointVec.minAngleVector(phrase1, phrase2, corner_vec, reverse_vec)
                    mid_pt = PointVec.rayrayIntersect(pt1,min_vec1,pt2,min_vec2)  # 两个射线交点
                    path_vec1 = VectorTwoPts(pt1, mid_pt)
                    path_vec2 = VectorTwoPts(mid_pt, pt2)
                    path = Polyline(pt1, [path_vec1, path_vec2])
                """
                path_dict[i][j] = path

        return visiable_dict, path_dict, corner_vec_dict

    def isParallel(self):
        # 根据向量计算两个矩形是否平行
        parallel = False
        if self.rec1.vec_lst[0].isVectorParallel(self.rec2.vec_lst[0]) == True:
	    parallel = True
        return parallel

    def getGapClass(self):
        # 判断两个矩形间距是属于哪种类型: 角对角, 边对边, 边对角
        gapClass = 0
        return gapClass

    def getGapDistance(self):
        # 根据矩形间距位置, 计算两个矩形之间的间距
        distance = 0
        return distance
        
