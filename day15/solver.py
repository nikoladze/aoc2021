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
    done = set()
    distances = {}
    q = []
    start = (0, 0)
    nrows = len(grid)
    ncols = len(grid[0])
    goal = (nrows - 1, ncols - 1)
    heapq.heappush(q, (0, start))
    while q:
        distance, pos = heapq.heappop(q)
        if pos in done:
            continue
        if pos == goal:
            return distance
        done.add(pos)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x, y = pos[0] + dx, pos[1] + dy
            if x < 0 or x >= ncols or y < 0 or y >= nrows:
                continue
            new_distance = distance + grid[y][x]
            heapq.heappush(q, (new_distance, (x, y)))


def shortest_path_dict(grid):
    distances = {}
    done = set()
    q = {}
    start = (0, 0)
    nrows = len(grid)
    ncols = len(grid[0])
    goal = (nrows - 1, ncols - 1)
    q[start] = 0
    while q:
        pos, distance = min(q.items(), key=lambda x: x[1])
        del q[pos]
        if pos == goal:
            return distance
        if pos in done:
            continue
        done.add(pos)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x, y = pos[0] + dx, pos[1] + dy
            if x < 0 or x >= ncols or y < 0 or y >= nrows:
                continue
            new_distance = distance + grid[y][x]
            q[(x, y)] = min(q.get((x, y), new_distance), new_distance)


# PART 1
@measure_time
def solve1(data, shortest_path=shortest_path_heapq):
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
def solve2(data, shortest_path=shortest_path_heapq):
    full_grid = fill_full_grid(data)
    return shortest_path(full_grid)


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
