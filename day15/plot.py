#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from solver import shortest_path_heapq as shortest_path, fill_full_grid, parse

with open("input.txt") as f:
    data = parse(f.read().strip())

grid = fill_full_grid(data)
min_distance, via, distances = shortest_path(grid)

nrows = len(grid)
ncols = len(grid[0])
img = np.zeros((nrows, ncols), dtype=int)
xs = []
ys = []
zs = []
for (x, y), z in distances.items():
    xs.append(x)
    ys.append(y)
    zs.append(z)
img[ys, xs] = zs

start = (0, 0)
pos = (ncols - 1, nrows - 1)
path_x = [pos[0]]
path_y = [pos[1]]
while pos != start:
    pos = via[pos]
    path_x.append(pos[0])
    path_y.append(pos[1])

plt.pcolormesh(range(ncols), range(nrows), img)
plt.plot(path_x, path_y, color="red")
plt.show()
