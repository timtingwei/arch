"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "htwt"
__version__ = "2018.10.22"

import rhinoscriptsyntax as rs
from genicStructGh import child_main

def main():
    # place_pt_lst: 该对象静态事件发生的点序列
    # road_curve:   该对象交通事件对应的路径线段
    child_main_lst = child_main()
    breakup = child_main_lst[0]
    seq_time = child_main_lst[1]
    trans_time = child_main_lst[2]
    place = child_main_lst[3]

    print('breakup:')
    print(breakup)
    print('seq_time:')
    print(seq_time)
    print('trans_time:')
    print(trans_time)
    #print('place:')
    #print(place)

    # 设置帧数
    #time_step = 0.1   # 0.1h/帧 = 6min/帧
    time_step = 1     # 1h/帧
    tot_time = 24     # 记录一天的变化
    
    # 构造打点时间序列
    temp_sum = 0
    clock_time_range = []
    while temp_sum < tot_time:
        clock_time_range.append(temp_sum)
        temp_sum = temp_sum + time_step

    # 获得确定起床点, 事件和交通情况下, 时间结点序列
    seqTime = [0, breakup]
    temp_sum = breakup
    for i in range(len(seq_time)-1):
        temp_sum = temp_sum + seq_time[i]
        seqTime.append(temp_sum)
        temp_sum = temp_sum + trans_time[i]
        seqTime.append(temp_sum)
    seqTime.append(temp_sum + seq_time[-1])
    # print(seqTime[-1]-breakup)   # right

    pt_lst = []       # 一个人的每一帧的点
    seq_p = 0         # 在序列上标记时间的指针
    for t in clock_time_range:
        while seqTime[seq_p+1] <= t:   # 用指针找到对应区间
            seq_p = seq_p + 1
        # seqTime[seq_p] <= t < seqTime[seq_p+1]
        if seq_p == 0:                 # 起床前睡觉地点(基因条未计算)
            pt = place_pt_lst[-1]
        else:                          # 一天的正常作息
            if seq_p % 2 == 1:  # 静事件
                pt = place_pt_lst[int((seq_p-1)/2)]
            else:               # 交通事件
                road_curve = road_curve_lst[int((seq_p-1)/2)]
                scale_t = (t-seqTime[seq_p]) / trans_time[int((seq_p-1)/2)]
                domain = rs.CurveDomain(road_curve)
                pt = rs.EvaluateCurve(road_curve, domain[1]*scale_t)
        pt_lst.append(pt)
    return pt_lst
    

pt_lst = main()