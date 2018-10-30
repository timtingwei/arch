#!/usr/bin/env python
#-*- coding: utf-8 -*-
import blockArrange

def foo1():
    # 所有建筑类型建筑面积
    tot_arch_type_area_lst = [3000, 5000, 6000]
    # 地块总面积
    tot_block_area = 4000.20
    # 已经存在地块建筑面积
    tot_exist_block_area = None
    # 已经存在地块占地面积
    tot_exist_block_building_area = None
    # 建筑类型
    arch_type_lst = [0, 3, 8]
    # 容积率
    plot_ratio = None
    # 覆盖率
    building_ratio = None
    # 层高
    arch_floor_lst = [2, 1, 3]
    # 栋数
    arch_num_lst = [1, 1, 1]
    # 底平面面积
    arch_plane_area_lst = [230.2, 300.5, 180.0]
    # 各类型建筑面积
    arch_type_area_lst = None
    # 各类型占地面积
    arch_type_building_area_lst = None
    # 占地面积
    scale_lst = None
    rst = blockArrange.arrange(
        tot_arch_type_area_lst, tot_block_area,
        tot_exist_block_area, tot_exist_block_building_area,
        arch_type_lst, plot_ratio, building_ratio,
        arch_floor_lst, arch_num_lst, arch_plane_area_lst,
        arch_type_area_lst, arch_type_building_area_lst,
        scale_lst)
    return rst

def foo2():
    # 所有建筑类型建筑面积
    tot_arch_type_area_lst = [300, 400]
    # 地块总面积
    tot_block_area = 300
    # 已经存在地块建筑面积
    tot_exist_block_area = None
    # 已经存在地块占地面积
    tot_exist_block_building_area = None
    # 建筑类型
    arch_type_lst = [0, 1]
    # 容积率
    plot_ratio = None
    # 覆盖率
    building_ratio = None
    # 层高
    arch_floor_lst = [2, 3]
    # 栋数
    arch_num_lst = [2, 2]
    # 底平面面积
    arch_plane_area_lst = None
    # 各类型建筑面积
    arch_type_area_lst = None
    # 各类型占地面积
    arch_type_building_area_lst = [40.0, 30.2]
    # 占地面积
    scale_lst = None
    rst = blockArrange.arrange(
        tot_arch_type_area_lst, tot_block_area,
        tot_exist_block_area, tot_exist_block_building_area,
        arch_type_lst, plot_ratio, building_ratio,
        arch_floor_lst, arch_num_lst, arch_plane_area_lst,
        arch_type_area_lst, arch_type_building_area_lst,
        scale_lst)
    return rst

def foo3():
    # 所有建筑类型建筑面积
    tot_arch_type_area_lst = [330, 420]
    # 地块总面积
    tot_block_area = 300
    # 已经存在地块建筑面积
    tot_exist_block_area = None
    # 已经存在地块占地面积
    tot_exist_block_building_area = None
    # 建筑类型
    arch_type_lst = [0, 1]
    # 容积率
    plot_ratio = None
    # 覆盖率
    building_ratio = None
    # 层高
    arch_floor_lst = [2, 3]
    # 栋数
    arch_num_lst = [3, 2]
    # 底平面面积
    arch_plane_area_lst = None
    # 各类型建筑面积
    arch_type_area_lst = None
    # 各类型占地面积
    arch_type_building_area_lst = [200, 30.2]
    # 占地面积
    scale_lst = None
    rst = blockArrange.arrange(
        tot_arch_type_area_lst, tot_block_area,
        tot_exist_block_area, tot_exist_block_building_area,
        arch_type_lst, plot_ratio, building_ratio,
        arch_floor_lst, arch_num_lst, arch_plane_area_lst,
        arch_type_area_lst, arch_type_building_area_lst,
        scale_lst)
    return rst

def foo4():
    # 所有建筑类型建筑面积
    tot_arch_type_area_lst = [330, 420]
    # 地块总面积
    tot_block_area = 300
    # 已经存在地块建筑面积
    tot_exist_block_area = None
    # 已经存在地块占地面积
    tot_exist_block_building_area = None
    # 建筑类型
    arch_type_lst = [0, 1]
    # 容积率
    plot_ratio = None
    # 覆盖率
    building_ratio = None
    # 层高
    arch_floor_lst = [2, 3]
    # 栋数
    arch_num_lst = [3, 2]
    # 底平面面积
    arch_plane_area_lst = None
    # 各类型建筑面积
    arch_type_area_lst = None
    # 各类型占地面积
    arch_type_building_area_lst = [200, 30.2]
    # 占地面积
    scale_lst = None
    rst = blockArrange.arrange(
        tot_arch_type_area_lst, tot_block_area,
        tot_exist_block_area, tot_exist_block_building_area,
        arch_type_lst, plot_ratio, building_ratio,
        arch_floor_lst, arch_num_lst, arch_plane_area_lst,
        arch_type_area_lst, arch_type_building_area_lst,
        scale_lst)
    return rst


def print_foo(arch_type_lst, arch_type_area_lst, rest_arch_area_lst, rest_flag_lst, tot_use_block_area, sum_building_area, building_flag, arch_type_building_area_lst, plot_ratio, building_ratio, arch_floor_lst, arch_num_lst, arch_plane_area_lst):
    print('建筑类型:')
    print(arch_type_lst)
    print('各类型建筑面积:')
    print(arch_type_area_lst)
    print('各建筑剩余建筑面积:')
    print(rest_arch_area_lst)
    print('剩余建筑面积是否满足标记:')
    print(rest_flag_lst)
    print('总共可用地块面积:')
    print(tot_use_block_area)
    print('输入建筑总占地面积:')
    print(sum_building_area)
    print('建筑占地是否满足标记:')
    print(building_flag)
    print('各类型占地面积:')
    print(arch_type_building_area_lst)
    print('容积率:')
    print(plot_ratio)
    print('覆盖率:')
    print(building_ratio)
    print('层数:')
    print(arch_floor_lst)
    print('栋数:')
    print(arch_num_lst)
    print('底面积:')
    print(arch_plane_area_lst)
    print('-----:')
    return
    

if __name__ == '__main__':
    #arch_type_lst, arch_type_area_lst, rest_arch_area_lst, rest_flag_lst, tot_use_block_area, sum_building_area, building_flag, arch_type_building_area_lst, plot_ratio, building_ratio, arch_floor_lst, arch_num_lst, arch_plane_area_lst = foo1()
    #print_foo(arch_type_lst, arch_type_area_lst, rest_arch_area_lst, rest_flag_lst, tot_use_block_area, sum_building_area, building_flag, arch_type_building_area_lst, plot_ratio, building_ratio, arch_floor_lst, arch_num_lst, arch_plane_area_lst)
    #arch_type_lst, arch_type_area_lst, rest_arch_area_lst, rest_flag_lst, tot_use_block_area, sum_building_area, building_flag, arch_type_building_area_lst, plot_ratio, building_ratio, arch_floor_lst, arch_num_lst, arch_plane_area_lst = foo2()
    #arch_type_lst, arch_type_area_lst, rest_arch_area_lst, rest_flag_lst, tot_use_block_area, sum_building_area, building_flag, arch_type_building_area_lst, plot_ratio, building_ratio, arch_floor_lst, arch_num_lst, arch_plane_area_lst = foo3()
    arch_type_lst, arch_type_area_lst, rest_arch_area_lst, rest_flag_lst, tot_use_block_area, sum_building_area, building_flag, arch_type_building_area_lst, plot_ratio, building_ratio, arch_floor_lst, arch_num_lst, arch_plane_area_lst = foo4()
    print_foo(arch_type_lst, arch_type_area_lst, rest_arch_area_lst, rest_flag_lst, tot_use_block_area, sum_building_area, building_flag, arch_type_building_area_lst, plot_ratio, building_ratio, arch_floor_lst, arch_num_lst, arch_plane_area_lst)
    
