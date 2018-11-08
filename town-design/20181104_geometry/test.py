#!/usr/bin/env python
#-*- coding: utf-8 -*-
from geometry import Point2D, PointVec, Vector, VectorTwoPts, RectangleCornerPoint, RectangleEdgePoint, Phrase, Polyline, Rectangle, RectangleRelation
from rectangleShortestPath import findShortestPath

def constructNormalRec(start_pt_lst, length, width):
    start_pt = Point2D(start_pt_lst)
    vec_lst = []
    length_vec = Vector(length, 0.0)
    width_vec = Vector(0.0, width)
    vec_lst = [length_vec, width_vec, length_vec.reverse(), width_vec.reverse()]
    rec = Rectangle(vec_lst, start_pt)
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

    return relation

def testFindShortestPath(relation):
    edge_index1 = 0; length1 = 3.5
    edge_index2 = 1; length2 = 2.2
    path = findShortestPath(relation, edge_index1, length1, edge_index2, length2)
    print('path: ')
    print(path)
    return path



def main():
    # ZeroDivisionError: float division by zero
    #rec1 = constructNormalRec([0.0, 4.0], 4, 3)
    #rec2 = constructNormalRec([10.0, 0.0], 3, 5)

    rec1, rec2 = constructNotNormalRecsSample1()
    relation = constructRelation(rec1, rec2)
    #testFindShortestPath(relation)
    return
if __name__ == '__main__':
    main()
    
