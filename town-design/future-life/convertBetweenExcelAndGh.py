# -*- coding: utf-8 -*-
"""Provides a scripting component.
    依赖xlrd和xlwt, 确认~\Rhino 6\Plug-ins\IronPython\Lib中存在他们
    Inputs:
        read: 
        filepath: 
        worksheetname:
        column:
        startRow:
        endRow:
        isStructed: 是否保留结构
    Output:
        Data: The a output variable"""

__author__ = "chen"
__version__ = "2018.10.02"

import rhinoscriptsyntax as rs
from xlrd import open_workbook
from xlwt import Workbook


def main():
    data = []
    input_file = filepath
    input_workbook = open_workbook(input_file)
    
    with open_workbook(input_file) as workbook:
        # if worksheet.nrows < startRow or worksheet.nrows < endRow or colum    边界条件
        worksheet = workbook.sheet_by_name(worksheetname)
        for row_index in range(startRow, endRow+1):
            value = worksheet.cell_value(row_index-1, column-1)
            if (not isStructed and value == ''):continue;
            data.append(value)
    return data

if (read):
    data = main()
