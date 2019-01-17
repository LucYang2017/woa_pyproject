# -*- coding: utf-8 -*-

# @Time    : 2019/1/14 21:25
# @Author  : Luc
# @Email   : lucyang0901@gmail.com
# @File    : draw_plane.py

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import field
import configs
import numpy as np
import matplotlib.cm as cm

time = 180
accuracy = 0.05
height = 1.3

nodes = field.load_field(time)
plane = []
for node in nodes:
    if node[2] == 0.5:
        plane.append(node)
plane = np.array(plane)

X = np.arange(-2.2, 2.2, 0.05)
Y = np.arange(-2.6, 2.8, 0.05)

X_GRID, Y_GRID = np.meshgrid(X, Y)
C_GRID = np.empty((len(X), len(Y)))
for i in range(len(X)):
    for j in range(len(Y)):
        xx = float(round(X[i], 2))
        yy = float(round(Y[j], 2))
        zz = height
        positions = np.array([[xx, yy, zz]])
        C_GRID[i, j] = field.query_c(positions=positions, field=nodes)

fig = plt.figure(figsize=(16, 6))
ax = fig.add_subplot(121, projection='3d')
ax.set_xlabel('X')
ax.set_xlim(configs.X_MIN, configs.X_MAX)
ax.set_ylabel('Y')
ax.set_ylim(configs.Y_MIN, configs.Y_MAX)
ax.set_zlabel('Z')
ax.set_zlim(0, 100)

ax.plot_surface(X_GRID, Y_GRID, C_GRID.T, rstride=10, cstride=10, cmap=cm.coolwarm)

cc = []
for i in range(len(nodes[:, -1])):
    if np.isnan(nodes[i, -1]):
        nodes[i, -1] = 0
    if nodes[i][2] == height:
        cc.append(nodes[i])
    # print(nodes[i])

ccc = []
for i in range(len(cc)):
    # print(cc[i])
    if cc[i][2] == height:
        ccc.append(cc[i][-1])

print(cc[ccc.index(max(ccc))])

ax2 = fig.add_subplot(122)
ax2.hist(ccc, bins=100, range=(0, 10000))

s = 0
for i in ccc:
    if i > 5000:
        s += 1

print(s / len(cc))
plt.show()
