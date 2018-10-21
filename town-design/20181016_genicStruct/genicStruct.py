#!/usr/bin/env python
#-*- coding: utf-8 -*-
import random
import Queue
import readDataFromExcel
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
        self.trans_time = []  # 储存与地点序列匹配的交通时间
        self.breakup = 0.0    # 起床时间点
        # self.weight_data = {0: 10, 1: 14, 2: 15, 3:22, 4:9, 5:12, 6:5}  # 事件权重, 暂时随机分配
        self.weight_data = {0: 20, 1: 15, 2:10 , 3:9, 4:6, 5:5, 6:5}  # 事件权重, 暂时随机分配
        self.isArrangeValid = False    # 人的事件时间地点安排表是否合理
        # 分配事件对应的分类
        self.getSeqClassify()
        #self.seqClassify = [2, 0, 2, 1, 2, 1, 3]   # 吃饭, 事件, 吃饭, 事件, 吃饭, 事件, 睡觉
        # 按照的分配事件类序, 人的一日三餐保证睡眠, 粗略分配事件时刻地点表
        # self.arrangeActivityTimeSeq(num_lst)
        self.arrangeActivityTimeSeq()

        # 根据事件发生的地点, 安排交通事件, 
        self.arrangeTransActivity()
        # 得到总时间, 剩余时间是否满足睡眠区间, 压缩或者扩展事件时间
        self.adjustActivityTime()
        # 选择起床时间点
        self.breakup = self.selectBreakupTime()
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
        # 求出所有的出行方式速度
        trans_speed_lst = [self.parent.relationMapping.getTransSpeedFromName(trans_type)*3.6
                           for trans_type in self.parent.transType]
        min_speed, max_speed = min(trans_speed_lst), max(trans_speed_lst)
        # 保证睡眠的一天事儿
        for i in range(len(self.place)-1):
            # distance = self.parent.relationMapping.getNodeShortestDistance([self.place[i], self.place[i+1]])
            distance = random.uniform(0.5, 5)    # 在0.5~5之间随机
            speed = 0.0
            # 1km以内走路, 1km以上选择用最快交通工具
            speed = min_speed if distance < 1.0 else max_speed
            time = distance / speed
            self.trans_time.append(time)
        
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
        
            

class TypeMapping():
    # 关系映射对象, 用于查表
    def __init__(self, tot_arch_type, tot_trans_type, tot_job_type, tot_trans_speed, tot_node_path, tot_block_num):
        self.arch_dict = {}
        self.arch_type = tot_arch_type
        for i in range(len(tot_arch_type)):
            # f(建筑类型) = 建筑类型编号
            self.arch_dict[tot_arch_type[i]] = i
        self.node_path = tot_node_path   # {a,b: [[[nodeOrder], d1], [], []], []}
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
        # node_pair: [node_i1, node_i2] -> key = node1, node2
        s_node = str(node_pair[0]) + ',' + str(node_pair[1])
        return self.node_path[s_node]

    def getNodeShortestDistance(self, node_pair):
        node_paths = self.nodeToPath(node_pair)
        # 根据带距离的路径结点, 选择最近的距离
        #node_path = [nodes, distances]
        return node_pathes[0][1]

    def getTransSpeedFromName(self, trans_type):
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


if __name__ == "__main__":
    """
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
                      ['7~9', '7~9', '7~9'],
                      ['别墅', '宾馆', '洗浴中心'],
                      ['是', '是', '是']],
                     ['6:00-9:30'],
                     ['走路', '公交车', '汽车']]
    tot_arch_type = ['普通小区', '河边旧民居', '别墅', '船', '农田自建房', '工厂', '菜市场',
                     '宾馆', '小饭馆', '农田', '学校', '警署', '老年活动中心', '医院', '政府',
                     '棋牌室', '公园', '超市', '茶馆', '网吧', '鱼塘', '洗浴中心','咖啡馆']
    tot_job_type = ['工厂叉车司机', '地头混混', '幼儿园老师', '啃老族', '打零工', '扫地工人',
                    '水果小贩', '小老板', '流浪汉', '快递员', '健身教练', '出租车司机',
                    '养蜂人', '小学生', '中学生', '工厂工人', '片警', '退休', '政府官员',
                    '上市公司老板', '渔民', '厂长', '货车司机', '种地农民', '幼儿园清洁工',
                    '中心学校校长', '幼儿园学生', '学校厨师长', '退休老人', '老年服务中心主管',
                    '村支书', '派出所民警', '病人', '医生', '水产养殖户', '家庭主妇', '旅游者']
    tot_trans_type = ['走路', '自行车', '电瓶车', '公交车', '汽车']
    tot_trans_speed = [1.2, 5, 1.8, 12.5, 16.7]
    """
    filepath = '/Users/htwt/Desktop/20181019_totalGenics.xls'
    genicDataLst_lst, tot_job_scale, tot_block_num, tot_arch_type, tot_job_type, tot_trans_type, tot_trans_speed = readDataFromExcel.read(filepath)
    genicDataLst = genicDataLst_lst[19]   # 选取其中一种职业
    tot_node_path = {}
    mapping = TypeMapping(tot_arch_type, tot_trans_type, tot_job_type, tot_trans_speed, tot_node_path, tot_block_num)
    parent = Parent(genicDataLst, mapping)
    testParent(parent)
    child = Child(parent)
    testChild(child)
    #print(readDataFromExcel.read())



"""
if __name__ == "__main__":
    filepath = '/Users/htwt/Desktop/20181019_totalGenics.xls'
    genicDataLst_lst, tot_job_scale, tot_block_num, tot_arch_type, tot_job_type, tot_trans_type, tot_trans_speed = readDataFromExcel.read(filepath)
    tot_node_path = {}
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
    print(num_lst)

    # 根据每个职业的人数和已经构造好的父类, 构造一定数量的子类实例
    children_dict = {}   # 职业序号为key的所有人对象
    for i in range(len(parent_lst)):
       parent = parent_lst[i]
       child_lst =  [Child(parent) for j in range(num_lst[i])]
       children_dict[i] = child_lst
    # 索引得到每个实例人的事件-时长-地点列表
    for key in children_dict:
        print(key)
        for person in children_dict[key]:
            print()
            print('name:')
            print(person.parent.name.encode('utf-8'))
            print("sequence:")
            print(person.sequence)
            print("time:")
            print(person.time)
            print("place:")
            print(person.place)
"""

    
"""
[['政府官员'], ['处理文件', '接待上访', '走访民众', '会议'], ['3~6', '2~4', '2~4', '0.5~5'], ['政府', '政府', '普通小区~河边旧民居~别墅~农田自建房~工厂~农田~老年活动中心', '政府'], ['是', '是', '否', '是'],
['打牌', '钓鱼', '拜访朋友', '嫖娼', '喝酒'], ['2~5', '1.5~4', '2~6', '0.5~10', '2~5'], ['棋牌室', '鱼塘', '普通小区~河边旧民居~别墅~工厂~茶馆', '别墅~洗浴中心~宾馆', '小饭馆'], ['否', '是', '否', '否', '否'], ['面馆早饭', '机构食堂', '餐馆吃饭', '回家吃饭'], ['0.2~1', '0.2~1.5', '0.5~3', '0.5~3'], ['小饭馆', '政府', '小饭馆', '别墅'], ['是', '是', '否', '是'], ['回家睡觉', '暂住宾馆', '夜总会玩乐'], ['7~10', '7~11', '7~11'], ['别墅', '宾馆', '洗浴中心'], ['是', '是', '是'], ['6:00-9:30'], ['走路', '班车', '汽车']]
"""
