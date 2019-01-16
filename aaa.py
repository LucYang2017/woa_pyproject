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

nodes = field.load_field(17)
plane = []
for node in nodes:
    if node[2] == 0.5:
        plane.append(node)
plane = np.array(plane)

X = np.arange(-2.2, 2.2, 0.05)
Y = np.arange(-2.6, 2.8, 0.05)


X_GRID, Y_GRID = np.meshgrid(X, Y)
Z_GRID = np.empty((len(X), len(Y)))
for i in range(len(X)):
    for j in range(len(Y)):
        xx = float(round(X[i], 2))
        yy = float(round(Y[j], 2))
        zz = 0.05
        positions = np.array([[xx, yy, zz]])
        Z_GRID[i, j] = field.query_c(positions=positions, field=nodes)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Grab some test data.


# Plot a basic wireframe.
# ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)
ax.plot_wireframe(X_GRID, Y_GRID, Z_GRID.T, rstride=10, cstride=10)

plt.show()
