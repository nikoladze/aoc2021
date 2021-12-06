#!/usr/bin/env python

from functools import wraps
from datetime import datetime
from collections import defaultdict


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
    fishes = data[:]
    for i in range(80):
        new_fishes = len([f for f in fishes if f == 0])
        fishes = [f-1 if f != 0 else 6 for f in fishes] + [8] * new_fishes
    return len(fishes)


# PART 2
@measure_time
def solve2(data, ndays=256):
    fishes = defaultdict(int)
    for i in data:
        fishes[i] += 1
    for day in range(ndays):
        prev_fishes = fishes.copy()
        fishes[8] = 0
        for i in range(7, -1, -1):
            fishes[i] = prev_fishes[i + 1]
        fishes[6] += prev_fishes[0]
        fishes[8] += prev_fishes[0]
    return sum(fishes.values())


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
