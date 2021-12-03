#!/usr/bin/env python

from functools import wraps
from datetime import datetime
import math


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
    return raw_data.split("\n")


# PART 1
@measure_time
def solve1(data):
    gamma = []
    epsilon = []
    n = len(data[0])
    for i in range(n):
        total = sum(line[i] == "1" for line in data)
        if total > len(data) // 2:
            gamma.append("1")
            epsilon.append("0")
        else:
            gamma.append("0")
            epsilon.append("1")
    return int("".join(gamma), 2) * int("".join(epsilon), 2)


def count_ones(data, pos):
    return sum(line[pos] == "1" for line in data)


def find_oxygen(data):
    data = data[:]
    for i in range(len(data[0])):
        if count_ones(data, i) >= math.ceil(len(data) / 2):
            data = [line for line in data if line[i] == "1"]
        else:
            data = [line for line in data if line[i] == "0"]
        if len(data) == 1:
            return int(data[0], 2)

def find_co2(data):
    data = data[:]
    for i in range(len(data[0])):
        if count_ones(data, i) < math.ceil(len(data) / 2):
            data = [line for line in data if line[i] == "1"]
        else:
            data = [line for line in data if line[i] == "0"]
        if len(data) == 1:
            return int(data[0], 2)

# PART 2
@measure_time
def solve2(data):
    return find_oxygen(data) * find_co2(data)


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
