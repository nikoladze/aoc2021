#!/usr/bin/env python

from functools import wraps
from datetime import datetime
from collections import defaultdict
from itertools import product
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
    instructions = []
    for line in raw_data.split("\n"):
        instructions.append(line.split())
    return instructions


def run(instructions, input_digits):
    variables = defaultdict(int)
    for line in data:
        ins = line[0]
        if len(line) == 2:
            var = line[1]
        if len(line) == 3:
            var = line[1]
            val = line[2]
            try:
                val = int(val)
            except ValueError:
                val = variables[val]
        #print(line)
        if ins == "inp":
            variables[var] = input_digits.pop(0)
        elif ins == "add":
            variables[var] = variables[var] + val
        elif ins == "mul":
            variables[var] = variables[var] * val
        elif ins == "div":
            variables[var] = int(variables[var] / val)
        elif ins == "mod":
            # TODO: is this correct here??
            #variables[var] = variables[var] % val
            variables[var] = val - int(variables[var] / val) * val
        elif ins == "eql":
            variables[var] = int(variables[var] == val)
    return variables


# PART 1
@measure_time
def solve1(data):
    #for i, digit in enumerate(product(*([range(1, 10)] * 14))):
    # for i, digit in enumerate(product(*([range(9, 0, -1)] * 14))):
    #     res = run(data, list(digit))
    #     print(int("".join(str(d) for d in digit)), res)
    #     if i > 1000:
    #         break

    #print(run(data, [int(i) for i in "13579246899999"]))
    # print(run(data, [int(i) for i in "11111111111111"]))
    # print(run(data, [int(i) for i in "21111111111111"]))
    # print(run(data, [int(i) for i in "12111111111111"]))
    # print(run(data, [int(i) for i in "11211111111111"]))
    # print(run(data, [int(i) for i in "11121111111111"]))
    # print(run(data, [int(i) for i in "11112111111111"]))
    from random import randint
    [random.randint(1, 9) for i in range(14)]


# PART 2
@measure_time
def solve2(data):
    pass


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
