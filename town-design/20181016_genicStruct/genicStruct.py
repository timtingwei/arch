#-*- coding=utf-8 -*-
# 基因条构造
# 工作-爱好-吃饭-睡觉构造
class Node():
    def __init__(self, subStr):
        self.activity = []
        self.domain = []
        self.place = []
        self.isDup = []
    activity = []  # 工作, 爱好, 吃饭, 睡觉的事件
    domain = []    # 时间区间
    place = []     # 地点
    isDup = []     # 是否关联
class Parent():
    ' 基因库中一条基因对应的基类 '
    name = ''
    job = Object()
    hobby = Object()
    eat = Object()
    sleep = Object()
    breakup = []    # 起床点时间点区间
    transType = []  # 出行方式
    def __init__(self, genicStr):
        # 父类的构造函数
        self.job = Node(subStr1)
        self.hobby = Node(subStr2)
        self.eat = Node(subStr3)
        self.sleep = Node(subStr4)
        self.breakup = stoi(subStr5)
        self.transType = stoi(subStr6)

class Child():
    parent = Object()
    #seqClassify = []
    sequence = []  # 事件序列
    time = []      # 事件对应的时段值
    place = []     # 事件对应的建筑类型序号, 建筑序号
    def __init__(self, parent):
        self.parent = parent
        self.seqClassify = [2, 0, 2, 1, 2, 1, 3]   # 吃饭, 事件, 吃饭, 事件, 吃饭, 睡觉
        self.getActivityTimeSeq()

    def getActivityTimeSeq():
        # 得到每个人的事件时长地点, 三个列表

if __name == "__main__":
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
       child_lst = [Child(parent) for num in num_lst]
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
# 由基因条字符串初始化基因条对象:
def CreatePersonFromStr(genicStr):
    person = Person()
    return person

# 由数值列表初始化基因条对象:
def CreatePersonFromValue(lst1, lst2, lst3, lst4):
    person = Person()
    return person

# 获得职业, 区间, 地点, 出行方式的中文->序号映射字典

# 获得职业, 区间, 地点, 出行方式的序号->中文映射字典

# 将整数转化成指定长度的字符串
def iToLenStr(int_v, length):
    temp = str(int_v)
    delta = length - len(temp)
    if delta > 0:
        return temp + '0'*delta
    else:
        print("Error!"); return;

# 把Node实例折叠成基因条
def flodNodeToGenicStr(node):
    temp = ''
    n = len(node.activity)
    for i in range(n):  # 事件
        temp += iToLenStr(node.activity[i], 1)
    temp += ' '*(10-n)*1
    for i in range(n):  # 时间区间
        temp += iToLenStr(node.domain[i][0], 2)
        temp += iToLenStr(node.domain[i][1], 2)
    temp += ' '*(10-n)*4
    for i in range(n):  # 地点
        m = len(n.place[i])
        for j in range(m):
            temp += iToLenStr(node.place[i][j], 2)
        temp += ' '*(10-m)*2
    temp += ' '*(10-n)*20
    for i in range(n):
        temp += iToLenStr(node.isDup[i], 1)
    temp += ' '*(10-n)*1
    return temp
    
        

# 把类对象实例折叠成基因条
def flodPersonToGenicStr(person):
    temp = ''
    # 职业名字
    temp += iToLenStr(person.name, 2)

    attr_lst = [person.Job, person.Hobby, person.Eat, person.Sleep]
    for attr in attr_lst:  # 工作, 爱好, 吃饭, 睡觉
        temp += flodNodeToGenicStr(attr_lst)
    for edge in person.breakup:  # 起床区间
        temp += iToLenStr(edge, 2)
    n_transType = len(person.transType)  # 出行方式
    for i in range(n_transType):
        temp += iToLenStr(person.transType[i], 1)
    temp += ' '*(10-n_transType)
    return temp
"""
