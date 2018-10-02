# -*- coding: utf-8 -*-
"""Provides a scripting component.
    依赖xlrd和xlwt, 确认~\Rhino 6\Plug-ins\IronPython\Lib中存在他们
    Inputs:
        Write: 
        FilepPath: 
        WorkSheetName:
        Column:
        StartRow:
        IsStructed: 是否保留结构
    Output:
        out: The a output variable"""

__author__ = "mituh"
__version__ = "2018.10.02"

import rhinoscriptsyntax as rs
from xlrd import open_workbook
#from xlwt import Workbook
from xlutils.copy import copy

def find_sheet_index(sheetName, rbook):
    sheet_i = 0
    names = rbook.sheet_names()
    for i in range(len(names)):
        if (names[i] == sheetName):
            sheet_i = i
            return i
    return -1

def main():
    rbook = open_workbook(FilePath)
    workbook = copy(rbook)
    sheet_i = find_sheet_index(WorkSheetName, rbook)
    if (sheet_i == -1):
        print('Error')
        return
    worksheet = workbook.get_sheet(sheet_i)
    worksheet.write(StartRow-1, Column-1, Table)
    DataStartRow = StartRow + 1
    for row_index in range(DataStartRow, DataStartRow+len(Data)):
        value = Data[row_index-DataStartRow]
        if (not IsStructed and value == ''):continue;
        worksheet.write(row_index-1, Column-1, value)
    workbook.save(FilePath)
    print("Ok")

if (Write):
    main()
