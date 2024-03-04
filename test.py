# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

import colorquiver

colorMode = 1
labelGrid = 64
fDict = {
    # 'family':'Times New Roman',
    # 'style':'italic',
    'weight':'normal',
    # 'color':'black',
    # 'size':16
}
mapping = [0, 0]

lim = (-1, 1, -1, 1)  # xmin, xmax, ymin, ymax

fig = plt.figure(figsize=(5, 4), facecolor="none")
ax = fig.add_axes((0.1, 0.1, 0.8, 0.8), facecolor="#EEE")

# ax.set_xticks([])
# ax.set_yticks([])
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)
# ax.spines['bottom'].set_visible(False)
# ax.spines['left'].set_visible(False)


shape = (100, 100)
X, Y = np.meshgrid(np.linspace(lim[0], lim[1], shape[1]), np.linspace(lim[2], lim[3], shape[0]))

l = np.sqrt(X**2 + Y**2)
U = -Y / l
V = X / l

mapping[1], maxValue = colorquiver.colorquiver(ax, lim, U, V, colorMode)

colorquiver.colorlabel(fig, labelGrid, mapping, colorMode, fDict)
ax.streamplot(X, Y, U, V, linewidth=1)
# ax.quiver(X[::4, ::4], Y[::4, ::4], U[::4, ::4], V[::4, ::4], linewidth=1)

plt.show()
