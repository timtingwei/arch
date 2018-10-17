#-*- coding=utf-8 -*-
# 基因条构造
# 工作-爱好-吃饭-睡觉构造
class Node():

    def __init__(self, subStr):
        self.activity = []
        self.domain = []
        self.place = []
        self.isDup = []
    def __init__(self, subGenicDataLst):
        n = len(subGenicDataLst[0])
        self.activity = [0]*n  # 事件     string   [a1, a2]
        self.domain = [0]*n    # 时间区间  double   [(d1, d2), (d3,d4)]
        self.place = [0]*n     # 地点     string  [[p1, p2], [p3, p4, p5]]
        self.isDup = [0]*n     # 是否关联  int      [0, 1]
        for i in range(n):
            self.activity[i] = (subGenicDataLst[0][i])
            self.domain[i] = (tuple(subGenicDataLst[1][i].split('~')))
            self.place[i] = subGenicDataLst[2][i].split('~')
            self.isDup[i] = 0 if cmp(subGenicDataLst[3][i], '否') == 0 else 1

class Parent():
    ' 基因库中一条基因对应的基类 '
    """
    def __init__(self, genicStr):
        # 父类的构造函数
        self.job = Node(subStr1)
        self.hobby = Node(subStr2)
        self.eat = Node(subStr3)
        self.sleep = Node(subStr4)
        self.breakup = stoi(subStr5)
        self.transType = stoi(subStr6)
    """
    def __init__(self, genicDataLst):
        """
        #genicDataLst = [  [],  [],  [],  [], [], [], []]
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
        """
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

    def convertTimeFormat(self, s):
        # convert 6:30 to 6.5
        lst = s.split(':')
        return int(lst[0]) + int(lst[1])/60
    def getNodeToList(self):
        return [self.job, self.hobby, self.eat, self.sleep]

class Child():
    def __init__(self, parent):
        self.parent = parent
        self.sequence = []  # 事件序列                       # string  [s1, s2, s3, s4]
        self.time = []      # 事件对应的时段值                # double  [t1, t2, t3, t4]
        self.place = []     # 事件对应的建筑类型序号, 建筑序号  # string,int  [[农田, 2], [工厂, 0], [p3,i3], [p4,i4]]
        #self.seqClassify = [2, 0, 2, 1, 2, 1, 3]   # 吃饭, 事件, 吃饭, 事件, 吃饭, 睡觉
        #self.getActivityTimeSeq()

    def getActivityTimeSeq():
        # 得到每个人的事件时长地点, 三个列表
        return

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
    parent = Parent(genicDataLst)
    child = Child(parent)
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


"""
[['政府官员'], ['处理文件', '接待上访', '走访民众', '会议'], ['3~6', '2~4', '2~4', '0.5~5'], ['政府', '政府', '普通小区~河边旧民居~别墅~农田自建房~工厂~农田~老年活动中心', '政府'], ['是', '是', '否', '是'],
['打牌', '钓鱼', '拜访朋友', '嫖娼', '喝酒'], ['2~5', '1.5~4', '2~6', '0.5~10', '2~5'], ['棋牌室', '鱼塘', '普通小区~河边旧民居~别墅~工厂~茶馆', '别墅~洗浴中心~宾馆', '小饭馆'], ['否', '是', '否', '否', '否'], ['面馆早饭', '机构食堂', '餐馆吃饭', '回家吃饭'], ['0.2~1', '0.2~1.5', '0.5~3', '0.5~3'], ['小饭馆', '政府', '小饭馆', '别墅'], ['是', '是', '否', '是'], ['回家睡觉', '暂住宾馆', '夜总会玩乐'], ['7~10', '7~11', '7~11'], ['别墅', '宾馆', '洗浴中心'], ['是', '是', '是'], ['6:00-9:30'], ['走路', '班车', '汽车']]
"""
