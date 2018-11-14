#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 布置建筑

def isBetweenPoly(length, polyline, poly_index):
    # 判断当前长度是否位于polyline上
    max_length = polyline.vec_length_lst[poly_index]
    rst = (0 <= length and length <= max_length)
    return rst

#def computeArchPosition(edge, dist_lst, arch_lst, angle_lst = None):
def computeArchPosition(edge, dist_lst, arch_lst, angle_lst = None):
    # 在多段线上, 根据间距和相关矩形属性得到矩形的位置
    poly_index = 0; poly_lengthToStart = 0.0;
    poly_num = len(edge.vec_lst)

    poly_index_lst_rst = []; poly_lengthToStart_lst_rst = []
    for i in range(len(arch_lst)):
        arch = arch_lst[i]

        if arch.arrangeClass == 0:  # 在建筑垂线在线段外, 布置在下一条合适的段线直到合适为止
            while poly_index < poly_num:
                poly_lengthToStart += dist_lst[i]
                start_length = poly_lengthToStart  # 矩形头点距离
                if isBetweenPoly(start_length, edge, poly_index):
                    poly_index += 1
                    poly_lengthToStart = 0.0
                    continue;
                poly_lengthToStart += arch.length   # 矩形尾点距离
                end_length = poly_lengthToStart
                if isBetweenPoly(end_length, edge, poly_index):
                    poly_index += 1
                    poly_lengthToStart = 0.0
                    continue;
                # 此时矩形完全在线段上, 是满足条件的
                poly_index_lst_rst.append(poly_index)
                poly_lengthToStart_lst_rst.append(poly_lengthToStart)
                break;  # 退出while

        elif arch.arrangeClass == 1:  # 在线段外, 缩小长度, 填满这段线
            pass


    return poly_index_lst_rst, poly_lengthToStart_lst_rst  # 在哪段线上, 对于这段线端点的长度

# 根据线段, 线段索引, 相对长度, 原有宽深的矩形实例, 构造分配好位置的矩形
def arrangeArch(arch, edge, poly_index, poly_lengthToStart, offset = None):
    origin_vec1 = edge.vec_lst[poly_index].unit()                 # 得到该线段的单位向量
    start_length_vec = origin_vec1.amptify(poly_lengthToStart)    # 线段初始点到位点的向量
    start_pt = edge.pt_lst[poly_index].addVec(start_length_vec)   # 矩形的初始位点
    # 得到偏移的向量

    origin_vec2 = origin_vec1.rotate(90)   # 得到该线段向量的垂直向量
    vec_lst = [origin_vec1, origin_vec2, ReverseVector(origin_vec1), ReverseVector(origin_vec2)]

    arch.fillArchWithRectangle(start_pt, vec_lst)
    return arch

# 沿着边界布置建筑
def arrangeAllArchs(arch_lst, edge, poly_index_lst, poly_lengthToStart_lst):
    # 构造所有新矩形
    arch_lst = []
    for i in range(len(poly_index_lst)):
        arch = arrangeArch(arch_lst[i], edge, poly_index_lst[i], poly_lengthToStart_lst[i])
        arch_lst.append(arch)
    return arch_lst

        
