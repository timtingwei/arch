#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 用于测试python的各种语法



class AttrDisplay:
    def gatherAttrs(self):
        return ', '.join("{} = {}"
                         .format(k, getattr(self, k))
                         for k in self.__dict__.keys())

    def __str__(self):
        s = "[{}: {}]".format(self.__class__.__name__, self.gatherAttrs())
        return s

class Parent(AttrDisplay, object):
    def __init__(self, a):
        self.a = a
        self.b_str = 'str in parent'
        return


class Child(Parent, AttrDisplay):
    def __init__(self, value):
        self.value = value
        return

def main():
    p = Parent(5)
    #print(p.__dict__.keys())
    c = Child(2)
    print(p)
    print(c)
    
    return

if __name__ == '__main__':
    main()
