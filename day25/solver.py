#!/usr/bin/env python

from functools import wraps
from datetime import datetime
import numpy as np

times = []


def measure_time(func):
    @wraps(func)
    def _func(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now()
        times.append((func.__name__, (end - start).total_seconds()))
        return result

    return _func


@measure_time
def parse(raw_data):
    return np.array([list(line) for line in raw_data.strip().split("\n")])


def updated(grid):
    new_grid = np.array(grid)
    dy, dx = grid.shape
    for y, line in enumerate(grid):
        for x, v in enumerate(line):
            if v == ">" and grid[y, (x + 1) % dx] == ".":
                new_grid[y, x] = "."
                new_grid[y, (x + 1) % dx] = ">"
    grid = new_grid
    new_grid = np.array(grid)
    for y, line in enumerate(grid):
        for x, v in enumerate(line):
            if v == "v" and grid[(y + 1) % dy, x] == ".":
                new_grid[y, x] = "."
                new_grid[(y + 1) % dy, x] = "v"
    return new_grid


# PART 1
@measure_time
def solve1(data, max_iter=10000):
    grid = data
    for i in range(1, max_iter):
        new_grid = updated(grid)
        if (new_grid == grid).all():
            return i
        grid = new_grid

# PART 2
@measure_time
def solve2(data):
    pass


if __name__ == "__main__":
    import sys

    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in times)))
