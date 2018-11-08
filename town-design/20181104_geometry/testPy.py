#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 用于测试python的各种语法

from geometry import Point2D, PointVec, Vector, VectorTwoPts, RectangleCornerPoint, RectangleEdgePoint, Phrase, Polyline, Rectangle, RectangleRelation, ReverseVector

"""
class AttrDisplay:
    def gatherAttrs(self):
        return ', '.join("{} = {}"
                         .format(k, getattr(self, k))
                         for k in self.__dict__.keys())
        #for k in self.__dict__.keys():
        #    item = "{} = {}".format(k, getattr(self, k))
        #    s.join(item)
        #print(s)
        #return s

    def __str__(self):
        s = "[{}: {}]".format(self.__class__.__name__, self.gatherAttrs())
        return s

class Parent(AttrDisplay, object):
    def __init__(self, a):
        self.a = a
        self.b_str = 'str in parent'
        return

class Animal(AttrDisplay, object):
    def __init__(self, name):
        self.name = name
        self.female = True
    
class Child(Parent, AttrDisplay):
    def __init__(self, value, likeAnimal_lst):
        self.value = value
        self.likeAnimal = likeAnimal_lst
        return

class Merge(AttrDisplay, object):
    def __init__(self, child, parent):
        self.child = child
        self.parent = parent

def main():
    p = Parent(5)
    #print(p.__dict__.keys())
    animal1, animal2 = Animal('dog'), Animal('cat')
    animal_lst = [animal1, animal2]
    c = Child(2, animal_lst)
    merge_instance = Merge(c, p)
    #print(p)
    #print(c)
    print(merge_instance)
    #print(p)
    #print(c)
    
    return
"""
def testVector():
    vec = Vector(3.2, 1.1)
    #reverse_vec = vec.reverse()
    reverse_vec = ReverseVector(vec)
    print(vec)
    print(reverse_vec)
    return vec

def main():
    testVector()
    

if __name__ == '__main__':
    main()
