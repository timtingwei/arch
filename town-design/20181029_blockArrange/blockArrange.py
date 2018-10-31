"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "mituh"
__version__ = "2018.10.29"

def getUseBlockArea(tot_block_area, tot_exist_block_area):
    # 得到实际可用地块占地面积
    if tot_exist_block_area is None: return tot_block_area  # 未输入已存在地块面积时, 用0计算
    else: return tot_block_area - tot_exist_block_area
def getParamsNum(arch_floor_lst, arch_num_lst, arch_plane_area_lst):
    # 得到输入变量有效的个数, 栋数, 层数, 底面积
    num = 0
    if arch_floor_lst: num += 1;
    if arch_num_lst: num += 1;
    if arch_plane_area_lst: num += 1
    return num
    
def fillParamsList(length, arch_type_area_lst, arch_type_building_area_lst, arch_num_lst, arch_floor_lst, arch_plane_area_lst):
    # 根据length长度, 扩展输入为None的值为[0]*length, 便于后面的等价计算
    merge_lst = [arch_type_area_lst, arch_type_building_area_lst, arch_num_lst, arch_floor_lst, arch_plane_area_lst]
    for i in range(len(merge_lst)):
        if merge_lst[i] is None:
            merge_lst[i] = [0]*length if i == 2 or i == 3 else [0.0]*length  # 栋数和层数为int型
    return merge_lst
    

# 占地面积, 栋数, 底面积 三元互算
def computeThreeParams(a = 0.0, b = 0, c = 0.0):
    a, b, c = float(a), int(b), float(c)
    if a and b: c = a / b
    elif a and c: 
        b = int(a / c) + 1
        c = a / b
    elif b and c:  a = b * c
    else: return
    return a, b, c     # building_area, arch_num, arch_plane_area

# 建筑面积, 栋数, 层数, 底面积 四元互算
def computeFourParams(a = 0.0, f = 0, n = 0, pa = 0.0):
    a, f, n, pa = float(a), int(f), int(n), float(pa)
    if a and f and n: pa = a/f/n
    elif a and f and pa:
        n = int(a/f/pa)+1
        pa = a/f/n
    elif a and n and pa:
        f = int(a/n/pa)+1
        pa = a/f/n
    elif f and n and pa: a = f*n*pa
    else: return
    return a, f, n, pa  # area, arch_floor, arch_num, arch_plane_area

def getRatio(sum_arch_area, tot_exist_block_area, tot_block_area):
    # 计算容积率和覆盖率
    if tot_exist_block_area is None: tot_exist_block_area = 0.0   # 不存在按0计算
    return (sum_arch_area + tot_exist_block_area) / tot_block_area

def getAreaFromRatio(plot_ratio, tot_block_area):
    # 通过容积率/覆盖率得到所有输入建筑的总建筑面积/占地面积
    return plot_ratio * tot_block_area

def getAreaListFromScale(sum_arch_area, scale_lst):
    # 通过建筑类型比例和总面积, 得到各建筑类型建筑面积
    return [sum_arch_area * scale for scale in scale_lst]

def arrange(tot_arch_type_area_lst, tot_block_area,
            tot_exist_block_area, tot_exist_block_building_area,
            arch_type_lst, plot_ratio, building_ratio,
            arch_floor_lst, arch_num_lst, arch_plane_area_lst,
            arch_type_area_lst, arch_type_building_area_lst,
            scale_lst):
    """
    @parms:
    tot_arch_type_area_lst, tot_block_area:   # 所有建筑类型建筑面积, 地块总面积
    tot_exist_block_area, tot_exist_block_building_area:  # 已经存在地块建筑面积, 已经存在地块占地面积
    arch_type_lst, plot_ratio, building_ratio: # 建筑类型, 容积率, 覆盖率
    arch_floor_lst, arch_num_lst, arch_plane_area_lst:  # 层高, 栋数, 底平面面积
    arch_type_area_lst, arch_type_building_area_lst:   # 各类型建筑面积, 各类型占地面积
    scale_lst:    占地面积, 建筑面积的在总地块中的分配比例, 在0~1范围内

    @output:
    arch_type_lst, arch_type_area_lst:    建筑类型, 各类型建筑面积
    rest_arch_area_lst, rest_flag_lst:    各建筑剩余建筑面积, 剩余建筑面积是否满足标记
    tot_use_block_area:                   总共可用地块面积
    sum_building_area:                    输入建筑总占地面积
    building_flag, arch_type_building_area_lst:    建筑占地是否满足标记, 各类型占地面积
    plot_ratio, building_ratio,           容积率, 覆盖率
    arch_floor_lst, arch_num_lst, arch_plane_area_lst  层数, 栋数, 底面积
    """
    if not tot_block_area: print("缺少地块总面积"); return;
    if not tot_arch_type_area_lst: print("缺少建筑类型的建筑面积"); return;
    if not arch_type_lst: print("缺少建筑类型"); return;
    tot_use_block_area = getUseBlockArea(tot_block_area, tot_exist_block_area)  # 获得可使用的建筑占地面积
    paramsNum = getParamsNum(arch_floor_lst, arch_num_lst, arch_plane_area_lst)  # 得到输入变量有效的个数
    arch_type_area_lst, arch_type_building_area_lst, arch_num_lst, arch_floor_lst, arch_plane_area_lst = fillParamsList(len(arch_type_lst), arch_type_area_lst, arch_type_building_area_lst, arch_num_lst, arch_floor_lst, arch_plane_area_lst)   # ?: 将None填充成0数组, 实现不太优雅
    building_flag = 0        # 占地面积是否满足标记
    rest_flag_lst = []       # 各建筑类型剩余是否满足标记
    rest_arch_area_lst = []  # 各建筑类型剩余建筑面积
    sum_arch_area = 0.0      # 输入得到总建筑面积
    sum_building_area = 0.0  # 输入得到总地块面积
    if paramsNum == 3:
        # 栋数, 层数, 底面积均存在的情况
        for i in range(len(arch_type_lst)):
            arch_type_area_lst[i] = computeFourParams(arch_type_area_lst[i], arch_floor_lst[i], arch_num_lst[i], arch_plane_area_lst[i])[0]  # 根据另外三个变量得到该类型建筑面积
            rest = tot_arch_type_area_lst[i] - arch_type_area_lst[i]  # 根据可用面积得到剩余面积
            rest_flag = 0 if rest < 0 else 1         # 建筑类型可用建筑面积限制
            rest_arch_area_lst.append(rest)
            rest_flag_lst.append(rest_flag)
            sum_arch_area += arch_type_area_lst[i]   # 输入的各类型总建筑面积
            sum_building_area += computeThreeParams(arch_type_building_area_lst[i], arch_num_lst[i], arch_plane_area_lst[i])[0]                    # 输入的各类型总占地面积
        building_flag = 1 if sum_building_area <= tot_use_block_area else 0  # 现有地块的限制条件
        plot_ratio = getRatio(sum_arch_area, tot_exist_block_area, tot_block_area)  # 计算容积率
        building_ratio = getRatio(sum_building_area, tot_exist_block_building_area, tot_block_area)   # 计算覆盖率
    elif paramsNum == 2:
        # 栋数, 层数, 底面积有且只有两个的情况
        two_params_flag = 0  # 下一层级计算标记
        # ? 判断是短路判断, 是否要做一个输入多个的提示情况?
        if arch_type_area_lst[0]: two_params_flag = 0
        elif arch_type_building_area_lst[0]: two_params_flag = 1
        elif plot_ratio:
            if not scale_lst: print("缺少比例参数"); return;
            two_params_flag = 0
            sum_arch_area = getAreaFromRatio(plot_ratio, tot_block_area)  # 通过容积率得到所有输入建筑的总建筑面积
            arch_type_area_lst = getAreaListFromScale(sum_arch_area, scale_lst)  # 通过建筑类型比例和总面积, 得到各建筑类型建筑面积
        elif building_ratio:
            if not scale_lst: print("缺少比例参数"); return;
            two_params_flag = 1
            sum_building_area = getAreaFromRatio(building_ratio, tot_block_area)   # 通过覆盖率得到所有输入建筑的总占地面积
            arch_type_building_area_lst = getAreaListFromScale(sum_building_area, scale_lst)  # 通过建筑类型比例和总面积, 得到各建筑类型建筑面积
        else:
            print("如果只输入两个建筑变量, 在各建筑类型面积, 各建筑类型占地面积, 容积率, 覆盖率中必须有一项")
            return

        if two_params_flag == 0:     # 进行第一种计算方式
            temp_flag = 0 if not sum_arch_area else 1   # 用于标记是否已经算总建筑面积?
            for i in range(len(arch_type_lst)):
                rest = tot_arch_type_area_lst[i] - arch_type_area_lst[i]  # ? 可抽象
                rest_flag = 0 if rest < 0 else 1
                rest_arch_area_lst.append(rest)
                rest_flag_lst.append(rest_flag)
                arch_type_area_lst[i], arch_floor_lst[i], arch_num_lst[i], arch_plane_area_lst[i] = computeFourParams(arch_type_area_lst[i], arch_floor_lst[i], arch_num_lst[i], arch_plane_area_lst[i])  # 生成新三元
                if not temp_flag: sum_arch_area += arch_type_area_lst[i]  # 没算过的话算
                arch_type_building_area_lst[i] = computeThreeParams(arch_type_building_area_lst[i], arch_num_lst[i], arch_plane_area_lst[i])[0]   # 根据新生成的三元得到该类型的建筑占地
                sum_building_area += arch_type_building_area_lst[i]   # 计算输入建筑的总地块面积
            building_flag = 1 if sum_building_area <= tot_use_block_area else 0  # 现有地块的限制条件
            if not plot_ratio: plot_ratio = getRatio(sum_arch_area, tot_exist_block_area, tot_block_area)
            building_ratio = getRatio(sum_building_area, tot_exist_block_building_area, tot_block_area)   # 计算覆盖率
        else:   # two_params_flag == 1 进行第二种计算方式
            if not (arch_floor_lst[0] and (arch_num_lst[0] or arch_plane_area_lst[0])):
                print("还需要层数, 还有栋数或者底面积两者中的任意一个"); return;
            sum_building_area = sum(arch_type_area_lst)  # 得到总的地块面积
            building_flag = 1 if sum_building_area <= tot_use_block_area else 0  # 现有地块的限制条件
            temp_flag = 0 if not sum_building_area else 1   # 用于标记是否已经算总占地面积?
            for i in range(len(arch_type_lst)):
                arch_type_building_area_lst[i], arch_num_lst[i], arch_plane_area_lst[i] = computeThreeParams(arch_type_building_area_lst[i], arch_num_lst[i], arch_plane_area_lst[i])   # 根据占地面积, 层数, 栋数or底面积生成新的三元
                arch_type_area_lst[i] = computeFourParams(arch_type_area_lst[i], arch_floor_lst[i], arch_num_lst[i], arch_plane_area_lst[i])[0]  # 根据另外三个变量得到该类型建筑面积
                
                rest = tot_arch_type_area_lst[i] - arch_type_area_lst[i]  # ? 可抽象
                rest_flag = 0 if rest < 0 else 1
                rest_arch_area_lst.append(rest)
                rest_flag_lst.append(rest_flag)

                sum_arch_area += arch_type_area_lst[i]
                if not temp_flag: sum_building_area += arch_type_building_area_lst[i]
            if not building_ratio: building_ratio = getRatio(sum_building_area, tot_exist_block_building_area, tot_block_area)   # 计算覆盖率
            plot_ratio = getRatio(sum_arch_area, tot_exist_block_area, tot_block_area)  # 计算容积率
        
    else:
        print("至少在建筑栋数, 底面积, 层数中输入两个")
        return
        
    return arch_type_lst, arch_type_area_lst, rest_arch_area_lst, rest_flag_lst, tot_use_block_area, sum_building_area, building_flag, arch_type_building_area_lst, plot_ratio, building_ratio, arch_floor_lst, arch_num_lst, arch_plane_area_lst

