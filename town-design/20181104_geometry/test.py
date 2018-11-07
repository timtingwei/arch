#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
class Parent(object):
    def __init__(self, a):
        self.a = a
        return

    def initChildInParent(self, b):
        child = Child(b)
        return child

class Child(object):
    def __init__(self, b):
        self.b = b
        return

def main():
    p = Parent(2)
    print(p.a)
    child = p.initChildInParent(3)
    print(child.b)

"""

class Parent(object):
    def __init__(self, a, length = None):
        self.value = a
        self.length = self.getLength if length is None else length
        return

    def getLength(self):
        length = 77
        return length
class Child(Parent):
    def __init__(self, a):
        self.value = a
        return
        

def main():
    """
    parent = Parent(4)
    jack = Parent(parent.value)
    jack.value = 12
    print(parent.value)
    print(jack.value)

    # test length
    print(parent.length)
    parent = Parent(4, length = 12)
    print(parent.length)
    """
    # test class type
    c = Child(3)
    p = Parent(4)
    print(isinstance(c, Child))
    print(type(c))

if __name__ == '__main__':
    main()
    
