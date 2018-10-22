
__author__ = "htwt"
__version__ = "2018.10.22"

import rhinoscriptsyntax as rs
#from genicStructGh import child_main
import genicStructGh

def createHash(keys, values):
    mp = {}
    n = len(keys)
    for i in range(n):
        mp[keys[i]] = values[i]
    return mp
def getDicts():
    road_dict = createHash(road_node_key, road_bet_node)
    place_dict = createHash(place_index_key, place_pt)
    insert_road_dict = createHash(insert_node_key, road_insert)
    return road_dict, place_dict, insert_road_dict

def getPlacePtLst(place_lst, place_dict):
    return [place_dict[str(place[0]) + ',' + str(place[1])] for place in place_lst]

def getRoadCurve(key1, key2, trans_path, road_dict, insert_road_dict):
    # 根据路径结点序号得到一条路径线段
    curve_lst = []
    #trans_path = ([9, 0, 70, 79, 91, 77, 8, 60, 56, 58, 47, 43, 29, 61, 50, 54, 78, 81, 80], 3660.0)
    if trans_path[1] == 0:
        return curve_lst
    curve_lst.append(insert_road_dict[key1])
    n = len(trans_path[0])
    for i in range(n-1):
        node, next = trans_path[0][i], trans_path[0][i+1]
        s1, s2 = str(node) + ',' + str(next), str(next) + ',' + str(node)
        cur = road_dict[s1] if s1 in road_dict else road_dict[s2]      # 0->9 or 9->0
        #print(cur)
        curve_lst.append(cur)
    curve_lst.append(insert_road_dict[key2])
    num = len(curve_lst)
    if num:
        if num == 1:
            return curve_lst[0]
        join_curve = rs.JoinCurves(curve_lst)
        length = rs.CurveLength(join_curve)
        print('length = ' + str(length))
        return join_curve
        #print(length)
        #t = 0.5
        #pt = rs.CurveArcLengthPoint(join_curve, t*length)
    else:
        return 

def getChildPtLst(child, place_dict, road_dict, insert_road_dict, clock_time_range):
    pt_lst = []       # 一个人的每一帧的点
    if not child.isArrangeValid:   # 如果该人的事件排列无效的话, 返回空列表
        return pt_lst
    # self.trans_path = [([9, 0, 70, 79, 91, 77, 8, 60, 56, 58, 47, 43, 29, 61, 50, 54, 78, 81, 80], 3660.0), ([], d), ([], d)]
    
    # 打印测试数据
    #genicStructGh.testChild(child)
    print(child.place)
    print(child.trans_path)

    # child.isArrangeValid, child.breakup, child.time, child.trans_time, child.trans_speed, child.place, child.trans_path
    # 根据child.place得到区块点表(place_pt_lst), 根据child.trans_path得到道路多段线(road_curve_lst)
    # place_pt_lst: 该对象静态事件发生的点序列
    # road_curve:   该对象交通事件对应的路径线段
    place_pt_lst = getPlacePtLst(child.place, place_dict)
    #road_curve_lst = [getRoadCurve(path, road_dict) for path in child.trans_path]
    road_curve_lst = []
    for i in range(len(child.trans_path)):
        place_this, place_next = child.place[i], child.place[i+1]
        path = child.trans_path[i]
        key1 = str(place_this[0]) + ',' + str(place_this[1]) + ';' + str(path[0][0])
        key2 = str(place_next[0]) + ',' + str(place_next[1]) + ';' + str(path[0][-1])
        road_curve = getRoadCurve(key1, key2, path, road_dict, insert_road_dict)
        road_curve_lst.append(road_curve)
    
    # evaluateCurveByLength() 组合line成polyline, 根据距离得到线上对应点
    # 获得确定起床点, 事件和交通情况下, 时间结点序列
    seqTime = [0, child.breakup]
    temp_sum = child.breakup
    for i in range(len(child.time)-1):
        temp_sum = temp_sum + child.time[i]
        seqTime.append(temp_sum)
        temp_sum = temp_sum + child.trans_time[i]
        seqTime.append(temp_sum)
    seqTime.append(temp_sum + child.time[-1])
    # print(seqTime[-1]-child.breakup)   # right

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
                scale_t = (t-seqTime[seq_p]) / child.trans_time[int((seq_p-1)/2)]
                #domain = rs.CurveDomain(road_curve)
                #pt = rs.EvaluateCurve(road_curve, domain[1]*scale_t)
                #length = child.trans_path[int((seq_p-1)/2)][1]*scale_t
                #pt = rs.CurveArcLengthPoint(road_curve, length)
        pt_lst.append(pt)
    return pt_lst, place_pt_lst, road_curve_lst

def main():
    dicts_lst = getDicts()
    road_dict, place_dict, insert_road_dict = dicts_lst[0], dicts_lst[1], dicts_lst[2]

    insert_road_dict['4,15;77']
    # 设置帧数
    time_step = 0.1   # 0.1h/帧 = 6min/帧
    #time_step = 1     # 1h/帧
    #time_step = 1/60   # 1min/zhen
    tot_time = 24     # 记录一天的变化
    
    # 构造打点时间序列
    temp_sum = 0
    clock_time_range = []
    while temp_sum < tot_time:
        clock_time_range.append(temp_sum)
        temp_sum = temp_sum + time_step

    pts_lst = []      # 所有人的帧数点的集合
    child_lst = genicStructGh.child_main()    # 从基因条py中传入所有的子对象
    
    #print(child_lst)
    """
    for child in child_lst:
        pts_lst.append(getChildPtLst(child, place_dict, road_dict, clock_time_range))
    
    return pts_lst
    """
    return getChildPtLst(child_lst[18], place_dict, road_dict, insert_road_dict, clock_time_range)
    

pt_lst, place_pt_lst, road_curve_lst = main()
