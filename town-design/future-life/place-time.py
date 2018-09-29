# -*- coding: utf-8 -*-

"""
01/01-02-03-04-05-06-06-06
02/07-07-08-08-05-09-09-07
03/06-10-11-10-12-13-01-01
04/01-01-08-08-08-08-08-01
"""
import random

def Hash(key, arr1, arr2):
    # 实际场所->地块编号
    return hash2(hash1(key, arr1), arr2)

def hash1(key, arr1):
    # 实际场所->场所分类, arr1是xl中导出的映射表
    return arr1[key]

def hash2(key, arr2):
    lst = arr2[key]
    return lst[random.randrange(0, len(lst))]

# 将所有基因条中时段-场所数据存入dict_place, 计算时段-地块存入dict-dk
def getGeneDict(gene_str_lst, arr1, arr2):
    dict_place = {}
    dict_dk = {}
    for gene_str in gene_str_lst:
        place_lst = gene_str.split('/', 1)[1].split('-')
        for i in range(len(place_lst)):
            if i in dict_dk:
                dict_dk[i].append(Hash(int(place_lst[i]), arr1, arr2))
            else:
                dict_dk[i] = [Hash(int(place_lst[i]), arr1, arr2)]
    return dict_dk

# 选择不同时段统计该时段各地块人数
def count(dict_dk, time, n):
    #time: 时段序号, n: 地块总数
    if time in dict_dk:
        return [dict_dk[time].count(i) for i in range(1, n)]
    else:
        print("count() error!\n")
        return []


gene_str_lst = ["01/01-02-03-04-05-06-06-06",
                "02/07-07-08-08-05-09-09-07"]
arr1 = [1, 2]           # 场所->场所分类映射
arr2 = [[3, 4],  [5, 7], [3, 4, 6]]   # 场所分类->地块映射
time = 2
n = 7
dict_dk = getGeneDict(gene_str_lst, arr1, arr2)
count(dict_dk, time, n)
