import blockArrange

def foo1():
    tot_arch_type_area_lst = [3000, 5000, 6000]
    tot_block_area = 4000.20
    tot_exist_block_area = None
    tot_exist_block_building_area = None
    arch_type_lst = [0, 3, 8]
    plot_ratio = None
    building_ratio = None
    arch_floor_lst = [2, 1, 3]
    arch_num_lst = [1, 1, 1]
    arch_plane_area_lst = [230.2, 300.5, 180.0]
    arch_type_area_lst = None
    arch_type_building_area_lst = None
    scale_lst = None
    rst = blockArrange.arrange(tot_arch_type_area_lst, tot_block_area,
            tot_exist_block_area, tot_exist_block_building_area,
            arch_type_lst, plot_ratio, building_ratio,
            arch_floor_lst, arch_num_lst, arch_plane_area_lst,
            arch_type_area_lst, arch_type_building_area_lst,
            scale_lst)
    return rst 

if __name__ == '__main__':
    arch_type_lst, arch_type_area_lst, rest_arch_area_lst, rest_flag_lst, tot_use_block_area, sum_building_area, building_flag, arch_type_building_area_lst, plot_ratio, building_ratio, arch_floor_lst, arch_num_lst, arch_plane_area_lst = foo1()
    print(arch_type_lst, arch_type_area_lst, rest_arch_area_lst, rest_flag_lst, tot_use_block_area, sum_building_area, building_flag, arch_type_building_area_lst, plot_ratio, building_ratio, arch_floor_lst, arch_num_lst, arch_plane_area_lst)
