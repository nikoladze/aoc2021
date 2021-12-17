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
    x_range, y_range = raw_data.split(",")
    x_range, y_range = [
        x.split(f"{k}=")[1].split("..") for x, k in [(x_range, "x"), (y_range, "y")]
    ]
    x_range, y_range = [tuple(int(i) for i in x) for x in [x_range, y_range]]
    return x_range, y_range


def simulate(vx, vy, steps):
    x, y = (0, 0)
    path = []
    for i in range(steps):
        x += vx
        y += vy
        if vx != 0:
            vx += [1, -1][vx > 0]
        vy -= 1
        path.append((x, y))
    return path


# PART 1
@measure_time
def solve1(data):
    x_range, y_range = data
    print(x_range, y_range)
    highest_y_values = []
    for vx in range(150):
        for vy in range(-100, 100):
            path = simulate(vx, vy, 200)
            if any(
                x_range[0] <= x <= x_range[1] and y_range[0] <= y <= y_range[1]
                for x, y in path
            ):
                highest_y_values.append(max((((vx, vy), y) for x, y in path), key=lambda x: x[1]))
    return max(highest_y_values, key=lambda x: x[1])

debug = []

# PART 2
@measure_time
def solve2(data):
    x_range, y_range = data
    params = []
    for vx in range(400):
        for vy in range(-200, 100):
            path = simulate(vx, vy, 200)
            in_target = [
                x_range[0] <= x <= x_range[1] and y_range[0] <= y <= y_range[1]
                for x, y in path
            ]
            if any(in_target):
                steps_first_hit = min(i for i, hit in enumerate(in_target) if hit)
                params.append((vx, vy, steps_first_hit))
    for i, label in enumerate(["vx", "vy", "steps"]):
        print(f"Range for {label}: {min(p[i] for p in params)} - {max(p[i] for p in params)}")
    debug.append(params)
    return len(params)


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
