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


@measure_time
def parse(raw_data):
    return [[int(i) for i in line] for line in raw_data.split("\n")]


class OctopusAutomaton:
    def __init__(self, grid):
        self.grid = np.array(grid)
        self.flashing = np.zeros_like(self.grid, dtype=bool)

    def try_update(self, x, y):
        if y < 0 or x < 0:
            return
        try:
            self.grid[y][x]
        except IndexError:
            return
        if self.grid[y][x] > 9:
            return
        self.grid[y][x] += 1

    def update_adjacent(self, x, y):
        self.try_update(x + 1, y)
        self.try_update(x - 1, y)
        self.try_update(x, y + 1)
        self.try_update(x, y - 1)
        self.try_update(x + 1, y + 1)
        self.try_update(x - 1, y - 1)
        self.try_update(x - 1, y + 1)
        self.try_update(x + 1, y - 1)

    def step(self):
        self.flashing[:] = False

        # first increase all counters
        for y, row in enumerate(self.grid):
            for x, v in enumerate(row):
                self.try_update(x, y)

        # then do the flashing chain
        any_update = True
        while any_update:
            any_update = False
            for y, row in enumerate(self.grid):
                for x, v in enumerate(row):
                    if self.flashing[y][x]:
                        # don't update already flashing octopusses
                        continue
                    if self.grid[y][x] > 9:
                        self.flashing[y][x] = True
                        self.update_adjacent(x, y)
                        any_update = True

        self.grid[self.flashing] = 0

    def __repr__(self):
        return "\n".join(
            "".join(str(i) if i != 0 else f"\033[1m{i}\033[0m" for x, i in enumerate(row))
            for y, row in enumerate(self.grid)
        )


# PART 1
@measure_time
def solve1(data, steps=10):
    automaton = OctopusAutomaton(data)
    total = 0
    for i in range(steps):
        automaton.step()
        total += automaton.flashing.sum()
    return total


# PART 2
@measure_time
def solve2(data):
    automaton = OctopusAutomaton(data)
    i = 1
    while True:
        automaton.step()
        if automaton.flashing.sum() == 100:
            return i
        i += 1


if __name__ == "__main__":
    import sys

    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data, 100)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in times)))
