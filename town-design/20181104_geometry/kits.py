#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 定义一些小工具, 将计算逻辑与工具逻辑分开

class AttrDisplay:
    ' 观察实例对象属性的类 '
    def gatherAttrs(self):
        return ', \n'.join("{}= {}"
                         .format('*'+k, getattr(self, k))
                         for k in self.__dict__.keys())

    def __str__(self):
        s = "[{}:\n{}]".format(self.__class__.__name__, self.gatherAttrs())
        return s
