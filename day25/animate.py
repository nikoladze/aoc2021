#!/usr/bin/env python

import sys
from solver import parse, updated
import time

data = parse(open("input.txt").read().strip())

def print_grid(grid):
    sys.stdout.write("\033c")
    sys.stdout.write("\n".join("".join(line) for line in grid))
    sys.stdout.flush()

grid = data
print_grid(grid)
for i in range(1, 10000):
    time.sleep(0.05)
    new_grid = updated(grid)
    if (new_grid == grid).all():
        break
    grid = new_grid
    print_grid(grid)
