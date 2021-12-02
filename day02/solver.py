#!/usr/bin/env python

from functools import wraps
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
    out = []
    for line in raw_data.split("\n"):
        instruction, value = line.split()
        value = int(value)
        out.append((instruction, value))
    return out


# PART 1
@measure_time
def solve1(data):
    depth = 0
    pos = 0
    for instruction, value in data:
        if instruction == "forward":
            pos += value
        elif instruction == "down":
            depth += value
        elif instruction == "up":
            depth -= value
    return depth * pos


# PART 2
@measure_time
def solve2(data):
    depth = 0
    pos = 0
    aim = 0
    for instruction, value in data:
        if instruction == "forward":
            pos += value
            depth += aim * value
        elif instruction == "down":
            aim += value
        elif instruction == "up":
            aim -= value
    return depth * pos


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
