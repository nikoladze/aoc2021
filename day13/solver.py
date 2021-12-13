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
    coord_block, instruction_block = raw_data.split("\n\n")
    coords = [[int(i) for i in line.split(",")] for line in coord_block.split("\n")]
    instructions = []
    for line in instruction_block.split("\n"):
        instruction = line.split()[-1]
        axis, pos = instruction.split("=")
        instructions.append((axis, int(pos)))
    return coords, instructions


def fold_left(coords, pos):
    new_coords = []
    for x, y in coords:
        if x > pos:
            new_coords.append((2 * pos - x, y))
        else:
            new_coords.append((x, y))
    return new_coords


def fold_up(coords, pos):
    new_coords = []
    for x, y in coords:
        if y > pos:
            new_coords.append((x, 2 * pos - y))
        else:
            new_coords.append((x, y))
    return new_coords


def fold(coords, instruction):
    if instruction[0] == "x":
        return fold_left(coords, instruction[1])
    else:
        return fold_up(coords, instruction[1])


# PART 1
@measure_time
def solve1(data):
    coords, instructions = data
    new_coords = fold(coords, instructions[0])
    return len(set(tuple(c) for c in new_coords))


# PART 2
@measure_time
def solve2(data):
    coords, instructions = data
    new_coords = coords
    for instruction in instructions:
        new_coords = fold(new_coords, instruction)
    new_coords = set(tuple(c) for c in new_coords)
    output = []
    output.append("\n")
    for y in range(max(y for x, y in new_coords) + 1):
        for x in range(max(x for x, y in new_coords) + 1):
            if (x, y) in new_coords:
                output.append("█")
            else:
                output.append(" ")
        output.append("\n")
    return "".join(output)


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
