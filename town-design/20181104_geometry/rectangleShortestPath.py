#!/usr/bin/env python
#-*- coding: utf-8 -*-

import geometry

# 已经判断好两个矩形各个角点的可见性
def findShortestPath(relation, edge_index1, length1, edge_index2, length2):
    # 把两个矩形的关系对象实例作为参数传入(关系对象只算一次), 计算得到两个矩形之间的最短路径
    path = None
    rec1, rec2 = relation.rec1, relation.rec2
    visiable_dict = relation.cornerVisiable_dict
    shortestPath_dict = relation.cornerShortestPath_dict

    corner1_a = edge_index1, corner2_a = edge_index2
    corner1_b = 0 if edge_index1 == 3 else edge_index1+1
    corner2_b = 0 if edge_index2 == 3 else edge_index2+1

    # 构造选择点的实例对象, 可在前面计算完性质和到各个角的路径
    # 考虑是否需要把选择点作为角点 ?
    pt1, pt2 = None, None
    if length1 == 0:                                  pt1 = rec1.pt_lst[corner1_a]
    elif length1 == rec1.vec_length_lst[edge_index1]: pt1 = rec1.pt_lst[corner1_b]
    else:                                             pt1 = RectangleEdgeCornerPoint(rec1, edge_index1, length1)

    if length2 == 0:                                  pt2 = rec2.pt_lst[corner2_a]
    elif length2 == rec2.vec_length_lst[edge_index2]: pt2 = rec2.pt_lst[corner2_b]
    else:                                             pt2 = RectangleEdgeCornerPoint(rec2, edge_index2, length2)

    isCorner_pt1, isCorner_pt2 = isinstance(pt1, RectangleCornerPoint), isinstance(pt2, RectangleCornerPoint)
    # 判断起点和终点之间的可见性
    isVisible = False
    if ((corner2_a in visiable_dict[corner1_a]) and (corner2_b in visiable_dict[corner1_a])
        and (corner2_a in visiable_dict[corner1_b]) and (corner2_b in visiable_dict[corner1_b])):
        isVisible = True
    if isVisible: # 如果可见的情况(老师True)
        # 得到可见点之间的路径
        if isCorner_pt1 and isCorner_pt2:   # 如果选择的两个点都位于角点, 直接选择路径
            path = shorestPath_dict[pt1.corner_index][pt2.corner_index]
        else:  # 不位于角点, 需要重新计算
            edgePt_vec = pt1.initVecBetweenPts(pt2)     # 矩形1指向指向矩形2角点的向量
            reverse_vec = edgePt_vec.reverse()          # 矩形2指向矩形1的向量
            
            phrase1, isParallel1 = Phrase.judgeVecWithPhrase(pt1, edgePt_vec)   # 已经抽象
            phrase2, isParallel2 = Phrase.judgeVecWithPhrase(pt2, reverse_vec)

            # 可抽象, 根据可见点的象限, 平行性, 指向性向量得到中间路径
            path = Phrase.getVisiablePathWithPhrase(pt1, pt2, phrase1, phrase2, isParallel1, isParallel2, edgePt_vec, reverse_vec)
    else:  # 无法直接可见的始末点
        # 得到起点和终点到各自矩形到可见端点的路径
        # 边上点到角点的距离, 抽象(但方向相反), 先不写, 先构造EdgePoint和CornerPoint类

        # 将中间路径(可见点之间的路径), 起点到端点的路径累加, 得到所有路径
        path_lst = []
        min_path, min_length = None, 2147483647  # 初始的最小距离为最大
        for corner1 in visiable_dict:
            for corner2_i in range(len(visiable_dict[corner1])):
                corner2 = visiable_dict[corner2_i]
                mid_path = shorestPath_dict[corner1][corner2_i]
                # 在这里讨论pt1 或者 pt2是角点的情况
                # 两个都是角点, 而且被可见性遍历到, 这是不可能的, 只存在一个角点
                if (isCorner_pt1 and corner1 == pt1.corner_index):
                    path_edge2 = pt2.cornerPath_dict[corner2][1]   # 矩形2 corner2角点出发到pt2的路径
                    path = mid_path.addPolylines([path_edge2])
                elif (isCorner_pt2 and corner2 == pt2.corner_index):
                    path_edge1 = pt1.cornerPath_dict[corner1][0]   # 矩形1边点(角点)出发到corner1角点路径
                    path = path_edge1.addPolylines([mid_path])
                else:
                    path_edge1 = pt1.cornerPath_dict[corner1][0]   # 矩形1边点(角点)出发到corner1角点路径
                    path_edge2 = pt2.cornerPath_dict[corner2][1]   # 矩形2 corner2角点出发到pt2的路径
                    path = path_edge1.addPolylines([mid_path, path_edge2])    # ? 实现addPolyline方法
                path_lst.append(path)
                # 比较路径, 选择距离最短的路径
                if path.length() < min_length:
                    min_path = path
                    min_length = path.length()

        path = min_path
    return path
