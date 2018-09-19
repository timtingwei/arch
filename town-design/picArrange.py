"""Provides a scripting component.
    Inputs:
        flag: The x script variable
        rootpath: The y script variable
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
	finalPath =rootPath
	print(finalPath)
	for i in range(1, len(s_lst)):
		finalPath = os.path.join(finalPath, s_lst[i])
	return finalPath

# 通过路径打开多个文件
def viewPic(prevPath):
	# 得到文件夹下照片数量cnt
	L = []
	for root, dirs, files in os.walk(prevPath):
		for file in files:
			if os.path.splitext(file)[1] == '.png':					L.append(os.path.join(root, file))
	# join中间添加空格
	open_sh = 'open'
	for fpath in L:
		print('fpath = ' + fpath)
		#appendPath = os.path.join(prevPath, cnt+1)
		open_sh += ' ' + fpath
		#os.system('open /Users/htwt/timspace/arch/town-design/CY/M-08/01/01.png /Users/htwt/timspace/arch/town-design/CY/M-08/01/02.png')
	print(open_sh)
	os.system(open_sh)


if (flag):
	layerNames = getObjectLayerName()
	a = layerNames
	print(a)
	finalPath = layerNameToPath(rootPath, layerNames)
	a = finalPath
	viewPic(finalPath)
