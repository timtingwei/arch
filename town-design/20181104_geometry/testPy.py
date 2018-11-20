#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 用于测试python的各种语法

#from geometry import Point2D, PointVec, Vector, VectorTwoPts, RectangleCornerPoint, RectangleEdgePoint, Phrase, Polyline, Rectangle, RectangleRelation, ReverseVector

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
"""
def testVector():
    vec = Vector(3.2, 1.1)
    #reverse_vec = vec.reverse()
    reverse_vec = ReverseVector(vec)
    print(vec)
    print(reverse_vec)
    return vec
"""

"""
class Display:
    def display(self):
        if isinstance(self, Parent):
            print(self.a)
        elif isinstance(self, Animal):
            print(self.name)

        return

class Parent(Display, object):
    def __init__(self):
        self.a = 5
        return

class Child(Parent):
    def __init__(self):
        self.b = 6
        super(Child, self).__init__()
        return

class Animal(Display, object):
    def __init__(self, name):
        self.name = name
        return

class Dog(Animal):
    def __init__(self):
        super(Dog, self).__init__('jack')
        self.active = 'wang'
        return



def main():
    c = Child()
    dog = Dog()
    c.display()
    dog.display()
"""

"""
# 测试子类实例如何调用父类的方法
class Parent(object):
    def __init__(self, a):
        self.a = a
        #self.b = self.getName()
    def getName(self):
        print('getName in parent')
        return

class Child(Parent):
    def __init__(self, b):
        # 用超类继承属性
        super(Child, self).__init__(3)
        self.b = b
    def getAge(self):
        print('getAge in child')
        return

def main():
    p = Parent(2)
    child = Child(3)
    child.getName()      # 继承类自然可以调用父类的方法
    print(child.a)
"""

# 测试ReverseVector类和类方法Vector::reverse()的区别, 是否会改变实例对象
from geometry import Vector, ReverseVector

def testReverse():
    vec = Vector(2.0, 3.0)
    reverse_vec = vec.reverse()
    other_vec = ReverseVector(vec)
    print(vec)
    print(reverse_vec)
    print(other_vec)

def main():
    testReverse()


if __name__ == '__main__':
    main()
