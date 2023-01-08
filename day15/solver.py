#!/usr/bin/env python

from functools import wraps, cache
from datetime import datetime
import heapq

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


def shortest_path_heapq(grid):
    distances = {}
    via_dict = {}
    q = []
    start = (0, 0)
    nrows = len(grid)
    ncols = len(grid[0])
    goal = (nrows - 1, ncols - 1)
    heapq.heappush(q, (0, start, 0))
    while q:
        distance, pos, via = heapq.heappop(q)
        if pos in distances:
            continue
        distances[pos] = distance
        via_dict[pos] = via
        if pos == goal:
            return distance, via_dict, distances
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x, y = pos[0] + dx, pos[1] + dy
            if x < 0 or x >= ncols or y < 0 or y >= nrows:
                continue
            new_distance = distance + grid[y][x]
            heapq.heappush(q, (new_distance, (x, y), pos))


def shortest_path_dict(grid):
    distances = {}
    via_dict = {}
    q = {}
    start = (0, 0)
    nrows = len(grid)
    ncols = len(grid[0])
    goal = (nrows - 1, ncols - 1)
    q[start] = (0, 0)
    while q:
        pos, (distance, via) = min(q.items(), key=lambda x: x[1])
        del q[pos]
        if pos in distances:
            continue
        distances[pos] = distance
        via_dict[pos] = via
        if pos == goal:
            return distance, via_dict, distances
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x, y = pos[0] + dx, pos[1] + dy
            if x < 0 or x >= ncols or y < 0 or y >= nrows:
                continue
            new_distance = distance + grid[y][x]
            if (x, y) not in q or q[x, y][0] > new_distance:
                q[x, y] = (new_distance, pos)


# PART 1
@measure_time
def solve1(data, shortest_path=shortest_path_heapq):
    return shortest_path(data)[0]


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
def solve2(data, shortest_path=shortest_path_heapq):
    full_grid = fill_full_grid(data)
    return shortest_path(full_grid)[0]


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--algorithm", choices=["heapq", "dict"], default="heapq")
    args = parser.parse_args()
    if args.algorithm == "heapq":
        shortest_path = shortest_path_heapq
    elif args.algorithm == "dict":
        shortest_path = shortest_path_dict

    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data, shortest_path=shortest_path)))
    print("Part 2: {}".format(solve2(data, shortest_path=shortest_path)))

    print("\nTime taken:")
    for func, time in times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in times)))
