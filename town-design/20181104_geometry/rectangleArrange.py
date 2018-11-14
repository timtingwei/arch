#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 布置建筑

def isBetweenPoly(length, polyline, poly_index):
    max_length = polyline.vec_length_lst[poly_index]
    rst = 0 <= length and length <= max_length
    return rst

def computeRecPosition(polyline, dist_lst, rec_lst):
    # 在多段线上, 根据间距和相关矩形属性得到矩形的位置
    poly_index = 0; poly_lengthToStart = 0.0;
    poly_num = len(polyline.vec_lst)

    poly_index_lst_rst = []; poly_lengthToStart_lst_rst = []
    for i in range(len(rec_lst)):
        rec = rec_lst[i]

        if rec.arrangeClass == 0:  # 在线段外的话, 换下一段线, 直到这段线合适为止
            while poly_index < poly_num:
                poly_lengthToStart += dist_lst[i]
                start_length = poly_lengthToStart  # 矩形头点距离
                if isBetweenPoly(start_length, polyline, poly_index):
                    poly_index += 1
                    poly_lengthToStart = 0.0
                    continue;
                poly_lengthToStart += rec.length   # 矩形尾点距离
                end_length = poly_lengthToStart
                if isBetweenPoly(end_length, polyline, poly_index):
                    poly_index += 1
                    poly_lengthToStart = 0.0
                    continue;
                # 此时矩形完全在线段上, 是满足条件的
                poly_index_lst_rst.append(poly_index)
                poly_lengthToStart_lst_rst.append(poly_lengthToStart)
                break;  # 退出while

        elif rec.arrangeClass == 1:  # 在线段外, 缩小长度, 填满这段线
            pass


    return poly_index_lst_rst, poly_lengthToStart_lst_rst  # 在哪段线上, 对于这段线端点的长度

# 根据线段, 线段索引, 相对长度, 原有宽深的矩形实例, 构造分配好位置的矩形
def arrangeRec(rec, polyline, poly_index, poly_lengthToStart):
    length_vec = polyline.vec_lst[poly_index].unit().amptify(poly_lengthToStart)
    start_pt = polyline.pt_lst[poly_index].addVec(length_vec)
    rec = Rectangle(rec.vec_lst[:], start_pt)
    return rec

# 沿着边界布置建筑
def arrangeAllRecs(rec_lst, polyline, poly_index_lst, poly_lengthToStart_lst):
    # 构造所有新矩形
    rec_lst = []
    for i in range(len(poly_index_lst)):
        rec = arrangeRec(rec_lst[i], polyline, poly_index_lst[i], poly_lengthToStart_lst[i])
        rec_lst.append(rec)
    return rec_lst

        
