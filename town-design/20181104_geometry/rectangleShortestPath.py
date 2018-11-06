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

    # 判断起点和终点之间的可见性
    corner1_a = edge_index1, corner2_a = edge_index2
    corner1_b = 0 if edge_index1 == 3 else edge_index1+1
    corner2_b = 0 if edge_index2 == 3 else edge_index2+1
    isVisible = False
    if ((corner2_a in visiable_dict[corner1_a]) and (corner2_b in visiable_dict[corner1_a])
        and (corner2_a in visiable_dict[corner1_b]) and (corner2_b in visiable_dict[corner1_b])):
        isVisible = True
    if isVisible: # 如果可见的情况(老师True)
        # 得到可见点之间的路径
        if ((length1 == 0 or length1 == rec1.vec_length_lst[edge_index1]) and
            (length2 == 0 or length2 == rec2.vec[edge_index2])):  # 位于角点, 可以直接索引
            if length1 == 0:
                if length2 == 0: path = shorestPath_dict[corner1_a][corner2_a]
                else:            path = shorestPath_dict[corner1_a][corner2_b]
            else:
                if length2 == 0: path = shorestPath_dict[corner1_b][corner2_a]
                else:            path = shorestPath_dict[corner1_b][corner2_b]
        else:  # 不位于角点, 需要重新计算
            pt1, pt2 = Point2D(), Point2D()
            pt1 = initPointVec_rectangle_edge(rec1, edge_index1)
            pt2 = initPointVec_rectangle_edge(rec2, edge_index2)  # ? 构造函数重写

            # 可抽象
            edgePt_vec = pt1.initVecBetweenPts(pt2)     # 矩形1指向指向矩形2角点的向量
            reverse_vec = edgePt_vec.reverse()          # 矩形2指向矩形1的向量
            isVisible = False
            phrase1, phrase2, parallel1, parallel2 = None, None, False, False
            for pi in range(4):
                if pt1.isValidPhrase[pi] == True:
                    isf_rst = pt1.phrase_lst[pi].isFlode(edgePt_vec)
                        if isf_rst:
                            phrase1 = pt1.phrase_lst[pi]
                            if isf_rst == -1: parallel1 = True
                            break;
            for pi in range(4):
                if pt2.isValidPhrase[pi] == True:
                    isf_rst = pt2.phrase_lst[pi].isFlode(reverse_vec)
                    if isf_rst:
                        phrase2 = pt2.phrase_lst[pi]
                        if isf_rst == -1: parallel2 = True
                        break;
            if parallel1 or parallel2:
                path = Polyline(pt1, [edgePt_vec])
            else:
                min_vec1, min_vec2 = PointVec.minAngleVector(phrase1, phrase2, edgePt_vec, reverse_vec)
                mid_pt = PointVec.rayrayIntersect(pt1,min_vec1,pt2,min_vec2)  # 两个射线交点
                path_vec1 = pt1.initVecBetweenPts(mid_pt)   # ? 构造长度
                path_vec2 = mid_pt.initVecBetweenPts(pt2)
                path = Polyline(pt1, [path_vec1, path_vec2])
    else:  # 无法直接可见的始末点
        # 得到起点和终点到各自矩形到可见端点的路径
        rec1_edge_path_dict, rec2_edge_path_dict = {}, {}
        rec1_edge_path_dict[corner1_a] = Polyline(pt1, [pt1.initVecBetweenPts(rec1.pt_lst[corner1_a])])
        rec1_edge_path_dict[corner1_b] = Polyline(pt1, [pt1.initVecBetweenPts(rec1.pt_lst[corner1_b])])
        after_corner = 0 if corner1_b == 3 else corner1_b+1
        before_corner = 0 if after_corner == 3 else after_corner+1
        rec1_edge_path_dict[before_corner] = Polyline(pt1, [rec1_edge_path_dict[corner1_a], rec1.vec_lst[before_corner].reverse()])   # ?是不是索引个反向量就可以了?
        rec1_edge_path_dict[after_corner] = Polyline(pt1, [rec1_edge_path_dict[corner1_b], rec1.vec_lst[corner1_b]))

        # 重复抽象(但方向相反)

        # 将中间路径(可见点之间的路径), 起点到端点的路径累加, 得到所有路径
        path_lst = []; min_path, min_length = None, MAX;
        for corner1 in visiable_dict:
            for corner2_i in range(len(visiable_dict[corner1])):
                corner2 = visiable_dict[corner2_i]
                mid_path = shorestPath_dict[corner1][corner2_i]
                path_edge1 = rec1_edge_path_dict[corner1]
                path_edge2 = rec2_edge_path_dict[corner2]
                path = path_edge1.addPolyline(mid_path, path_edge2)    # ? 实现addPolyline方法
                path_lst.append(path)
                # 比较路径, 选择距离最短的路径
                if path.length() < min_length:
                    min_path = path
                    min_length = path.length()

        path = min_path
    return path
