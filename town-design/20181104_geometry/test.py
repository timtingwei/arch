#!/usr/bin/env python
#-*- coding: utf-8 -*-
from geometry import Point2D, PointVec, Vector, VectorTwoPts, RectangleCornerPoint, RectangleEdgePoint, Phrase, Polyline, Rectangle, RectangleRelation, ReverseVector
from rectangleShortestPath import findShortestPath

def constructNormalRec(start_pt_lst, length, width):
    start_pt = Point2D(start_pt_lst)
    vec_lst = []
    length_vec = Vector(length, 0.0)
    width_vec = Vector(0.0, width)
    vec_lst = [length_vec, width_vec, ReverseVector(length_vec), ReverseVector(width_vec)]
    rec = Rectangle(vec_lst, start_pt)
    #print("print(rec.vec_lst): ")
    #for vec in rec.vec_lst:
    #    print(vec)
    return rec

def constructNotNormalRecsSample1():
    start_pt1, start_pt2 = Point2D([-2.989484, 2.030411]), Point2D([-0.040854, -9.81334])
    vec_lst1 = [ Vector(4.523321,-1.382918), Vector(3.008505,9.840376), Vector(-4.523321,1.382918), Vector(-3.008505,-9.840376) ]
    vec_lst2 = [Vector(8.19364, 4.667886), Vector(-2.098816, 3.684097), Vector(-8.19364, -4.667886), Vector(2.098816, -3.684097)]
    rec1 = Rectangle(vec_lst1, start_pt1)
    rec2 = Rectangle(vec_lst2, start_pt2)
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

def testFindShortestPath(relation):
    #edge_index1 = 0; length1 = 3.5
    #edge_index2 = 1; length2 = 2.2
    path = findShortestPath(relation, edge_index1=0, length1=0.0, edge_index2=0, length2=0.0)
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

def testArrangeRectangleWithEdgePoly():
    path_lst = arrangeRectangleWithEdgePoly()
    print('path_lst: ')
    print(path_lst)
        
        
def main():
    # ZeroDivisionError: float division by zero
    rec1 = constructNormalRec([0.0, 4.0], 4.0, 3.0)
    rec2 = constructNormalRec([10.0, 0.0], 3.0, 5.0)
    #rec1, rec2 = constructNotNormalRecsSample1()
    relation = constructRelation(rec1, rec2)
    #index = 3; length = 3
    #testRectangleCornerPoint(rec1, index, length)
    testFindShortestPath(relation)
    return


if __name__ == '__main__':
    #main()
    #testRectangleCornerPoint()
    testArrangeRectangleWithEdgePoly()
    
