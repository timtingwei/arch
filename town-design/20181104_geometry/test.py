#!/usr/bin/env python
#-*- coding: utf-8 -*-
from geometry import Point2D, PointVec, Vector, VectorTwoPts, RectangleCornerPoint, RectangleEdgePoint, Phrase, Polyline, Rectangle, RectangleRelation, ReverseVector, Domain
from generate import Edge, Arch
from rectangleShortestPath import findShortestPath
import rectangleArrange


def constructNormalRec(start_pt_lst, length, width):
    start_pt = Point2D(start_pt_lst)
    vec_lst = []
    length_vec = Vector(length, 0.0)
    width_vec = Vector(0.0, width)
    vec_lst = [length_vec, width_vec, ReverseVector(length_vec), ReverseVector(width_vec)]
    rec = Rectangle(start_pt, vec_lst)
    #print("print(rec.vec_lst): ")
    #for vec in rec.vec_lst:
    #    print(vec)
    return rec

def constructNotNormalRecsSample1():
    start_pt1, start_pt2 = Point2D([-2.989484, 2.030411]), Point2D([-0.040854, -9.81334])
    vec_lst1 = [ Vector(4.523321,-1.382918), Vector(3.008505,9.840376), Vector(-4.523321,1.382918), Vector(-3.008505,-9.840376) ]
    vec_lst2 = [Vector(8.19364, 4.667886), Vector(-2.098816, 3.684097), Vector(-8.19364, -4.667886), Vector(2.098816, -3.684097)]
    rec1 = Rectangle(start_pt1, vec_lst1)
    rec2 = Rectangle(start_pt2, vec_lst2)
    return rec1, rec2

def constructNotNormalRecsSample3():
    start_pt1, start_pt2 = Point2D([900.447964935,239.278153979]), Point2D([3465.71194023,2299.56214292])
    vec_lst1 = [Vector(-760.288490508,514.115187156), Vector(-209.600807071,-309.963769207), Vector(760.288490508,-514.115187156), Vector(209.600807071,309.963769207) ]
    vec_lst2 = [Vector(-567.049662268,772.009549672), Vector(-393.991080522,-289.390862123), Vector(567.049662268,-772.009549672), Vector(393.991080522,289.390862123)]
    rec1 = Rectangle(start_pt1, vec_lst1)
    rec2 = Rectangle(start_pt2, vec_lst2)
    return rec1, rec2

def constructRelation(rec1, rec2):
    relation = RectangleRelation(rec1, rec2)

    """
    print('rec1, rec2:')
    print(relation.rec1, relation.rec2)
    print('relation.cornerVisiable_dict: ')
    print(relation.cornerVisiable_dict)
    print('relation.cornerShortestPath_dict: ')
    print(relation.cornerShortestPath_dict)
    print('relation.corner_vec_dict: ')
    print(relation.corner_vec_dict)

    print('')
    print('relation.isParallel: ')
    print(relation.isParallel)
    print('relation.gapClass: ')
    print(relation.gapClass)
    print('relation.gapDistance: ')
    print(relation.gapDistance)
    """

    """
    print('print(relation.cornerVisiable_dict): ')
    print(relation.cornerVisiable_dict)
    print('print(relation.cornerShortestPath_dict): ')
    for corner1 in relation.cornerVisiable_dict:
        for corner2_i in range(len(relation.cornerVisiable_dict[corner1])):
            corner2 = relation.cornerVisiable_dict[corner1][corner2_i]
            print(corner1, corner2)
            path = relation.cornerShortestPath_dict[corner1][corner2_i]
            print(path.vec_lst[0])
            print(path.vec_lst[1])
    """

    return relation

def testFindShortestPath(relation, edge_index1=0, length1=0.0, edge_index2=0, length2=0.0):
    #edge_index1 = 0; length1 = 3.5
    #edge_index2 = 1; length2 = 2.2
    path = findShortestPath(relation, edge_index1, length1, edge_index2, length2)
    #print('path: ')
    #print(path)
    print('path.keys: ')
    print(path.__dict__.keys())
    print('path.start_pt.x,y:')
    print(path.start_pt.x, path.start_pt.y)
    print('path.vec_lst: ')
    for vec in path.vec_lst:
        print(vec)

    print('len = ' + str(path.length))
    return path

def testRectangleCornerPoint():
    # getRectangleCornerPath()向量方向对应出
    rec1 = constructNormalRec([0.0, 4.0], 4.0, 3.0)
    pt = RectangleCornerPoint(rec1, 0)

def testRectangleCornerPoint(rec, index, length):
    pt = RectangleCornerPoint(rec, index)
    print('index = ' + str(index))
    print(pt.index_this, pt.index_before, pt.index_after, pt.index_cross)
    pt_edge = RectangleEdgePoint(rec, index, length)
    print('pt_edge: ')
    print(pt_edge.index_this, pt_edge.index_before, pt_edge.index_after, pt_edge.index_cross)

def arrangeRectangleWithEdgePoly():
    # 根据地块边界多段线布置建筑
    # 按矩形序得到的矩形间的最短路
    # num = 10
    # rec_lst = [None] * num       # 所有矩形列表
    rec1 = constructNormalRec([0.0, 4.0], 4.0, 3.0)
    rec2 = constructNormalRec([10.0, 0.0], 3.0, 5.0)
    rec3 = constructNormalRec([0.0, -3.0], 3.3, 2.33)
    rec4 = constructNormalRec([-1.5, -8.0], 4.4, 2.2)
    rec_lst = [rec1, rec2, rec3, rec4]
    edge_poly = None            # 地块边界


    path_lst = []
    for i in range(len(rec_lst)-1):
        rec1 = rec_lst[i]; rec2 = rec_lst[i+1]
        relation = constructRelation(rec1, rec2)
        path = findShortestPath(relation, edge_index1=0, length1=0.0, edge_index2=0, length2=0.0)
        path_lst.append(path)
    return path_lst
    
    


def testArrangeRectangleWithEdgePoly(edge, area_lst, length_domain_lst, width_domain_lst, dist_lst, length_lst, width_lst, flag_lst, arrangeClass_lst):
    #start_pt = Point2D([1.0, -2.0])
    #vec_lst = [Vector(10.0, 0.0), Vector(0.0, 15.0), Vector(10.0, 20.0), Vector(10.0, 0.0)]
    #edge = Edge(start_pt, vec_lst)
    #dist_lst = [1.2, 0.0, 0.0, 6.0, 4.0, 9.0]
    arch_lst = []
    for i in range(len(length_lst)):
        #arch = Arch(length=length_lst[i], width=width_lst[i], arrangeClass=arrangeClass_lst[i])
        arch = Arch(area_lst[i], length_domain_lst[i], width_domain_lst[i], length_lst[i], width_lst[i], flag_lst[i], arrangeClass_lst[i])
        arch_lst.append(arch)    
    poly_index_lst, poly_lengthToStart_lst = rectangleArrange.computeArchPosition(edge, dist_lst, arch_lst)
    print(arch_lst[0].area)
    print(poly_index_lst)
    print(poly_lengthToStart_lst)
    new_arch_lst = rectangleArrange.arrangeAllArchs(arch_lst, edge, poly_index_lst, poly_lengthToStart_lst)
    print(new_arch_lst)
    return

        
def main_shortestPath():
    # ZeroDivisionError: float division by zero
    #rec1 = constructNormalRec([0.0, 4.0], 4.0, 3.0)
    #rec2 = constructNormalRec([10.0, 0.0], 3.0, 5.0)
    #rec1, rec2 = constructNotNormalRecsSample1()
    # 矩形最短路径, 选择点为角点时报错
    rec1, rec2 = constructNotNormalRecsSample3()
    relation = constructRelation(rec1, rec2)
    #index = 3; length = 3
    #testRectangleCornerPoint(rec1, index, length)
    testFindShortestPath(relation, 0, 0.0, 3, 0.0)
    return

def main_arrangeRectangleWithEdgePoly():
    """
    start_pt = Point2D([1.0, -2.0])
    vec_lst = [Vector(10.0, 0.0), Vector(0.0, 15.0), Vector(10.0, 20.0), Vector(10.0, 0.0)]
    edge = Edge(start_pt, vec_lst)
    dist_lst = [1.2, 0.0, 0.0, 6.0, 4.0, 9.0]
    length_lst = [6.0, 3.0, 5.0, 2.2, 8.0, 3.0]
    width_lst =  [2.5, 2.5, 6.0, 2.5, 2.5, 2.5]
    arrangeClass_lst = [0, 0, 0, 0, 0, 0, 0]
    """
    start_pt = Point2D([0.0, 0.0])
    vec_lst = [Vector(13.0, 0.0)]
    edge = Edge(start_pt, vec_lst)
    dist_lst = [3.0, 0.0, 1.0, 1.0]
    area_lst = [5.2, 3.2, 4.3, 8.5]
    length_domain_lst = []
    width_domain_lst = []
    # 用左右值列表构造区间(轩总可以照这个思路自己设计下, edge同理)
    length_domain_left_lst =  [1.0, 2.0, 1.0, 2.0]
    length_domain_right_lst = [4.0, 6.0, 7.0, 6.0]
    width_domain_left_lst =  [1.0, 2.0, 1.0, 2.0]
    width_domain_right_lst = [4.0, 6.0, 7.0, 6.0]
    for i in range(len(length_domain_left_lst)):
        lenth_domain = Domain(length_domain_left_lst[i], length_domain_right_lst[i])
        width_domain = Domain(width_domain_left_lst[i], width_domain_right_lst[i])
        length_domain_lst.append(lenth_domain)
        width_domain_lst.append(width_domain)

    #length_domain_lst = [Domain(1.0, 4.0), Domain(2.0, 6.0), Domain(1.0, 7.0), Domain(2.0, 6.0)]
    #width_domain_lst = [Domain(1.0, 4.0), Domain(2.0, 6.0), Domain(1.0, 7.0), Domain(2.0, 6.0)]
    length_lst = [2.0, 2.0, 3.0, 2.0]
    width_lst =  [1.0, 2.0, 1.5, 1.5]
    flag_lst = [0, 1, 0, 1]
    arrangeClass_lst = [0, 0, 0, 0]
    # arch_lst = testArrangeRectangleWithEdgePoly(edge, dist_lst, length_lst, width_lst, arrangeClass_lst)
    arch_lst = testArrangeRectangleWithEdgePoly(edge, area_lst, length_domain_lst, width_domain_lst, dist_lst, length_lst, width_lst, flag_lst, arrangeClass_lst)
    return arch_lst

if __name__ == '__main__':
    #main_shortestPath()
    main_arrangeRectangleWithEdgePoly()
    
