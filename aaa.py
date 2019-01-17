# # -*- coding: utf-8 -*-
#
# # @Time    : 2019/1/14 20:17
# # @Author  : Luc
# # @Email   : lucyang0901@gmail.com
# # @File    : aaa.py
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import field
import numpy as np


def start_end(min, max, accuracy):
    import math
    left_boundary = math.floor(int(min / accuracy)) - 1
    right_boundary = math.floor(int(max / accuracy)) + 1
    x = []
    for i in range(left_boundary, right_boundary + 1):
        if min  <= round(i * accuracy, 2) <= max:
            x.append(round(i * accuracy, 2))
    x = sorted(x)
    start = x[0]
    end = x[-1]
    return round(start, 2), round(end, 2)


a, b = start_end(1.100000001, 2.95000001, 0.05)
print(a)
print(b)
