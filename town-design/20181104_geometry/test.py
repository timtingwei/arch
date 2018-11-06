#!/usr/bin/env python
#-*- coding: utf-8 -*-

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

if __name__ == '__main__':
    main()
    
