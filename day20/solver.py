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
    algorithm, grid = raw_data.split("\n\n")
    algorithm = "".join(["0" if c == "." else "1" for c in algorithm])
    image = defaultdict(lambda: "0")
    for y, row in enumerate(grid.split("\n")):
        for x, val in enumerate(row):
            if val == "#":
                image[(x, y)] = "1"
    return algorithm, image


def enhancement_index(image, x, y):
    digits = []
    for x2, y2 in [
        (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
        (x - 1, y), (x, y), (x + 1, y),
        (x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
    ]:
        digits.append(image[(x2, y2)])
    return int("".join(digits), 2)


def enhance(image, algorithm):
    new_image = image.copy()
    xmin = min(x for x, y in image)
    xmax = max(x for x, y in image)
    ymin = min(y for x, y in image)
    ymax = max(y for x, y in image)
    for y in range(ymin - 1, ymax + 2):
        for x in range(xmin - 1, xmax + 2):
            new_image[(x, y)] = algorithm[enhancement_index(image, x, y)]
    if image.default_factory() == "0":
        new_image.default_factory = lambda: algorithm[0]
    else:
        new_image.default_factory = lambda: algorithm[-1]
    return new_image


def print_image(image):
    xmin = min(x for x, y in image)
    xmax = max(x for x, y in image)
    ymin = min(y for x, y in image)
    ymax = max(y for x, y in image)
    print("")
    for y in range(ymin - 1, ymax + 2):
        for x in range(xmin - 1, xmax + 2):
            v = image[(x, y)]
            print("." if v == "0" else "#", end="")
        print("\n", end="")


# PART 1
@measure_time
def solve1(data):
    algorithm, image = data
    image = enhance(image, algorithm)
    image = enhance(image, algorithm)
    return len(list(x for x in image.values() if x == "1"))


# PART 2
@measure_time
def solve2(data):
    algorithm, image = data
    for i in range(50):
        image = enhance(image, algorithm)
    return len(list(x for x in image.values() if x == "1"))


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
