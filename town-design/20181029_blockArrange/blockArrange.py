"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "mituh"
__version__ = "2018.10.29"

"""
import rhinoscriptsyntax as rs

# 占地面积, 栋数, 底面积 三元互算
def computeThreeParams(a = 0.0, b = 0, c = 0.0):
    if a and b: c = a / b
    elif a and c: 
        b = int(a / c) + 1
        c = a / b
    elif b and c:  a = b * c
    else: return
    return a, b, c

# 建筑面积, 栋数, 层数, 底面积 四元互算
def computeFourParams(a = 0.0, f = 0, n = 0, pa = 0.0):
    if a and f and n: pa = a/f/n
    elif a and f and pa:
        n = int(a/f/pa)+1
        pa = a/f/n
    elif a and n and pa:
        f = int(a/n/pa)+1
        pa = a/f/n
    elif f and n and pa: a = f*n*pa
    else: return
    return a, f, n, pa


#a, b, c = computeThreeParams(x, y, z)
def main():
    final_arch_rest_area = getRestArea()  # 获得剩余建筑面积
    if (block_tot_area is None) or (tot_arch_area is None):
        print("缺少地块总面积和所有类型建筑可用面积"); return;
    block_use_area = block_tot_area - block_exist_area
    if block_use_area <= 0:
        print('无可用地块面积'); return;
    if arch_type is None:
        print('缺少建筑类型'); return;
    if plot_ration:
        # 确定容积率
    elif building_ratio:
        # 确定覆盖率
    elif arch_floor and arch_n and plane_area:
        # 确定建筑栋数, 层数, 底面积
        print("确定建筑栋数, 层数, 底面积")
        if (len(arch_floor) != len(arch_n)) or (len(arch_n) == len(plane_area)):
            print("多个建筑类型, 栋数, 层数, 底面积数量需要对应"); return
        # 获得建筑面积
        arch_area_lst = []   # 各建筑类型所需的建筑面积
        
        for i in range(len(arch_floor)):
            # 获得建筑面积
            arch_area = computeFourParams(0.0, arch_floor[i], arch_n[i], plane_area[i])[0]
            final_arch_rest_area[i] -= arch_area
            judgeRestArea(final_arch_rest_area[i])
            arch_area_lst.append(arch_area)
        
    return final_arch_type, final_arch_rest_area, final_arch_area, final_arch_space,
        final_arch_plot_ratio, final_building_ratio, final_arch_floor, final_arch_n, final_plane_area

final_arch_type, final_arch_rest_area, final_arch_area, final_arch_space, final_arch_plot_ratio, final_building_ratio, final_arch_floor, final_arch_n, final_plane_area = main()
"""

# test if

def testIf():
    if 1:
        a = 5
    print('a = ' + str(a))

if __name__ == '__main__':
    testIf()
