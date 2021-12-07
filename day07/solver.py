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
    return [int(i) for i in raw_data.split(",")]


# PART 1
@measure_time
def solve1(data):
    fuel_spendings = []
    for pos in range(min(data), max(data) + 1):
        fuel_spendings.append(sum(abs(crab_pos - pos) for crab_pos in data))
    return min(fuel_spendings)


# PART 2
@measure_time
def solve2(data):
    fuel_spendings = []
    for pos in range(min(data), max(data) + 1):
        fuel_spendings.append(sum(sum(range(abs(crab_pos - pos) + 1)) for crab_pos in data))
    return min(fuel_spendings)


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
