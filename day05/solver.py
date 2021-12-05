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


def parse_gen(raw_data):
    for line in raw_data.split("\n"):
        start, end = line.split(" -> ")
        x1, y1 = start.split(",")
        x2, y2 = end.split(",")
        yield ((int(x1), int(y1)), (int(x2), int(y2)))


@measure_time
def parse(raw_data):
    return list(parse_gen(raw_data))


def make_vent_map(data):
    return np.zeros(
        (
            max(max(y1, y2) for (x1, y1), (x2, y2) in data) + 2,
            max(max(x1, x2)for (x1, y1), (x2, y2) in data) + 2,
        ),
        dtype=int
    )


def horizontal_line(vent_map, x1, y1, x2, y2):
    assert x1 == x2
    y1, y2 = sorted((y1, y2))
    vent_map[y1: y2 + 1, x1] += 1


def vertical_line(vent_map, x1, y1, x2, y2):
    assert y1 == y2
    x1, x2 = sorted((x1, x2))
    vent_map[y1, x1: x2 + 1] += 1


# PART 1
@measure_time
def solve1(data):
    vent_map = make_vent_map(data)
    for (x1, y1), (x2, y2) in data:
        if x1 == x2:
            horizontal_line(vent_map, x1, y1, x2, y2)
        if y1 == y2:
            vertical_line(vent_map, x1, y1, x2, y2)
    return (vent_map >= 2).sum()


def diagonal_line(vent_map, x1, y1, x2, y2):
    assert abs(y2 - y1) == abs(x2 - x1)
    step_x = 1 if x2 >= x1 else -1
    step_y = 1 if y2 >= y1 else -1
    for x, y in zip(range(x1, x2 + step_x, step_x), range(y1, y2 + step_y, step_y)):
        vent_map[y, x] += 1


# PART 2
@measure_time
def solve2(data):
    vent_map = make_vent_map(data)
    for (x1, y1), (x2, y2) in data:
        if abs(x2 - x1) == abs(y2 - y1):
            diagonal_line(vent_map, x1, y1, x2, y2)
        elif x1 == x2:
            horizontal_line(vent_map, x1, y1, x2, y2)
        elif y1 == y2:
            vertical_line(vent_map, x1, y1, x2, y2)
    return (vent_map >= 2).sum()


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
