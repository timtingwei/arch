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
        breakup = [0]*10
        transType = [0]*10

