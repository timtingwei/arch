# -*- coding: utf-8 -*-

import sys
from xlrd import open_workbook
from xlwt import Workbook
import random


def excel_op():
    input_file = 'place-time_data.xlsx'
    output_file = 'place-time_data_output.xlsx'
    input_workbook = open_workbook(input_file)
    output_workbook = Workbook()
    output_worksheet = output_workbook.add_sheet('space-time_output')
    """
    print('Number of worksheets:', output_workbook.nsheets)
    for worksheet in output_workbook.sheets():
        print("Worksheet name:", worksheet.name, "\tRows:", \
              worksheet.nrows, "\tColumns:", worksheet.ncols)
    """
    job_dict = {}
    place_dict = {}
    print(job_dict.keys())

    with open_workbook(input_file) as workbook:
        worksheet = workbook.sheet_by_name('Sheet1')
        # 不计第一行的变量名
        for row_index in range(1, worksheet.nrows):
            gene_str = ''
            job = worksheet.cell_value(row_index, 0)
            if job in job_dict:
                job_index = job_dict[job]
            else:
                job_dict[job] = len(job_dict.keys())+1
            # 新增职业类写入cell
            # 写入新的cell
            output_worksheet.write(row_index, 0, job_dict[job])
            # 将职业添加到基因条
            gene_str += str(job_dict[job])
            for column_index in range(1, worksheet.ncols):
                # 每一个场所
                place = worksheet.cell_value(row_index, column_index)
                if not place in place_dict:
                    place_dict[place] = len(place_dict.keys())+1
                # 将新增场所类写入cell
                # 写入新的cell
                output_worksheet.write(row_index, column_index, place_dict[place])
                # 将场所添加到基因条
                if (column_index == 1):
                    gene_str += '/'
                else:
                    gene_str += '-'
                gene_str += str(place_dict[place])
            # 将基因条写入cell
            output_worksheet.write(row_index, worksheet.ncols, gene_str)

        for key in job_dict.keys():
            output_worksheet.write(job_dict[key], worksheet.ncols+1, key)
        for key in place_dict.keys():
            output_worksheet.write(place_dict[key], worksheet.ncols+2, key)
    output_workbook.save(output_file)

    return

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

# 得到n个地块, m个时段的数据
def getMoreCount(dict_dk, n, m):
    for i in range(m)


"""
gene_str_lst = ["01/01-02-03-04-05-06-06-06",
                "02/07-07-08-08-05-09-09-07"]
arr1 = [1, 2]           # 场所->场所分类映射
arr2 = [[3, 4],  [5, 7], [3, 4, 6]]   # 场所分类->地块映射
time = 2
n = 7
dict_dk = getGeneDict(gene_str_lst, arr1, arr2)
count(dict_dk, time, n)
"""

dict_tmp = {"tim":1, "a":2, "胡廷威":3}
print(dict_tmp["胡廷威"])
print(dict_tmp.keys())
print(sys.argv[0])
excel_op()
