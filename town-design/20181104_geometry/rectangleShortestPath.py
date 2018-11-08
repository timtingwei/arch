#!/usr/bin/env python
#-*- coding: utf-8 -*-
import pdb
from geometry import RectangleCornerPoint, RectangleEdgePoint, Polylines, ReverseVector, VectorTwoPts, Phrase

# 已经判断好两个矩形各个角点的可见性
def findShortestPath(relation, edge_index1, length1, edge_index2, length2):
    # 把两个矩形的关系对象实例作为参数传入(关系对象只算一次), 计算得到两个矩形之间的最短路径
    path = None
    rec1, rec2 = relation.rec1, relation.rec2
    cornerVisiable_dict = relation.cornerVisiable_dict
    cornerShortestPath_dict = relation.cornerShortestPath_dict

    corner1_a = edge_index1; corner2_a = edge_index2
    corner1_b = 0 if edge_index1 == 3 else edge_index1+1
    corner2_b = 0 if edge_index2 == 3 else edge_index2+1

    # 构造选择点的实例对象, 可在前面计算完性质和到各个角的路径
    # 考虑是否需要把选择点作为角点 考虑
    pt1, pt2 = None, None
    if length1 == 0:                                  pt1 = rec1.pt_lst[corner1_a]
    elif length1 == rec1.vec_length_lst[edge_index1]: pt1 = rec1.pt_lst[corner1_b]
    else:                                             pt1 = RectangleEdgePoint(rec1, edge_index1, length1)

    if length2 == 0:                                  pt2 = rec2.pt_lst[corner2_a]
    elif length2 == rec2.vec_length_lst[edge_index2]: pt2 = rec2.pt_lst[corner2_b]
    else:                                             pt2 = RectangleEdgePoint(rec2, edge_index2, length2)

    isCorner_pt1, isCorner_pt2 = isinstance(pt1, RectangleCornerPoint), isinstance(pt2, RectangleCornerPoint)
    isVisible = False; flag1 = False
    if isCorner_pt1 and isCorner_pt2:
        flag1 = True
        index =  0
        for i in cornerVisiable_dict[pt1.corner_index]:
            if pt2.corner_index == i:
                isVisible = True; index = i; break;
    else:
        # 至少有一个边点的情况
        edgePt_vec = VectorTwoPts(pt1, pt2)         # 矩形1指向指向矩形2角点的向量
        reverse_vec = ReverseVector(edgePt_vec)     # 矩形2指向矩形1的向量
        phrase1, isParallel1 = Phrase.judgeVecWithPhrase(pt1, edgePt_vec)   # 已经抽象
        phrase2, isParallel2 = Phrase.judgeVecWithPhrase(pt2, reverse_vec)

        isVisible = True if phrase1 and phrase2 else False
    
    if isVisible == True:  # 如果可见, 索引路径
        if flag1:  # 两个都是角点标记
            path = cornerShortestPath_dict[pt1.corner_index][index]
        else:   # 至少一个边点的情况
            path = Phrase.getVisiablePathWithPhrase(pt1, pt2, phrase1, phrase2, isParallel1, isParallel2, edgePt_vec, reverse_vec)
    else:  # 如果不可见, 角点到可见角点路径
        path_lst = []  # 储存所有路径
        min_path, min_length = None, 2147483647  # 初始的最小距离为最大
        for corner1 in cornerVisiable_dict:
            for corner2_i in range(len(cornerVisiable_dict[corner1])):
                corner2 = cornerVisiable_dict[corner1][corner2_i]
                merge_path_lst = []
                mid_path = cornerShortestPath_dict[corner1][corner2_i]
                if isCorner_pt1 and corner1 == pt1.corner_index:  # 端点就是pt1
                    edge2_path = pt2.cornerPath_dict[corner2][1]    # 进2
                    merge_path_lst = [mid_path, merge_path_lst]
                elif isCorner_pt2 and corner2 == pt2.corner_index:  # 端点就是pt2
                    edge1_path = pt1.cornerPath_dict[corner1][0]    # 出1
                    merge_path_lst = [edge1_path, mid_path]
                else:
                    edge1_path = pt1.cornerPath_dict[corner1][0]    # 出1
                    edge2_path = pt2.cornerPath_dict[corner2][1]    # 进2
                    merge_path_lst = [edge1_path, mid_path, edge2_path]
                temp_path = Polylines(merge_path_lst)
                #path_lst.append(temp_path)
                # 比较路径, 选择距离最短的路径
                if temp_path.length < min_length:
                    min_path = temp_path
                    min_length = temp_path.length
        path = min_path  # 选择最小路径作为最终路径
    return path
