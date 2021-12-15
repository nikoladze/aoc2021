#!/usr/bin/env python

from functools import wraps, cache
from datetime import datetime


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
    return [[int(i) for i in line] for line in raw_data.split("\n")]


def get_graph(grid):
    import networkx as nx
    G = nx.DiGraph()

    def try_add(x0, y0, x1, y1):
        if any(x < 0 for x in (x0, y0, x1, y1)):
            return
        try:
            G.add_edge((x0, y0), (x1, y1), weight=grid[y1][x1])
        except IndexError:
            pass

    for y, row in enumerate(grid):
        for x, risk in enumerate(row):
            try_add(x, y, x + 1, y)
            try_add(x, y, x - 1, y)
            try_add(x, y, x, y + 1)
            try_add(x, y, x, y - 1)

    return G


def shortest_path(grid):
    import networkx as nx
    graph = get_graph(grid)
    ymax = len(grid) - 1
    return nx.dijkstra_path_length(graph, (0, 0), (ymax, ymax))


# PART 1
@measure_time
def solve1(data):
    return shortest_path(data)


def fill_full_grid(grid):
    size = len(grid)
    new_grid = []
    for y in range(5 * size):
        new_grid.append([])
        for x in range(5 * size):
            if x < size and y < size:
                new_grid[-1].append(grid[y][x])
                continue
            if y < size:
                ref = new_grid[y][x - size]
                new_grid[-1].append(ref + 1 if ref < 9 else 1)
                continue
            ref = new_grid[y - size][x]
            new_grid[-1].append(ref + 1 if ref < 9 else 1)
    return new_grid


# PART 2
@measure_time
def solve2(data):
    return shortest_path(fill_full_grid(data))


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
