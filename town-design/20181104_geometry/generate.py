#!/usr/bin/env python
#-*- coding: utf-8 -*-
#关于设计驱动对象的描述和算法
import geometry

class Arch(geometry.Rectangle):
    '建筑对象构造'
    """
    #通过宽深来构造矩形
    def __init__(self, length = None, width = None, arrangeClass = 0, area = None):
        self.length, self.width = length, width    # 建筑长宽
        # start_pt, vec_lst, vec_length_lst, pt_lst, phrase_lst, cornerYinYangProperty_lst
        self.arrangeClass = arrangeClass     # 建筑的沿边界分布的分配方式(0是建筑垂线不会有超过poly部分)
        return
    """
    def __init__(self, area, length_domain, width_domain, length, width, flag, arrangeClass=0):
        self.area = area
        self.length_domain, self.width_domain = length_domain, width_domain
        self.length, self.width = self.convertArea(area, length_domain, width_domain, length, width, flag)
        self.arrangeClass = arrangeClass    # 建筑的沿边界分布的分配方式(0是建筑垂线不会有超过poly部分)
        return

    def fillArchWithRectangle(self, start_pt, vec_lst):
        # 用起始点和向量填充当前arch实例
        super(Arch, self).__init__(start_pt, vec_lst)
        return

    """
    def limit(self, length, length_domain):
        # 把长度限制在值域范围内
        length = length_domain[0] if length < length_domain[0] else (length_domain[1] if length > length_domain[1] else length)
        return length
    """


    def recomputeDomain(self, area, length_domain, width_domain):
        # 根据面积, 对宽深范围重新计算, 得到在限制一次后, 不会超出的范围
        # 注释掉的会改变区间对象实例
        length_left, length_right = length_domain.left, length_domain.right
        width_left, width_right = width_domain.left, width_domain.right
        l_d1 = area/width_domain.right  # 得到最大深时的最小宽
        l_d2 = area/width_domain.left  # 得到最小深时的最大宽
        #if l_d1 > length_domain.left: length_domain.left = l_d1
        #if l_d2 < length_domain.right: length_domain.right = l_d2
        if l_d1 > length_domain.left: length_left = l_d1
        if l_d2 < length_domain.right: length_right = l_d2

        l_w1 = area/length_domain.right  # 得到最大宽时的最小深
        l_w2 = area/length_domain.left  # 得到最小宽时的最大深
        #if l_w1 > width_domain.left: width_domain.left = l_w1
        #if l_w2 < width_domain.right: width_domain.right = l_w2
        if l_w1 > width_domain.left: width_left = l_w1
        if l_w2 < width_domain.right: width_right = l_w2
        new_length_domain = geometry.Domain(length_left, length_right)
        new_width_domain = geometry.Domain(width_left, width_right)
        return new_length_domain, new_width_domain


    # 结合面积转宽深的机制
    def convertArea(self, area, length_domain, width_domain, length, width, flag):
        """
        给定面积, 宽深范围, 改变宽深中的一个值, 确定另外一个值
        @params:
        area: 面积 float
        length_domian: 宽值范围 float[2]
        width_domain: 深值范围 float[2]
        length:   宽度 float
        width:    深度 float
        flag:     当前确定的是宽还是深度, 1 -> 宽, 0 -> 深
        """
        area = float(area)  # ? 如何定义好呢
        length_domian, width_domain = self.recomputeDomain(area, length_domain, width_domain)
        # 修改实例属性
        self.length_domain, self.width_domain = length_domain, width_domain
        if flag:
            #length = limit(length, length_domain)
            length = length_domain.limitInDomain(length)
            width = area / length
        else:
            #width = limit(width, width_domain)
            width = width_domain.limitInDomain(width)
            length = area / width
        return length, width

class Edge(geometry.Polyline):
    '地块边界对象构造'
    def __init__(self, start_pt, vec_lst):
        super(Edge, self).__init__(start_pt, vec_lst)
        self.edgeProperty_lst = []     # 边界性质

class Road(geometry.Polyline):
    '道路对象描述'
    def __init__(self, start_pt, vec_lst):
        super(Road, self).__init__(start_pt, vec_lst)
        self.max_flow = 0.0    # 这条路的最大人流量
        return

class Block(object):
    '地块对象描述'
    def __init__(self, edge_poly):
        self.edge_poly = edge_poly     # 地块边界
        return

class GroupBlock(geometry.Rectangle):
    '非正交区块对象描述'
    def __init__(self, parent_block):
        self.parent_block = parent_block    # 区块所属父地块
        return

class ArchGroup(object):
    '建筑组团对象描述'
    def __init__(self, child_arch_lst):
        self.child_arch_lst = child_arch_lst    # 该组团所拥有的建筑列表
        return
    
class Rigid(geometry.Rectangle):
    '在区块中包含建筑的刚体对象描述'
    def __init__(self, parent_groupBlock, child_arch):
        self.parent = parent_groupBlock   # 所属的组团
        self.child = child_arch           # 包含的建筑
        self.x_domain, self.y_domain = self.computeRigidDomain()
        return

    def computeRigidDomain(self):
        # 计算存放矩形的刚体, 在区块中的位置, 从0角点开始算
        x_domain, y_domain = None
        # 如果已经是平行于父矩形边界:
        # 如果不平行
        return x_domain, y_domain
