"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""
# -*- coding: UTF-8 -*-
__author__ = "htwt"

import rhinoscriptsyntax as rs
import os
import shutil

# 提取该物件的图层名字(放在数组中)
def getObjectLayerName():
	id = rs.GetObject("Please select a object")
	if id: return rs.ObjectLayer(id)

# 图层名字转换成路径
def layerNameToPath(rootPath, layerName):
	s_lst = layerName.split('::')
	finalPath = rootPath
	print(finalPath)
	for i in range(1, len(s_lst)):
		finalPath = os.path.join(finalPath, s_lst[i])
	return finalPath

# 通过路径打开文件
def viewPic():
	os.system('open /Users/htwt/timspace/arch/town-design/CY/M-08/01/01.png /Users/htwt/timspace/arch/town-design/CY/M-08/01/02.png')
	return


if (flag):
	layerNames = getObjectLayerName()
	a = layerNames
	rootPath = os.path.abspath('.')
	finalPath = layerNameToPath(rootPath, layerNames)
	a = finalPath
	#viewPic(finalPath)
