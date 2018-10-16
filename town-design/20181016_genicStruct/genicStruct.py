#-*- coding=utf-8 -*-

# 基因条构造
class Node:
    def __init__(self):
        activity = [0]*10
        domain = [0]*10
        place = [0]*10
        isDup = [0]*10
Job = Node
Hobby = Node
Eat = Node
Sleep = Node
class Person:
    def __init__(self):
        name = ''
        Job = Job()
        Hobby = Hobby()
        Eat = Eat()
        Sleep = Sleep()
        breakup = []
        transType = []

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
    """
    for i in range(10):
        if i < len(person.transType):
            temp += iToLenStr(person.transType[i], 1)
        else:
            temp += ' '*1
    """
    n_transType = len(person.transType)  # 出行方式
    for i in range(n_transType):
        temp += iToLenStr(person.transType[i], 1)
    temp += ' '*(10-n_transType)
    return temp
