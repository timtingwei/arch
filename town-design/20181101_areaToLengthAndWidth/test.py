#!/usr/bin/env python
#-*- coding: utf-8 -*-
import areaToLengthAndWidth

def foo():
    area = 200.0
    length_domain = [10, 50]
    width_domain = [5, 30]
    length = 20
    width = 30
    flag = 0
    rst = areaToLengthAndWidth.convertArea(area, length_domain, width_domain, length, width, flag)
    print(rst)

    return


if __name__ == '__main__':
    foo()
    
