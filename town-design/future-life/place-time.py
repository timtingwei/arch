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

    job_dict = {}
    place_dict = {}
    gene_str_lst = []
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
            gene_str_lst.append(gene_str)

        for key in job_dict.keys():
            output_worksheet.write(job_dict[key], worksheet.ncols+1, key)
        for key in place_dict.keys():
            output_worksheet.write(place_dict[key], worksheet.ncols+2, key)
    output_workbook.save(output_file)
    #return gene_str_lst

def getDataFromExcel():
    # 从excel读取数据(这段关联性不好)
    gene_str_lst = []
    scale_lst = []
    sumCnt = 0
    arr1 = {}
    m = 0     # 时段个数
    n = 15     # 直接给了地块个数, 后面改回来
    hash_n = {}  # 用于求地块个数的Hash表, 也可以在表中直接写

    input_file = 'place-time_data.xlsx'

    with open_workbook(input_file) as workbook:
        worksheet = workbook.sheet_by_name('arr1')
        # 不计第一行的变量名
        col_arr1 = 2
        for row_index in range(1, worksheet.nrows):
            value = worksheet.cell_value(row_index, col_arr1)
            if (value == ''): continue
            arr1[row_index] = value
            #hash_n[value] = 1
        worksheet = workbook.sheet_by_name('scale')
        col_scale = 1
        col_sum = 2
        for row_index in range(1, worksheet.nrows):
            value = worksheet.cell_value(row_index, col_scale)
            if (value == ''): continue
            scale_lst.append(value)
        sumCnt = worksheet.cell_value(1, col_sum)
        
    #n = len(hash_n.keys())
    #print(hash_n.keys())
    
    input_file = 'place-time_data_output.xlsx'
    with open_workbook(input_file) as workbook:
        worksheet = workbook.sheet_by_name('space-time_output')
        col_gene = 9
        for row_index in range(1, worksheet.nrows):
            value = worksheet.cell_value(row_index, col_gene)
            if (value == ''): continue
            if (m == 0):    # 时段个数未被计算
                m = len(value.split('/', 1)[1].split('-'))
            gene_str_lst.append(value)

    

    return gene_str_lst, scale_lst, sumCnt, arr1, m, n

    

def Hash(key, arr1):
    # 实际场所->地块编号
    # return hash2(hash1(key, arr1), arr2)  暂时还用不到hash2
    return hash1(key, arr1)

def hash1(key, arr1):
    # 实际场所->场所分类, arr1是xl中导出的映射表
    return arr1[key]

def hash2(key, arr2):
    # 场所分类->地块编号, arr2是xl中导出的映射表
    lst = arr2[key]
    return lst[random.randrange(0, len(lst))]


def getDkrs(gene_str_basic_lst, scale_lst, sumCnt, m, n, arr1):
    # m是地块数
    # n是时段个数, (修改成从excel中读入的参数)
    # n = 8;
    dict_rs = {}
    for i in range(1, m+1):
        dict_rs[i] = {}
        for j in range(0, n):
            dict_rs[i][j] = 0
    
    # 计算各个职业对应人数
    lstSum = sum(scale_lst)
    #sum += x for x in scale_lst;
    cnt_lst = [int(scale/lstSum*sumCnt) for scale in scale_lst]
    # 得到地块-时段字典
    for i in range(len(gene_str_basic_lst)):
        gene_str = gene_str_basic_lst[i]
        place_lst = gene_str.split('/', 1)[1].split('-')
        for time in range(n):
            dk = Hash(int(place_lst[time]), arr1)
            if not dk in dict_rs:
                print("error not dk in dict_rs")
                continue
            #if not dk in dict_rs:
            #    dict_rs[dk] = {}
            if not time in dict_rs[dk]:
                dict_rs[dk][time] = 0
            dict_rs[dk][time] += cnt_lst[i]
    return dict_rs    # 返回地块-时段Hash表

def printDkrs(dict_rs, m, n):
    # 打印地块-时段表, m是地块数, n是时段数
    fo = open("dk-data_output.txt", "w")
    for dk in range(1, m+1):
        p_str = ''
        for time in range(0, n):
            if (time): p_str += ','
            #print(str(dict_rs[dk][time]))
            p_str += str(dict_rs[dk][time])
        print(p_str)
        fo.write(p_str+'\n')
    fo.close()


# 根据职业人数拷贝基因条
def generateGeneLst(gene_str_basic_lst, scale_lst, sumCnt):
    gene_str_lst = []
    sum = 0
    for x in scale_lst:
        sum += x
    for i in range(len(scale_lst)):
        for j in range(int(scale_lst[i]/sum*sumCnt)):
            gene_str_lst.append(gene_str_basic_lst[i])
    return gene_str_lst

# 将所有基因条中时段-场所数据存入dict_place, 计算时段-地块存入dict-dk
def getGeneDict(gene_str_lst, arr1):
    dict_place = {}
    dict_dk = {}
    for gene_str in gene_str_lst:
        #print(gene_str.split('/', 1))
        place_lst = gene_str.split('/', 1)[1].split('-')
        for i in range(len(place_lst)):
            if i in dict_dk:
                dict_dk[i].append(Hash(int(place_lst[i]), arr1))
            else:
                dict_dk[i] = [Hash(int(place_lst[i]), arr1)]
    return dict_dk

# 选择不同时段统计该时段各地块人数
# O(n)
def count(dict_dk, time, n):
    #time: 时段序号, n: 地块总数
    if time in dict_dk:
        return [dict_dk[time].count(i) for i in range(1, n+1)]
    else:
        print("count() error!\n")
        return []

# 得到n个地块, m个时段的数据
# O(n)
def getMoreCount(dict_dk, n, m):
    dict_dkrs = {}
    for i in range(n):
        dict_dkrs[i] = []    # 在字典中创建空表

    for time in range(m):
        lst = count(dict_dk, time, n)    # 一个时段不同地块人数
        for i in range(n):
            
            dict_dkrs[i].append(lst[i])
    # file output
    fo = open("dk-data_output.txt", "w")
    for i in range(n):
        p_str = ''
        for j in range(len(dict_dkrs[i])):
            if (j): p_str += ','
            p_str += str(dict_dkrs[i][j])
        print(p_str)
        fo.write(p_str+'\n')
    fo.close()


def main1():
    excel_op()
    n = 0; m = 0   # n是地块个数, m是时段个数
    gene_str_basic_lst, scale_lst, sumCnt, arr1, m, n = getDataFromExcel()
    gene_str_lst = generateGeneLst(gene_str_basic_lst, scale_lst, sumCnt)
    dict_dk = getGeneDict(gene_str_lst, arr1)
    #print(m, n)
    getMoreCount(dict_dk, n, m)



def main2():
    excel_op()
    n = 0; m = 0   # n是地块个数, m是时段个数
    gene_str_basic_lst, scale_lst, sumCnt, arr1, m, n = getDataFromExcel()
    dict_dkrs = getDkrs(gene_str_basic_lst, scale_lst, sumCnt, n, m, arr1)
    #dict_dk, m = getGeneDict(gene_str_lst, arr1)
    #print(m, n)
    #getMoreCount(dict_dk, n, m)
    printDkrs(dict_dkrs, n, m)

main2()
