#!/usr/bin/env python
#-*- coding: utf-8 -*-
import random
import Queue
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
    def __init__(self, genicDataLst, mappingObj, path_obj):
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
        self.typeMapping = mappingObj     # 类型映射属性

    def convertTimeFormat(self, s):
        # convert 6:30 to 6.5
        lst = s.split(':')
        return float(lst[0]) + float(lst[1])/60
    def getNodeToList(self):
        return [self.job, self.hobby, self.eat, self.sleep]

class DeltaNode(object):
    '压缩事件时间区间的优先队列的结点构造'
    def __init__(self, index, d, weight):
        self.index = index
        self.weight = weight
        self.d = d
    def __lt__(self, other):
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
        self.weight_data = {0: 10, 1: 14, 2: 15, 3:22, 4:9, 5:12, 6:5}  # 事件权重, 暂时随机分配
        self.isArrangeValid = False    # 人的事件时间地点安排表是否合理
        # 分配事件对应的分类
        self.getSeqClassify()
        #self.seqClassify = [2, 0, 2, 1, 2, 1, 3]   # 吃饭, 事件, 吃饭, 事件, 吃饭, 事件, 睡觉
        # 按照的分配事件类序, 人的一日三餐保证睡眠, 粗略分配事件时刻地点表
        # self.arrangeActivityTimeSeq(num_lst)
        self.arrangeActivityTimeSeq()
        # 根据事件发生的地点, 安排交通事件, 得到总时间后压缩或者扩展区间
        self.arrangeTransActivity(self.parent.path_obj)
        # 计算事件总和, 与24小时比较, 剩余时间是否满足睡眠区间, 压缩或者延伸时间长度
    def display(self):
        return

    def getSeqClassify(self):
        self.seqClassify = [2, 0, 2, 1, 2, 1, 3]   # 吃饭, 事件, 吃饭, 事件, 吃饭, 事件, 睡觉
        # 暂时: 吃饭和睡觉不变, 事件中工作和爱好分配权重
        weight_data = {0: 1, 1: 9}   # 平均分配
        # 在数组中选择某个数来代替权重的运算
        i_lst = [1, 3, 5]
        for i in i_lst:
            self.seqClassify[i] = self.random_weight(weight_data)

    def arrangeActivityTimeSeq(self):
        # 学长的接口
        # 测试: 每个都是20
        num_lst = [20]*(len(self.parent.typeMapping.arch_dict.keys()))
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
                arch_type_index = self.parent.typeMapping.archToIndex(arch_type)
                arch_index = random.randint(0, num_lst[arch_index])
                mp[classify][activity_i] = (arch_type_index, arch_index)
            if classify <> 3:   # 先不计算睡觉时间
                time = random.uniform(activity_lst[1][0], activity_lst[1][1]) #[d1, d2)
            else:
                time = 0
            self.sequence.append(activity_i)
            self.time.append(time)
            self.place.append((arch_type_index, arch_index))
        return

    def getTotalTime(self):
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

    def arrangeTransActivity(self.parent.path_obj):

        # 事件的权重, 应该作为类属性
        self.weight_data = {0: 10, 1: 14, 2: 15, 3:22, 4:9, 5:12, 6:5}  # 事件权重, 暂时随机分配
        # 保证睡眠的一天事儿
        tran_time_lst = []
        for i range(len(self.place)-1):
            distance = path_obj.getShortestPathDistance(self.place[i], self.place[i+1])
            tran_type_int = random.randint(0, len(self.transType))
            time = distance / speed
            tran_time_lst.append(time)
        update_total_time = sum(tran_time_lst) + getTotalTime()

        seq_n = len(self.sequence)
        node_lst = self.parent.getNodeList()
        domain_lst = [ node_lst[self.seqClassify[i]].domain[self.sequence[i]]
                       for i in range(seq_n)]    # 已经存在的每个事件的区间
        sleep_d1, sleep_d2 = domain_lst[-1][0], domain_lst[-1][1]
        delta, flag = 0, 0
        q_node_lst = [0]*(seq_n-1)    # 用于构造优先队列 [[0, d0, weight0], [1, d1, weight1]]
        que = Queue.PriorityQueue()
        if 24-update_total_time < sleep_d1:   # 睡眠不足
            self.time[-1] = sleep_d1          # 保证最必要的睡眠
            flag = -1
            delta = sleep_d1 - (24-update_total_time)
            # 压缩优先队列,  权重小的差值在前
            for i in range(seq_n-1):
                # 当前时间和区间左端点的差, 事件权重
                que.put(DeltaNode(i, self.time[i] - domain_lst[i][0], self.weight_data[i]))
            
        elif 24 - update_total_time > d2:    # 睡眠过多
            self.time[-1] = sleep_d2          # 保证最必要的睡眠
            flag = 1
            delta = 24 - update_total_time - sleep_d2
            # 扩展优先队列, 权重大的事件差值在前
            for i in range(seq_n-1):
                # 当前时间和区间右端点的差, 事件权重
                que.put(DeltaNode(i, domain_lst[i][1] - self.time[i], self.weight_data[i]))
        else:
            self.time[-1] = 24 - update_total_time   # 睡眠区间合理, 剩余时间睡觉
            # 分配交通时间(还没写)

            return 
                

        while delta != 0 and not que.empty():
            qNode = que.get()  # 队首出队
            if qNode.d <= delta:
                delta = delta - qNode.d
                if flag == 1:
                    this.time[qNode.index] = domain_lst[qNode.index][1]  # 扩展取右端点
                else:
                    this.time[qNode.index] = domain_lst[qNode.index][0]  # 压缩取左端点
            else:   # 队首差值大于剩余delta
                this.time[qNode.index] = this.time[qNode.index] + delta * flag  # 1加-1减
                delta = 0
        if delta != 0:   # 所有可扩展或者压缩的区间分配完后, 仍旧不足
            self.isArrangeValid = False
            # 路径选择太远
            # 建筑位点选择太远
            # 出行方式不恰当
            # 城市路网不合理
            # 城市区块分布有问题
        else:
            self.isArrangeValid = True

        # 插入一天的交通时间(还没写)

        return
        
            

class TypeMapping():
    # 关系映射对象
    def __init__(self, tot_arch_type):
        self.arch_dict = {}
        for i in range(len(tot_arch_type)):
            # f(建筑类型) = 建筑类型编号
            self.arch_dict[tot_arch_type[i]] = i
        return

    def archToIndex(self, archType):
        return self.arch_dict[archType]

class Path(object):
    ' 路径对象描述 '
    def __init__(self):
        self.shortestPaths = {}
    
def testNode(node):
    print('testNode:')
    print(node.activity)
    print(node.domain)
    print([p for p in node.place])
    print(node.isDup)

def testParent(parent):
    print(parent.name)
    testNode(parent.job)
    testNode(parent.hobby)
    testNode(parent.eat)
    testNode(parent.sleep)
    print(parent.breakup)
    print(parent.transType)

def testChild(child):
    """
    print('parentName = ' + child.parent.name)
    print(child.sequence)
    print(child.time)
    print(child.place)
    """
    seqTimePlace_lst = child.getSeqTimePlaceList()
    print("seqClassify:")
    print(seqTimePlace_lst[0])
    print("sequence:")
    print(seqTimePlace_lst[1])
    print("time:")
    print(seqTimePlace_lst[2])
    print("place:")
    print(seqTimePlace_lst[3])
    print("total time = " + str(child.getTotalTime()))


if __name__ == "__main__":
    genicDataLst = [ ['政府官员'],
                     [['处理文件', '接待上访', '走访民众', '会议'],
                      ['3~6', '2~4', '2~4', '0.5~5'],
                      ['政府', '政府', '普通小区~河边旧民居~别墅~农田自建房~工厂~农田~老年活动中心', '政府'],
                      ['是', '是', '否', '是']],
                     [['打牌', '钓鱼', '拜访朋友', '嫖娼', '喝酒'],
                      ['2~5', '1.5~4', '2~6', '0.5~10', '2~5'],
                      ['棋牌室', '鱼塘', '普通小区~河边旧民居~别墅~工厂~茶馆', '别墅~洗浴中心~宾馆', '小饭馆'],
                      ['否', '是', '否', '否', '否']],
                     [['面馆早饭', '机构食堂', '餐馆吃饭', '回家吃饭'],
                      ['0.2~1', '0.2~1.5', '0.5~3', '0.5~3'],
                      ['小饭馆', '政府', '小饭馆', '别墅'],
                      ['是', '是', '否', '是']],
                     [['回家睡觉', '暂住宾馆', '夜总会玩乐'],
                      ['7~10', '7~11', '7~11'],
                      ['别墅', '宾馆', '洗浴中心'],
                      ['是', '是', '是']],
                     ['6:00-9:30'],
                     ['走路', '班车', '汽车']]
    tot_arch_type = ['普通小区', '河边旧民居', '别墅', '船', '农田自建房', '工厂', '菜市场',
                     '宾馆', '小饭馆', '农田', '学校', '警署', '老年活动中心', '医院', '政府',
                     '棋牌室', '公园', '超市', '茶馆', '网吧', '鱼塘', '洗浴中心','咖啡馆']
    mapping = TypeMapping(tot_arch_type)
    parent = Parent(genicDataLst, mapping)
    # testParent(parent)
    child = Child(parent)
    testChild(child)

"""
if __name__ == "__main__":

    genicStr_lst = []    # 所有职业基因条
    tot_num = 1000       # 总人数
    num_scale_lst = []   # 各职业对应的人数比例
    # 传入所有职业的基因条, 得到所有职业的父类实例
    parent_lst = [Parent(s) for s in genicStr_lst]
    # 根据总人数和分配比得到每个职业的人数
    num_lst = [int(x * tot_num) for x in num_scale_lst]
    # 根据每个职业的人数和已经构造好的父类, 构造一定数量的子类实例
    children_dict = {}   # 职业序号为key的所有人对象
    for i in range(len(parent_lst)):
       parent = parent_lst[i]
       child_lst = [Child(parent) for num in num_lst]   # error
       children_dict[i] = child_lst
    # 索引得到每个实例人的事件-时长-地点列表
    for key in children_dict:
        print()
        for person in children_dict[key]:
            print()
            print("name : " + person.parent.name)
            print("sequence : " + person.sequence)
            print("time: " + person.time)
            print("place: " + person.space)
"""
    
"""
[['政府官员'], ['处理文件', '接待上访', '走访民众', '会议'], ['3~6', '2~4', '2~4', '0.5~5'], ['政府', '政府', '普通小区~河边旧民居~别墅~农田自建房~工厂~农田~老年活动中心', '政府'], ['是', '是', '否', '是'],
['打牌', '钓鱼', '拜访朋友', '嫖娼', '喝酒'], ['2~5', '1.5~4', '2~6', '0.5~10', '2~5'], ['棋牌室', '鱼塘', '普通小区~河边旧民居~别墅~工厂~茶馆', '别墅~洗浴中心~宾馆', '小饭馆'], ['否', '是', '否', '否', '否'], ['面馆早饭', '机构食堂', '餐馆吃饭', '回家吃饭'], ['0.2~1', '0.2~1.5', '0.5~3', '0.5~3'], ['小饭馆', '政府', '小饭馆', '别墅'], ['是', '是', '否', '是'], ['回家睡觉', '暂住宾馆', '夜总会玩乐'], ['7~10', '7~11', '7~11'], ['别墅', '宾馆', '洗浴中心'], ['是', '是', '是'], ['6:00-9:30'], ['走路', '班车', '汽车']]
"""
