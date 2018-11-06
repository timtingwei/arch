
"""Provides a scripting component.
    Inputs:
        flag: The x script variable
        rootpath: The y script variable
    Output:
        a: The a output variable"""
__author__ = "htwt"
# -*- coding: UTF-8 -*-

import os
import shutil

import rhinoscriptsyntax as rs


# 提取该物件的图层名字(放在数组中)
def getObjectsLayerNames():
	# 可选择多点, 只能选择点物件, 可预先选择
	obj_ids = rs.GetObjects("Please select points", rs.filter.point, False, True)
	names = []
	for id in obj_ids:
		names.append(rs.ObjectLayer(id))
	return names

# 图层名字转换成路径
def layerNamesToPaths(rootPath, layerNames):
	finalPaths_lst = []
	for layerName in layerNames:
		s_lst = layerName.split('::')
		finalPath = rootPath
		for i in range(1, len(s_lst)):
			finalPath = os.path.join(finalPath, s_lst[i])
		finalPaths_lst.append(finalPath)
		print("finalPath = " + finalPath)
	return finalPaths_lst

# 通过路径打开多个文件
def viewPic(prevPath):
	print("prevPath = " + prevPath)
	# 得到文件夹下照片数量cnt
	L = []
	for root, dirs, files in os.walk(prevPath):
		for file in files:
			suffix = os.path.splitext(file)[1]
			if suffix == '.png' or suffix == '.jpg' or suffix == '.jpeg' or suffix == '.JPG':
				L.append(os.path.join(root, file))
	# join中间添加空格
	open_sh = 'open'
	for fpath in L:
		print('fpath = ' + fpath)
		#appendPath = os.path.join(prevPath, cnt+1)
		open_sh += ' ' + fpath
		#os.system('open /Users/htwt/timspace/arch/town-design/CY/M-08/01/01.png /Users/htwt/timspace/arch/town-design/CY/M-08/01/02.png')
	print("open_sh = " + open_sh)
	os.system(open_sh)


#调用多个路径, 每个路径打开对应的多张照片
def viewMorePathPic(prevPaths_lst):
	for prevPath in prevPaths_lst:
		viewPic(prevPath)

if (flag):
	layerNames = getObjectsLayerNames()
	#a = layerNames
	#print(a)
	finalPaths_lst = layerNamesToPaths(rootPath, layerNames)
	#a = finalPath
	#viewPic(finalPath)
	viewMorePathPic(finalPaths_lst)


# 修改交通组图片编号
# para:
# @input:rootPath
# @output:

def reviseJTfilesNames(rootPath):
    jtPath = os.path.join(rootPath, 'JT')
    for root, dirs, files in os.walk(jtPath):
        for name in files:
            s_lst = os.path.splitext(name)
            if (s_lst[1] == '.jpg'):
                print("name = " + name)
                orig_name = os.path.join(root, name)
                if (int(s_lst[0]) % 3 == 1):
                    os.rename(orig_name, os.path.join(root, '01-前.jpg'))
                elif (int(s_lst[0]) % 3 == 2):
                    os.rename(orig_name, os.path.join(root, '02-右.jpg'))
                elif (int(s_lst[0]) % 3 == 0):
                    os.rename(orig_name, os.path.join(root, '03-左.jpg'))


def reviseJTfileContents(rootPath):
    jtPath = os.path.join(rootPath, 'JT')
    
    #for root, dirs, files in os.walk(jtPath):
    #    for name in dirs:
    #        print(name)
    
    #for x in os.listdir('.'):
    #    print("file = " + x)

    print(jtPath)
    for fileName in os.listdir(jtPath):
        nextPath = os.path.join(jtPath, fileName)
        # 忽略隐藏文件夹
        if not (fileName.startswith('.')):
            # 该层文件夹需要用一个新文件夹来放照片
            wrong_pic = [x for x in os.listdir(nextPath) if os.path.splitext(x)[1]=='.jpg']
            for pic in wrong_pic:
                print("pic = " + pic)
            if (len(wrong_pic) != 0):
                dirPath = os.path.join(nextPath, "01")
                if (not os.path.exists(dirPath)):
                    os.mkdir(dirPath)
                for pic in wrong_pic:
                    shutil.copyfile(os.path.join(nextPath, pic), os.path.join(dirPath, pic))
                    os.remove(os.path.join(nextPath, pic))


def reviseMain():
    #reviseJTfilesNames(rootPath)
    rootPath = '/Users/htwt/timspace/arch/town-design/collection/'
    reviseJTfileContents(rootPath)

# reviseMain()


