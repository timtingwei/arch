#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 面积转换宽深机制
def limit(length, length_domain):
    # 把长度限制在值域范围内
    length = length_domain[0] if length < length_domain[0] else (length_domain[1] if length > length_domain[1] else length)
    return length
    

def recomputeDomain(area, length_domain, width_domain):
   # 根据面积, 对宽深范围重新计算, 得到在限制一次后, 不会超出的范围
    l_d1 = area/width_domain[1]  # 得到最大深时的最小宽
    l_d2 = area/width_domain[0]  # 得到最小深时的最大宽
    if l_d1 > length_domain[0]: length_domain[0] = l_d1
    if l_d2 < length_domain[1]: length_domain[1] = l_d2

    l_w1 = area/length_domain[1]  # 得到最大宽时的最小深
    l_w2 = area/length_domain[0]  # 得到最小宽时的最大深
    if l_w1 > width_domain[0]: width_domain[0] = l_w1
    if l_w2 < width_domain[1]: width_domain[1] = l_w2
    return length_domain, width_domain
    

def convertArea(area, length_domain, width_domain, length, width, flag):
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
    length_domian, width_domain = recomputeDomain(area, length_domain, width_domain)
    if flag:
        length = limit(length, length_domain)
        width = area / length
    else:
        width = limit(width, width_domain)
        length = area / width
    return length, width
    
