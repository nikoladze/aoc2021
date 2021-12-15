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



def min_risk_from(risk, trace, x, y, grid):

    def _min_risk_from(risk, trace, x, y):
        if x == len(grid[0]) - 1 and y == len(grid) - 1:
            return trace + [(x, y)], risk + grid[y][x]

        def try_min(x, y):
            if (x, y) in trace or x < 0 or y < 0:
                return None
            try:
                return _min_risk_from(risk, trace, x, y)
            except IndexError:
                return None

        left = try_min(x - 1, y)
        right = try_min(x + 1, y)
        top = try_min(x, y - 1)
        bottom = try_min(x, y + 1)

        new_trace, min_risk = min(
            [x for x in [left, right, top, bottom] if x is not None], key=lambda x: x[1]
        )
        return trace + new_trace, min_risk

    return _min_risk_from(trace, x, y)


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


# PART 1
@measure_time
def solve1(data):
    #trace, res = min_risk_from([(0, 0)], 0, 0, data)
    #print(trace)
    #return res
    import networkx as nx
    graph = get_graph(data)
    ymax = len(data) - 1
    #path = nx.dijkstra_path(graph, (0, 0), (ymax, ymax))
    path = nx.shortest_path(graph, (0, 0), (ymax, ymax), weight="weight")
    print("")
    for y in range(len(data)):
        for x in range(len(data[0])):
            if (x, y) in path:
                print("#", end="")
            else:
                print(data[y][x], end="")
        print("\n", end="")
    risk = 0
    for x, y in path[1:]:
        risk += data[y][x]
    #return risk
    return nx.dijkstra_path_length(graph, (0, 0), (ymax, ymax))


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
    import networkx as nx
    new_grid = fill_full_grid(data)
    graph = get_graph(new_grid)
    ymax = len(new_grid) - 1
    #path = nx.dijkstra_path(graph, (0, 0), (ymax, ymax))
    path = nx.shortest_path(graph, (0, 0), (ymax, ymax), weight="weight")
    # print("")
    # for y in range(len(data)):
    #     for x in range(len(data[0])):
    #         if (x, y) in path:
    #             print("#", end="")
    #         else:
    #             print(data[y][x], end="")
    #     print("\n", end="")
    risk = 0
    for x, y in path[1:]:
        risk += new_grid[y][x]
    return risk


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
