#-*- coding: utf-8 -*-
from openpyxl import load_workbook

def getColumnValueList(booksheet, column, start_row):
    # 读取一个booksheet的某一列的值, 可以标记头行
    lst = []
    row = start_row
    while (1):
        value = booksheet.cell(row, column).value
        if (value == None):
            break
        lst.append(value)
        row = row + 1
    return lst



if __name__ == '__main__':
    wb = load_workbook('/Users/htwt/Desktop/20181019_totalGenics.xlsx')
    sheets = wb.sheetnames
    # 表头
    sheet_head = sheets[0]
    booksheet = wb[sheet_head]
    tot_arch_type = getColumnValueList(booksheet, 5, 2)   # 所有建筑类型
    tot_job_type = getColumnValueList(booksheet, 6, 2)    # 所有职业类型
    tot_trans_type = getColumnValueList(booksheet, 7, 2)  # 所有出行方式类型
    tot_trans_speed  = getColumnValueList(booksheet, 8, 2)  # 所有出行方式速度

    genicDataLst_lst = []   # 存放所有职业的数据list的list
    for sheetName in wb.sheetnames[1:]:
        lst = []
        booksheet = wb[sheetName]
        jobName = getColumnValueList(booksheet, 1, 3)    # 该职业名字
        lst.append(jobName)
        # 每一个分类结构放在一个list下
        for i in range(15)[2:14:4]:  # [2, 6, 10, 14]
            activity = getColumnValueList(booksheet, i, 3)
            domain = getColumnValueList(booksheet, i+1, 3)
            place = getColumnValueList(booksheet, i+2, 3)
            isDup = getColumnValueList(booksheet, i+3, 3)
            node_lst = [activity, domain, place, isDup]
            lst.append(node_lst)
        breakup = getColumnValueList(booksheet, 18, 3)
        trans_type = getColumnValueList(booksheet, 19, 3)
        lst.append(breakup)
        lst.append(trans_type)
        
        genicDataLst_lst.append(lst)
    print(genicDataLst_lst)
    
