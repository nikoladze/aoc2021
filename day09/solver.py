#!/usr/bin/env python

from functools import wraps, reduce
from datetime import datetime
from operator import mul


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
    return [[int(x) for x in line] for line in raw_data.split("\n")]


def higher_or_none(data, height, x, y):
    if x < 0 or y < 0:
        return True
    try:
        return data[y][x] > height
    except IndexError:
        return True


def find_low_points(data):
    low_points = []
    for y, line in enumerate(data):
        for x, height in enumerate(line):
            check = lambda x, y: higher_or_none(data, height, x, y)
            if (
                check(x - 1, y)
                and check(x + 1, y)
                and check(x, y - 1)
                and check(x, y + 1)
            ):
                low_points.append((x, y, height))
                continue
    return low_points


# PART 1
@measure_time
def solve1(data):
    low_points = find_low_points(data)
    return sum(height + 1 for x, y, height in low_points)


def find_basins(data):
    low_points = find_low_points(data)
    basins = []

    def extend_basin(basin, x, y):
        height = data[y][x]

        def check_extend(x, y):
            if x < 0 or y < 0:
                return
            try:
                if not (data[y][x] > height and data[y][x] != 9):
                    return
            except IndexError:
                return
            basin.add((x, y))
            extend_basin(basin, x, y)

        check_extend(x - 1, y)
        check_extend(x + 1, y)
        check_extend(x, y + 1)
        check_extend(x, y - 1)

    for x, y, height in low_points:
        if any((x, y) in basin for basin in basins):
            # already got that point
            continue
        basin = set()
        basin.add((x, y))
        extend_basin(basin, x, y)
        basins.append(basin)
    return basins


# PART 2
@measure_time
def solve2(data):
    basins = find_basins(data)
    return reduce(mul, sorted(len(basin) for basin in basins)[-3:], 1)


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
