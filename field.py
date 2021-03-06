# -*- coding: utf-8 -*-

# @Time    : 2019/1/4 8:13
# @Author  : Luc
# @Email   : lucyang0901@gmail.com
# @File    : field.py


import numpy as np
from configs import *
from scipy.interpolate import griddata
import print_colors
import math


def scinum_2_float(sci_num):
    """
    转换科学计数法的数字或字符串为浮点类型,E的大小写区别可能造成报错
    :param sci_num: 科学计数法表达的数字，类型一般是字符串，比如 6.0000000e+000 "3.4717316e-009"
    :return: 返回浮点类型的数字
    """
    sci_num = str(sci_num)
    base = float(sci_num.split('E')[0])
    power = float(sci_num.split('E')[1])
    return base * pow(10, power)


def generate_raw_field(file_name):
    raw_data = open('data/' + str(FIELD_TYPE) + '/' + str(file_name) + '.txt', 'r', encoding='utf-8').readlines()[1:]
    raw_field = []
    # for i in range(len(raw_data)):  # 这个for用于处理有风速信息的数据
    #     msg = raw_data[i].split(',')[1:]
    #     if round(scinum_2_float(msg[1]), 2) == height:
    #         x_coordinate = round(scinum_2_float(msg[0]), 2)
    #         y_coordinate = round(scinum_2_float(msg[1]), 2)
    #         z_coordinate = round(scinum_2_float(msg[2]), 2)
    #         position = [x_coordinate, y_coordinate, z_coordinate]
    #         x_airflow_velocity = scinum_2_float(msg[3])
    #         y_airflow_velocity = scinum_2_float(msg[4])
    #         z_airflow_velocity = scinum_2_float(msg[5])
    #         airflow_velocity = [x_airflow_velocity, y_airflow_velocity, z_airflow_velocity]
    #         concentration = [round(scinum_2_float(msg[6]), 3)]
    #         node_msg = position + airflow_velocity + concentration
    #         node_msgs.append(node_msg)
    for i in range(len(raw_data)):  # 用于处理没有风速信息的数据
        msg = raw_data[i].split(',')[1:]
        x_coordinate = round(scinum_2_float(msg[0]), 2)
        y_coordinate = round(scinum_2_float(msg[1]), 2)
        z_coordinate = round(scinum_2_float(msg[2]), 2)
        position = [x_coordinate, y_coordinate, z_coordinate]
        concentration = [scinum_2_float(msg[-1]) * pow(10, 5)]
        node = position + concentration
        raw_field.append(node)
    return np.array(raw_field)


def generate_raw_airflow_field():
    raw_data = open('data/' + str(FIELD_TYPE) + '/speed.txt', 'r', encoding='utf-8').readlines()[1:]
    raw_airflow_field = []
    for i in range(len(raw_data)):  # 用于处理没有风速信息的数据
        msg = raw_data[i].split(',')[1:]
        x_coordinate = round(scinum_2_float(msg[0]), 2)
        y_coordinate = round(scinum_2_float(msg[1]), 2)
        z_coordinate = round(scinum_2_float(msg[2]), 2)
        position = [x_coordinate, y_coordinate, z_coordinate]
        x_velocity = round(scinum_2_float(msg[3]), 2)
        y_velocity = round(scinum_2_float(msg[4]), 2)
        z_velocity = round(scinum_2_float(msg[5]), 2)
        airflow = [x_velocity, y_velocity, z_velocity]
        node = position + airflow
        raw_airflow_field.append(node)
    return np.array(raw_airflow_field)


def generate_empty_grid(accuracy):
    empty_grid = []
    x_max = round(X_MAX, 2)
    x_min = round(X_MIN, 2)
    y_max = round(Y_MAX, 2)
    y_min = round(Y_MIN, 2)
    z_max = round(Z_MAX, 2)
    z_min = round(Z_MIN, 2)

    def start_end(min, max, accuracy):
        import math
        left_boundary = math.floor(int(min / accuracy)) - 1
        right_boundary = math.floor(int(max / accuracy)) + 1
        x = []
        for i in range(left_boundary, right_boundary + 1):
            if min <= round(i * accuracy, 2) <= max:
                x.append(round(i * accuracy, 2))
        x = sorted(x)
        start = x[0]
        end = x[-1]
        return round(start, 2), round(end, 2)

    x_start, x_end = start_end(x_min, x_max, accuracy)
    y_start, y_end = start_end(y_min, y_max, accuracy)
    z_start, z_end = start_end(z_min, z_max, accuracy)
    xi = np.arange(x_start, x_end + accuracy, accuracy)
    yi = np.arange(y_start, y_end + accuracy, accuracy)
    zi = np.arange(z_start, z_end + accuracy, accuracy)
    for i in xi:
        for j in yi:
            for k in zi:
                empty_grid.append([round(i, 2), round(j, 2), round(k, 2)])

    return np.array(empty_grid)


def generate_airflow_field(raw_airflow_field, empty_grid):
    grid_v_x = griddata(raw_airflow_field[:, :3], raw_airflow_field[:, 3], empty_grid, method='linear')
    grid_v_y = griddata(raw_airflow_field[:, :3], raw_airflow_field[:, 4], empty_grid, method='linear')
    grid_v_z = griddata(raw_airflow_field[:, :3], raw_airflow_field[:, 5], empty_grid, method='linear')
    for i in range(len(grid_v_x)):
        if np.isnan(grid_v_x[3]):
            grid_v_x[3]
        if np.isnan(grid_v_x[4]):
            grid_v_x[3]
        if np.isnan(grid_v_x[5]):
            grid_v_x[3]
    field = np.column_stack((empty_grid, grid_v_x, grid_v_y, grid_v_z))
    return field


def prepare_airflow_field_data_base():
    epg = generate_empty_grid(0.05)

    raw_airflow_field = generate_raw_airflow_field()
    airflow_filed = generate_airflow_field(raw_airflow_field, epg)
    save_field(airflow_filed, 'speed')
    print('%s saved' % ('speed'))


def generate_field(raw_field, empty_grid):
    grid_c = griddata(raw_field[:, :3], raw_field[:, 3], empty_grid, method='linear')
    for c in grid_c:
        if np.isnan(c):
            c = 0
    field = np.column_stack((empty_grid, grid_c))
    return field


def save_field(field, file_name):
    import pickle as p
    f = open('field/' + str(FIELD_TYPE) + '/' + str(file_name) + '.data', 'wb')
    p.dump(field, f)
    f.close()


def query_c(positions, field):
    accuracy = abs(field[0][2] - field[1][2])

    x_max = field[-1][0]
    x_min = field[0][0]
    y_max = field[-1][1]
    y_min = field[0][1]
    z_max = field[-1][2]
    z_min = field[0][2]

    x_total = int((x_max - x_min) / accuracy + 1)
    y_total = int((y_max - y_min) / accuracy + 1)
    z_total = int((z_max - z_min) / accuracy + 1)

    c_array = []

    def get_nearest_coordinate_value(coordinate_value, coordinate_min, coordinate_max):
        d_min = float('inf')
        nearest_coordinate_value = 0

        for i in np.arange(coordinate_min, coordinate_max + accuracy, accuracy):
            d = abs(coordinate_value - i)
            if d <= d_min:
                d_min = d
                nearest_coordinate_value = i
        return round(nearest_coordinate_value, 2)

    for position in positions:
        x = get_nearest_coordinate_value(position[0], x_min, x_max)
        y = get_nearest_coordinate_value(position[1], y_min, y_max)
        z = get_nearest_coordinate_value(position[2], z_min, z_max)
        x_counter = round((x - x_min) / accuracy + 1, 0)
        y_counter = round((y - y_min) / accuracy + 1, 0)
        z_counter = round((z - z_min) / accuracy + 1, 0)
        c_index = int((x_counter - 1) * y_total * z_total + (y_counter - 1) * z_total + z_counter) - 1
        c = field[c_index]
        # if np.linalg.norm(c[:3] - np.array(position)) > accuracy * 1.7321:
        if round(np.linalg.norm(c[:3] - np.array([x, y, z])), 3) != 0:
            print_colors.red('ATTENTION !! This position is far away from the supposed position!!')
            print(np.array([x, y, z]))
            print(c[:3])
            for i in range(len(field)):  # 防止出现不对的情况
                if np.linalg.norm(field[i][:3] - np.array([x, y, z])) == 0:
                    c_index = i
                    break
        c = field[c_index]
        if round(np.linalg.norm(c[:3] - np.array([x, y, z])), 3) != 0:
            print_colors.red('ATTENTION !! This position is far away from the supposed position!!')
            print_colors.red('Distance:\t\t\t\t%s' % (np.linalg.norm(c[:3] - np.array(position))))
            print_colors.red('In position:\t%s' % (position))
            print_colors.red('Formed position:\t%s' % ([x, y, z]))
            print_colors.red('Out position:\t\t%s' % (c[:3]))

        if np.isnan(c[-1]):
            c[-1] = 0
        c_array.append(c[-1])
    return np.array(c_array)


def query_v(positions, airflow_field):
    accuracy = abs(airflow_field[0][2] - airflow_field[1][2])

    x_max = airflow_field[-1][0]
    x_min = airflow_field[0][0]
    y_max = airflow_field[-1][1]
    y_min = airflow_field[0][1]
    z_max = airflow_field[-1][2]
    z_min = airflow_field[0][2]

    x_total = int((x_max - x_min) / accuracy + 1)
    y_total = int((y_max - y_min) / accuracy + 1)
    z_total = int((z_max - z_min) / accuracy + 1)

    v_array = []

    def get_nearest_coordinate_value(coordinate_value, coordinate_min, coordinate_max):
        d_min = float('inf')
        nearest_coordinate_value = 0

        for i in np.arange(coordinate_min, coordinate_max + accuracy, accuracy):
            d = abs(coordinate_value - i)
            if d <= d_min:
                d_min = d
                nearest_coordinate_value = i
        return round(nearest_coordinate_value, 2)

    for position in positions:
        x = get_nearest_coordinate_value(position[0], x_min, x_max)
        y = get_nearest_coordinate_value(position[1], y_min, y_max)
        z = get_nearest_coordinate_value(position[2], z_min, z_max)
        x_counter = round((x - x_min) / accuracy + 1, 0)
        y_counter = round((y - y_min) / accuracy + 1, 0)
        z_counter = round((z - z_min) / accuracy + 1, 0)
        v_index = int((x_counter - 1) * y_total * z_total + (y_counter - 1) * z_total + z_counter) - 1
        v = airflow_field[v_index]
        # if np.linalg.norm(c[:3] - np.array(position)) > accuracy * 1.7321:
        if round(np.linalg.norm(v[:3] - np.array([x, y, z])), 3) != 0:
            print_colors.red('ATTENTION !! This position is far away from the supposed position!!')
            print(np.array([x, y, z]))
            print(v[:3])
            for i in range(len(airflow_field)):  # 防止出现不对的情况
                if np.linalg.norm(airflow_field[i][:3] - np.array([x, y, z])) == 0:
                    v_index = i
                    break
        v = airflow_field[v_index]
        if round(np.linalg.norm(v[:3] - np.array([x, y, z])), 3) != 0:
            print_colors.red('ATTENTION !! This position is far away from the supposed position!!')
            print_colors.red('Distance:\t\t\t\t%s' % (np.linalg.norm(c[:3] - np.array(position))))
            print_colors.red('In position:\t%s' % (position))
            print_colors.red('Formed position:\t%s' % ([x, y, z]))
            print_colors.red('Out position:\t\t%s' % (v[:3]))
        v_array.append(v[-3:])
    return np.array(v_array)


def prepare_field_data_base(t_start, t_end):
    print_colors.red("Are you sure to create " + str(FIELD_TYPE) + "_data_base?")
    epg = generate_empty_grid(0.05)
    for i in range(t_start, t_end + 1):
        raw_f = generate_raw_field(i)
        field = generate_field(raw_f, epg)
        save_field(field, i)
        print('%d saved' % (i))


def load_field(file_name):
    import pickle as p
    f = open('field/' + str(FIELD_TYPE) + '/' + str(file_name) + '.data', 'rb')
    return p.load(f)


def load_airflow_field():
    import pickle as p
    f = open('field/' + str(FIELD_TYPE) + '/speed.data', 'rb')
    return p.load(f)




