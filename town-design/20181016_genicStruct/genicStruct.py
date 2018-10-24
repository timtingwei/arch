#!/usr/bin/env python
#-*- coding: utf-8 -*-
import random
import Queue
import readDataFromExcel
import readDictFromTxt
# 基因条构造
# 工作-爱好-吃饭-睡觉构造
class Node():
    ' 一个分类属性的结构 ' 
    def __init__(self, subGenicDataLst):
        n = len(subGenicDataLst[0])
        self.activity = ['']*n  # 事件     string   [a1, a2]
        self.domain = [0.0]*n    # 时间区间  double   [(d1, d2), (d3,d4)]
        self.place = ['']*n     # 地点     string  [[p1, p2], [p3, p4, p5]]
        self.isDup = [0]*n     # 是否关联  int      [0, 1]
        for i in range(n):
            self.activity[i] = (subGenicDataLst[0][i])
            self.domain[i] = tuple([float(d) for d in subGenicDataLst[1][i].split('~')])
            self.place[i] = subGenicDataLst[2][i].split('~')
            self.isDup[i] = 0 if cmp(subGenicDataLst[3][i], '否') == 0 else 1

class Parent():
    ' 基因库中一条基因对应的基类 '
    def __init__(self, genicDataLst, mappingObj):
        self.name = genicDataLst[0][0]      #职业名字
        #obj_lst = self.getNodeToList()
        #for i in range(1, 5):
        #    obj_lst[i-1] = Node(genicDataLst[i])
        self.job = Node(genicDataLst[1])    # 工作
        self.hobby = Node(genicDataLst[2])  # 爱好
        self.eat = Node(genicDataLst[3])    # 吃饭
        self.sleep = Node(genicDataLst[4])  # 睡觉
        self.breakup = [self.convertTimeFormat(time) for time in genicDataLst[5][0].split('-')]  # 起床时间点
        self.transType = genicDataLst[6]  # 出行方式
        self.relationMapping = mappingObj     # 类型映射属性

    def convertTimeFormat(self, s):
        # convert 6:30 to 6.5
        lst = s.split(':')
        return float(lst[0]) + float(lst[1])/60
    def getNodeToList(self):
        return [self.job, self.hobby, self.eat, self.sleep]

class DeltaNode(object):
    '压缩事件时间区间的优先队列的结点构造'
    def __init__(self, index, d, weight, flag):
        self.index = index
        self.weight = weight
        self.d = d
        self.flag = flag
    def __lt__(self, other):
        if self.flag == 1:     # 如果flag为1, weight大的排在前面, 权重大的被先扩展
            return self.weight > other.weight
        elif self.flag == -1:   # 如果flag为0, 权重小的先被压缩
            return self.weight < other.weight
    def __str__(self):
        return '(' + str(self.index)+',\'' + str(self.d)+',\'' + str(self.weight) + '\')'

class Child():
    ' 每个职业下不同人的事件安排结构 '
    def __init__(self, parent):
        self.parent = parent
        self.sequence = []  # 事件序列                       # string  [s1, s2, s3, s4]
        self.time = []      # 事件对应的时段值                # double  [t1, t2, t3, t4]
        self.place = []     # 事件对应的建筑类型序号, 建筑序号  # string,int  [[农田, 2], [工厂, 0], [p3,i3], [p4,i4]]
        self.trans_speed = [] # 储存与交通时间匹配的速度
        self.trans_time = []  # 储存与地点序列匹配的交通时间
        self.trans_path = []  # 储存对应事件和交通的路径结点序和距离
        self.breakup = 0.0    # 起床时间点
        # self.weight_data = {0: 10, 1: 14, 2: 15, 3:22, 4:9, 5:12, 6:5}  # 事件权重, 暂时随机分配
        self.weight_data = {0: 20, 1: 15, 2:10 , 3:9, 4:6, 5:5, 6:5}  # 事件权重, 暂时随机分配
        self.isArrangeValid = True    # 人的事件时间地点安排表是否合理
        # 分配事件对应的分类
        self.getSeqClassify()
        #self.seqClassify = [2, 0, 2, 1, 2, 1, 3]   # 吃饭, 事件, 吃饭, 事件, 吃饭, 事件, 睡觉
        # 按照的分配事件类序, 人的一日三餐保证睡眠, 粗略分配事件时刻地点表
        # self.arrangeActivityTimeSeq(num_lst)
        self.arrangeActivityTimeSeq()

        # 根据事件发生的地点, 安排交通事件, 
        self.arrangeTransActivity()
        if self.isArrangeValid == True:    # 如果交通时间安排的是有效的话
            # 得到总时间, 剩余时间是否满足睡眠区间, 压缩或者扩展事件时间
            self.adjustActivityTime()
            # 选择起床时间点
            self.breakup = self.selectBreakupTime()
            self.seq_clock_time = self.getSeqClockTime()     # 事件和交通的时间结点序列

    def getSeqClockTime(self):
        # 获得确定起床点, 事件和交通情况下, 时间结点序列
        seqTime = [0, self.breakup]
        temp_sum = self.breakup
        for i in range(len(self.time)-1):
            temp_sum = temp_sum + self.time[i]
            seqTime.append(temp_sum)
            temp_sum = temp_sum + self.trans_time[i]
            seqTime.append(temp_sum)
        seqTime.append(temp_sum + self.time[-1])
        # print(seqTime[-1]-child.breakup)   # right
        return seqTime

    def display(self):
        return

    def getSeqClassify(self):
        # 得到事件序列的类型
        self.seqClassify = [2, 0, 2, 1, 2, 1, 3]   # 初:吃饭, 事件, 吃饭, 事件, 吃饭, 事件, 睡觉
        # 暂时: 吃饭和睡觉不变, 事件中工作和爱好分配权重
        weight_data = {0: 5, 1: 5}   # 平均分配
        # 在数组中选择某个数来代替权重的运算
        i_lst = [1, 3, 5]
        for i in i_lst:
            self.seqClassify[i] = self.random_weight(weight_data)

    def arrangeActivityTimeSeq(self):
        # 学长的接口
        # 测试: 每个都是20
        # num_lst = [20]*(len(self.parent.relationMapping.arch_dict.keys()))
        num_lst = self.parent.relationMapping.tot_block_num
        # num_lst: 建筑类型中实际的区块数量
        # 得到每个人的事件时长地点, 三个列表
        self.sequence = []  # 事件序列                       # string  [s1, s2, s3, s4]
        self.time = []      # 事件对应的时段值                # double  [t1, t2, t3, t4]
        self.place = []     # 事件对应的建筑类型序号, 区块序号  # int,int  [[农田, 2], [工厂, 0], [p3,i3], [p4,i4]]
        # eat, job/hobby, eat, job/hobby, eat, job/hobby, sleep
        mp = {0:{}, 1:{}, 2:{}, 3:{}}   # key=事件, value = (建筑类型, 建筑序号)
        node_lst = self.parent.getNodeToList()
        for classify in self.seqClassify:
            # 选择事件为序号
            activity_len = len(node_lst[classify].activity)
            activity_i = random.choice(range(activity_len))
            #activity_i = random.randint(0, activity_len-1)
            # 得到该事件的横向列表
            activity_lst = [activity_i,
                            node_lst[classify].domain[activity_i],
                            node_lst[classify].place[activity_i],
                            node_lst[classify].isDup[activity_i]]
            # 为事件选择发生地点和建筑类型
            if activity_i in mp[classify] and activity_lst[3] == 1:
                # 重复且关联
                arch_type = ''
                arch_type_index = mp[classify][activity_i][0]
                arch_index = mp[classify][activity_i][1]
            else:
                arch_type = random.choice(activity_lst[2])
                arch_type_index = self.parent.relationMapping.archToIndex(arch_type)
                #arch_index = random.randint(0, num_lst[arch_type_index])
                arch_index = random.choice(range(num_lst[arch_type_index]))
                mp[classify][activity_i] = (arch_type_index, arch_index)
            if classify <> 3:   # 先不计算睡觉时间
                time = random.uniform(activity_lst[1][0], activity_lst[1][1]) #[d1, d2)
            else:
                time = 0
            self.sequence.append(activity_i)
            self.time.append(time)
            self.place.append((arch_type_index, arch_index))
        return

    def getActivityTotalTime(self):
        sum_t = 0
        for t in self.time:
            sum_t += t
        return sum_t

    def random_weight(self, weight_data):
        total = sum(weight_data.values())    # 权重求和
        ra = random.uniform(0, total)        # 在0与权重和之前获取一个随机数
        curr_sum = 0
        ret = None
        keys = weight_data.iterkeys()
        for k in keys:
            curr_sum += weight_data[k]       # 在遍历重累加当前权重
            if ra <= curr_sum:               # 当随机数<=当前权重和时, 返回权重key
                ret = k
                break
        return ret
    def getSeqTimePlaceList(self):
        return [self.seqClassify, self.sequence, self.time, self.place]

    def arrangeTransActivity(self):
        # 安排交通事件
        self.trans_speed = []
        self.trans_time = []
        self.trans_path = []
        # 求出所有的出行方式速度
        trans_speed_lst = [self.parent.relationMapping.getTransSpeedFromName(trans_type)*3.6
                           for trans_type in self.parent.transType]
        min_speed, max_speed = min(trans_speed_lst), max(trans_speed_lst)
        temp_trans_path = []
        # 保证睡眠的一天事儿
        for i in range(len(self.place)-1):
            distance = 0
            if self.place[i] != self.place[i+1]:
                shortestPath = self.parent.relationMapping.getNodeShortestPath([self.place[i], self.place[i+1]])
                #print('shorestPath:', shortestPath)
                if shortestPath == -1:  # 跨越2.5层, 不存在最短路
                    self.isArrangeValid = False
                    return
                distance = shortestPath[1]/1000        # 米和公米进行转换
                temp_trans_path.append(shortestPath)
            #distance = random.uniform(0.5, 5)    # 在0.5~5之间随机
            speed = 0.0
            # 1km以内走路, 1km以上选择用最快交通工具
            speed = min_speed if distance < 1.0 else max_speed
            time = distance / speed
            self.trans_speed.append(speed)
            self.trans_time.append(time)
        self.trans_path = temp_trans_path
        return
        
    def adjustActivityTime(self):
        # 测试
        #print('activity_time:')
        #print(self.time)
        #print('total activityAndTransport time:')
        #print(self.getActivityTotalTime()+sum(self.trans_time))
        # 根据计算得到交通序列, 调整事件消耗的时间
        update_total_time = sum(self.trans_time) + self.getActivityTotalTime()
        # 事件的权重, 应该作为类属性
        #self.weight_data = {0: 20, 1: 15, 2:10 , 3:9, 4:6, 5:5, 6:5}  # 事件权重, 暂时随机分配
        self.weight_data = {0: 5, 1: 20, 2:10 , 3:20, 4:10, 5:10, 6:5}

        seq_n = len(self.sequence)
        node_lst = self.parent.getNodeToList()
        domain_lst = [ node_lst[self.seqClassify[i]].domain[self.sequence[i]]
                       for i in range(seq_n)]    # 已经存在的每个事件的区间
        sleep_d1, sleep_d2 = domain_lst[-1][0], domain_lst[-1][1]
        delta, flag = 0, 0
        # q_node_lst = [0]*(seq_n-1)    # 用于构造优先队列 [[0, d0, weight0], [1, d1, weight1]]
        que = Queue.PriorityQueue()     # que中存放DeltaNode{index, d, weight}
        if 24-update_total_time < sleep_d1:   # 睡眠不足
            self.time[-1] = sleep_d1          # 保证最必要的睡眠
            flag = -1
            delta = sleep_d1 - (24-update_total_time)
            # 压缩优先队列,  权重小的差值在前
            for i in range(seq_n-1):
                # 当前时间和区间左端点的差, 事件权重
                que.put(DeltaNode(i, self.time[i] - domain_lst[i][0], self.weight_data[i], flag))
            
        elif 24 - update_total_time > sleep_d2:    # 睡眠过多
            self.time[-1] = sleep_d2          # 保证最必要的睡眠
            flag = 1
            delta = 24 - update_total_time - sleep_d2
            # 扩展优先队列, 权重大的事件差值在前
            for i in range(seq_n-1):
                # 当前时间和区间右端点的差, 事件权重
                que.put(DeltaNode(i, domain_lst[i][1] - self.time[i], self.weight_data[i], flag))
        else:
            self.time[-1] = 24 - update_total_time   # 睡眠区间合理, 剩余时间睡觉
            # 分配交通时间(之前分配的交通时间是合理的)
            return 
                
        while delta != 0 and not que.empty():
            qNode = que.get()  # 队首出队
            if qNode.d <= delta:
                delta = delta - qNode.d
                if flag == 1:
                    self.time[qNode.index] = domain_lst[qNode.index][1]  # 扩展取右端点
                else:
                    self.time[qNode.index] = domain_lst[qNode.index][0]  # 压缩取左端点
            else:   # 队首差值大于剩余delta
                self.time[qNode.index] = self.time[qNode.index] + delta * flag  # 1加-1减
                delta = 0
        if delta != 0:   # 所有可扩展或者压缩的区间分配完后, 仍旧不足
            self.isArrangeValid = False
            # 路径选择太远
            # 建筑位点选择太远
            # 出行方式不恰当
            # 城市路网不合理
            # 城市区块分布有问题

            # 修改之前插入的一天的交通时间(还没写)
        else:
            self.isArrangeValid = True

        return

    def getActivityAndTransTotalTime(self):
        return sum(self.trans_time) + self.getActivityTotalTime()

    def selectBreakupTime(self):
        # 选择起床时间点
        # 测试:[6.5, 9.5]   [23.5, 1.0]
        # print('selectBreakupTime():', self.parent.breakup)
        ret = 0.0
        domain = self.parent.breakup
        if domain[0] < domain[1]:
            ret =  random.uniform(domain[0], domain[1])
        else:
            tmp = [random.uniform(domain[0], 24), random.uniform(0, domain[1])]
            ret = random.choice(tmp)
        return ret

class ParentBlock(object):
    ' 所有区块对象的存储结构 '
    def __init__(self, block_lst):      # 人对象作为成员函数的参数, 不作为属性(目前暂时选择这种)
        self.block_dict =  {}           # 属于这个父block的所有blocks, key = name, value=obj
        for block in block_lst:
            self.block_dict[block.name] = block   # 跟直接根据name找到block实例对象

        self.tot_area = 0               # 所有子区块的总面积(未算)
        return

    """
    def __init__(self, block_lst, child_lst):
        self.block_dict =  {}           # 属于这个父block的所有blocks, key = name, value=obj
        for block in block_lst:
            self.block_dict[block.name] = block   # 跟直接根据name找到block实例对象

        self.child_lst = child_lst      # 所有跟这个bloc相关的人对象
        self.tot_area = 0               # 所有子区块的总面积(未算)
        return
    """

    def statPersonCount(self, child_lst):
        # 统计各个子区块的信息
        # 根据传入的人员对象, 统计各个子区块的使用总人流量, 最大同时使用人数, 地块总花费的时长
        # 规定不同时段地块人数的时间间隔
        tot_time = 24     # 记录一天的变化
        range_num = 48    # 一天被分成48个时段
        for key in self.block_dict:
            self.block_dict[key].initTimeSeqPersonCountLst(range_num)   # 初始化成[0]*range_num
        
        # 构造打点时间序列
        temp_sum = 0
        clock_time_range = []
        while temp_sum < tot_time:
            clock_time_range.append(temp_sum)
            temp_sum = temp_sum + float(tot_time) / range_num

        seq_p = 0
        for child in child_lst:  # 遍历每个人
            len_place = len(child.place)
            mp_name =  {}   # 一天中某人多次去某个地方, 只算增加一个人
            for i in range(len_place):   # 遍历当前人的所有事件地点
                block_name = child.place[i][0]
                self.block_dict[block_name].addSumTime(child.time[i])  #总花费时长
                if not block_name in mp_name:
                    self.block_dict[block_name].addTotPerosonCount()   #使用总人流量
                    mp_name[block_name] = 1   # 标记

            # 人对象不同时间段所处的地块, 可获得某地块当天的最大同时使用人数(这一块可直接传入drawing函数)
            seq_p = 0
            for i in range(range_num):
                t = clock_time_range[i]
                while child.seq_clock_time[seq_p+1] <= t:     # maybe error
                    seq_p = seq_p + 1
                # seq_clock_time[seq_p] <= t < seq_clock_time[seq_p+1]
                if seq_p == 0:     # 起床前睡觉地点(基因条未计算)
                    block_name = child.place[-1][0]
                else:
                    if seq_p % 2 == 1:
                        block_name = child.place[int(seq_p-1)/2][0]
                    # 暂时忽略交通的情况
                self.block_dict[block_name].addOneTimeRangePersonCount(i)
                #print(t, block_name, seq_p)
        for block_name in self.block_dict:
            block_obj = self.block_dict[block_name]
            print('block_name: ' + str(block_name))
            # 使用总人流量
            print('tot_person_count = ' + str(block_obj.tot_person_count))
            # 总花费的时长
            print('sum_time = ' + str(block_obj.sum_time))
            block_obj.max_person_count = max(block_obj.time_seq_person_count)  #最大同时使用人数
            
            print('block.time_seq_person_count =  ', block_obj.time_seq_person_count)
            print('block.max_person_count = ' + str(block_obj.max_person_count))
        return

    # 统计总共地块的信息

    # 为所有区块分配建筑
    def arrangeAllBlock(self, building_density_lst, plot_ratio_lst, arch_num_lst):
        i = 0
        for block_name in self.block_dict:
            block_obj = self.block_dict[block_name]
            # 根据地块人员分配计算出使用面积
            block_obj.getUseArea()
            # 在使用面积确定的情况下, 控制建筑密度, 容积率，建筑数量
            block_obj.arrangeArch(block_obj.use_area, building_density_lst[i], plot_ratio_lst[i], arch_num_lst[i]):
            i += 1
        return
                
            
class ChildBlock(object):
    '每一个区块对象'
    def __init__(self, name):
        self.name = name    # 区块建筑类型名字(序号)
        self.arch = []      # 属于该区块的建筑对象(未添加)
        self.tot_person_count = 0    # 区块一天中使用的总人流量
        self.max_person_count = 0    # 一天中最大的同时使用人数
        self.sum_time = 0.0  # 一天中不同人总共在该地块花费的时长
        self.area = []      # 该区块面积(未添加)
        self.time_seq_person_count = []    # 一天中不同时段该地块人数
        self.use_area = 0   # 该区块总使用面积

    def addTotPerosonCount(self):
        # 增加一个区块一天中使用的总人数
        self.tot_person_count = self.tot_person_count + 1
        return

    def updateMaxPersonCount(self, compareCount):
        # 尝试用当前地块人数更新最大同时使用人数
        self.max_person_count = compareCount if compareCount > self.max_person_count else self.max_person_count
        return

    def addSumTime(self, addTime):
        self.sum_time = self.sum_time + addTime
        return

    def initTimeSeqPersonCountLst(self, num):
        # 为一天中不同时段地块人数数组建立初始Hash表
        self.time_seq_person_count = [0] * num
        return

    def addOneTimeRangePersonCount(self, time_i):
        self.time_seq_person_count[time_i] += 1
        return

    def getUseArea(self, self.max_person_count):
        # 根据一天中最大的同时使用人数, 映射计算出总使用面积
        # 假设每个人需要10平米面积
        self.use_area = 10 * self.max_person_count
        return
        

    def arrangeArch(self, self.use_area, building_density, plot_ratio, arch_num):
        # 根据建筑使用面积, 建筑密度, 容积率, 建筑数量, 得到区块中各个建筑面积和高度, 以及其他关于地块的中间数据
        if not self.use_area: return -1
        floor_space = use_area / plot_ratio
        tot_area = floor_space / building_density

        # 平均分配面积
        each_area = tot_area / each_num
        # 平均分配高度
        each_height = use_area / each_area / arch_num

        if each_height < 3 or each_height > 15:
            return -1
        else:
            return each_height
            

class TypeMapping():
    # 关系映射对象, 用于查表
    def __init__(self, tot_arch_type, tot_trans_type, tot_job_type, tot_trans_speed, tot_node_path, tot_block_num):
        self.arch_dict = {}
        self.arch_type = tot_arch_type
        for i in range(len(tot_arch_type)):
            # f(建筑类型) = 建筑类型编号
            self.arch_dict[tot_arch_type[i]] = i
        self.node_path = tot_node_path
        """
        # {'p1,i1;p2,i2': [([node_i1, node_i2, node_i3], d1),
                           ([node_i4, node_i5, node_i6], d2),
                           ([node_i7, node_i8, node_i9], d3)],
           'p3,i3;p4,i4': [([node_i1, node_i2, node_i3], d1),
                           ([node_i4, node_i5, node_i6], d2),
                           ([node_i7, node_i8, node_i9], d3)]
          }
        """
        self.trans_type_dict = {}  # 将出行方式映射成序号
        self.trans_speed_dict = {}  # 将出行序号映射成速度
        for i in range(len(tot_trans_type)):
            self.trans_type_dict[tot_trans_type[i]] = i
            self.trans_speed_dict[i] = tot_trans_speed[i]

        self.tot_block_num = [int(num) for num in tot_block_num]   # 各个建筑类型对应的区块数量
        return

    def archToIndex(self, archType):
        #print(archType.encode('utf-8'))
        return self.arch_dict[archType]
    def indexToArch(self, index):
        # 将建筑类型序号映射成建筑类型
        return self.arch_type[index]

    def nodeToPath(self, node_pair):
        # f(结点序号) = 结点间路径
        # node_pair: [(p1, i1), (p2, i2)] -> key = 'p1,i1;p2,i2'
        s1 = str(node_pair[0][0]) + ',' + str(node_pair[0][1])
        s2 = str(node_pair[1][0]) + ',' + str(node_pair[1][1])
        s_node1 = s1 + ';' + s2
        s_node2 = s2 + ';' + s1
        # print('s_node', s_node)
        if s_node1 in self.node_path or s_node2 in self.node_path:
            ret = self.node_path[s_node1] if s_node1 in self.node_path else self.node_path[s_node2]
            return ret
        else:
            #print('error:node not in dict, no path.')
            return -1

    def getNodeShortestPath(self, node_pair):
        node_paths = self.nodeToPath(node_pair)
        if node_paths != -1:
            # 根据带距离的路径结点, 选择最近的距离
            return node_paths[0]  # ([node_i1, node_i2, node_i3], d1)
        else:
            return -1

    def getTransSpeedFromName(self, trans_type):
        #print(trans_type.encode('utf-8'))
        return self.trans_speed_dict[self.trans_type_dict[trans_type]]

    def getTransSpeedFromIndex(self, trans_type_i):
        return self.trans_speed_dict[trans_type_i]



class Path(object):
    ' 路径对象描述 '
    def __init__(self):
        self.shortestPaths = {}
    
def testNode(node):
    print('testNode:')
    print(str(node.activity).decode('string_escape'))
    print(node.domain)
    print(str(node.place).decode('string_escape'))
    #print([str(p).decode('string_escape') for p in node.place])
    print(node.isDup)

def testParent(parent):
    print(parent.name)
    testNode(parent.job)
    testNode(parent.hobby)
    testNode(parent.eat)
    testNode(parent.sleep)
    print(parent.breakup)
    print(str(parent.transType).decode('string_escape'))
    print('parent.tot_block_num: ')
    print(parent.relationMapping.tot_block_num)

def testChild(child):
    seqTimePlace_lst = child.getSeqTimePlaceList()
    print("seqClassify:")
    print(seqTimePlace_lst[0])
    print("sequence:")
    print(seqTimePlace_lst[1])
    print("time:")
    print(seqTimePlace_lst[2])
    print("place:")
    #print(seqTimePlace_lst[3])
    temp = [(child.parent.relationMapping.indexToArch(place[0]), place[1]) for place in seqTimePlace_lst[3]]
    print(str(temp).decode('string_escape'))
    print("total activity time = " + str(child.getActivityTotalTime()))
    print('trans_time: ')
    print(child.trans_time)
    print("total time = " + str(child.getActivityAndTransTotalTime()))
    print("child.isArrangeValid = " + str(child.isArrangeValid))

def statBlockData(child_lst, mapping):
    # 构造地块实例和统计地块信息
    block_lst = []
    type_num = len(mapping.arch_type)
    block_lst = [ChildBlock(name) for name in range(type_num)]
    parentBlock = ParentBlock(block_lst)
    parentBlock.statPersonCount(child_lst)  # 统计地块信息, 写入各个地块


def child_main():
    filepath = '/Users/htwt/Desktop/20181019_totalGenics.xls'
    genicDataLst_lst, tot_job_scale, tot_block_num, tot_arch_type, tot_job_type, tot_trans_type, tot_trans_speed = readDataFromExcel.read(filepath)
    genicDataLst = genicDataLst_lst[18]   # 选取其中一种职业
    tot_node_path = readDictFromTxt.getNodePathDict()
    mapping = TypeMapping(tot_arch_type, tot_trans_type, tot_job_type, tot_trans_speed, tot_node_path, tot_block_num)
    parent = Parent(genicDataLst, mapping)
    #testParent(parent)
    while 1:
        child = Child(parent)                     # 有很多人位点选择不合理
        if child.isArrangeValid == True: break;   # 直到循环出满意的才结束
    #child = Child(parent)
    testChild(child)
    statBlockData([child], mapping)
    return


def createChild(parent):   # 因为2.5层路网不全做的一个循环
    while 1:
        child = Child(parent)
        if child.isArrangeValid == True:
            break;
    return child

def parent_main():
    filepath = '/Users/htwt/Desktop/20181019_totalGenics.xls'
    genicDataLst_lst, tot_job_scale, tot_block_num, tot_arch_type, tot_job_type, tot_trans_type, tot_trans_speed = readDataFromExcel.read(filepath)
    tot_node_path = readDictFromTxt.getNodePathDict()
    mapping = TypeMapping(tot_arch_type, tot_trans_type, tot_job_type, tot_trans_speed, tot_node_path, tot_block_num)

    tot_num = 1000       # 总人数
    # 重新计算每个职业的实际比例
    sum_scale = sum(tot_job_scale)
    for i in range(len(tot_job_scale)):
        tot_job_scale[i] = tot_job_scale[i]/ sum_scale

    # 传入所有职业的基因条, 得到所有职业的父类实例
    parent_lst = [Parent(genicDataLst, mapping) for genicDataLst in genicDataLst_lst]
    # 根据总人数和分配比得到每个职业的人数
    num_lst = [int(x * tot_num) for x in tot_job_scale]
    #print(num_lst)

    # 根据每个职业的人数和已经构造好的父类, 构造一定数量的子类实例
    children_dict = {}   # 职业序号为key的所有人对象
    children_lst = []
    for i in range(len(parent_lst)):
       parent = parent_lst[i]
       child_lst = []
       for j in range(num_lst[i]):
           child = createChild(parent)
           child_lst.append(child)
           children_lst.append(child)
       #child_lst =  [createChild(parent) for j in range(num_lst[i])]
       children_dict[i] = child_lst

    # 根据人统计地块信息
    statBlockData(children_lst, mapping)
    


if __name__ == "__main__":
    #child_main()
    parent_main()

