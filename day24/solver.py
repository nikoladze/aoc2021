#!/usr/bin/env python

from functools import wraps, cache
from datetime import datetime
from collections import defaultdict
from itertools import product
from dataclasses import dataclass
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


class HaltAndCatchFire(Exception):
    """
    (Program authors should be especially cautious; attempting to execute div
    with b=0 or attempting to execute mod with a<0 or b<=0 will cause the
    program to crash and might even damage the ALU. These operations are never
    intended in any serious ALU program.)
    """
    pass


def run(data, input_digits, z_start=None, verbose=False):
    variables = defaultdict(int)
    if z_start is not None:
        variables["z"] = z_start
    for line in data:
        ins = line[0]
        a = line[1]
        if len(line) == 3:
            b = line[2]
            try:
                b = int(b)
            except ValueError:
                b = variables[b]
        if ins == "inp":
            variables[a] = input_digits.pop(0)
        elif ins == "add":
            variables[a] = variables[a] + b
        elif ins == "mul":
            variables[a] = variables[a] * b
        elif ins == "div":
            if b == 0:
                raise HaltAndCatchFire("Division by zero")
            variables[a] = variables[a] // b
        elif ins == "mod":
            if variables[a] < 0 or b <= 0:
                raise HaltAndCatchFire("Negative numbers in modulo will destroy MONAD!")
            variables[a] = variables[a] % b
        elif ins == "eql":
            variables[a] = int(variables[a] == b)
        if verbose:
            print(line, variables)
    return variables


def split_blocks(data):
    input_blocks = []
    for line in data:
        if line[0] == "inp":
            input_blocks.append([])
        input_blocks[-1].append(line)
    return input_blocks


def get_coeffs(block):
    a = block[4][2]
    b = block[5][2]
    c = block[-3][2]
    return int(a), int(b), int(c)

def calculate_z0_options(block, z1, w):
    """
    all blocks after an input instruction have the following structure:

    inp w
    mul x 0  # x = 0
    add x z  # x = z0
    mod x 26 # x = z0 % 26
    div z a  # z1 = z0 / a
    add x b  # x = (z0 % 26) + b
    eql x w  # x = int((z0 % 26) + b == w)
    eql x 0  # x = int((z0 % 26) + b != w)
    mul y 0  # y = 0
    add y 25 # y = 25
    mul y x  # y = 25 * x
    add y 1  # y = 25 * x + 1
    mul z y  # z1 = (z0 / a) * (25 * x + 1)
    mul y 0  # y = 0
    add y w  # y = w
    add y c  # y = w + c
    mul y x  # y = (w + c) * x
    add z y  # z1 = (z0 / a) * (25 * x + 1) + (w + c) * x

    => z0 = (z1 - (w + c) * x) / (25 * x + 1) * a  # + 0 ... a - 1 because of rounding division
    """
    options = []
    a, b, c = get_coeffs(block)
    for x in [0, 1]:
        z0 = (z1 - (w + c) * x) / (25 * x + 1)
        if int(z0) != z0:
            # if division doesn't yield integer number this won't work
            # (i think, since we had to multiply integer numbers)
            continue
        z0 = z0 * a
        if z0 < 0:
            # not allowed because it would go into modulo
            continue
        for shift in range(a):
            z_test = z0 + shift
            x_test = z_test % 26 + b
            if int(x_test != w) == x:
                options.append(int(z_test))
    return options


@cache
def find_possible_combinations(block, z_expected, iterate_reversed=True):
    combinations = []
    if iterate_reversed:
        i_range = range(9, 0, -1)
    else:
        i_range = range(1, 10)
    for i in i_range:
        for z_start in calculate_z0_options(block, z_expected, i):
            combinations.append((i, z_start))
    return combinations


def find_valid_number(z_expected, rev_input_blocks, largest=True):
    if len(rev_input_blocks) == 0:
        return []
    if largest:
        iterate_reversed = True
    else:
        iterate_reversed = False
    combinations = find_possible_combinations(
        tuple(tuple(line) for line in rev_input_blocks[0]),
        z_expected,
        iterate_reversed=iterate_reversed,
    )
    for new_digit, new_z_expected in combinations:
        res = find_valid_number(new_z_expected, rev_input_blocks[1:], largest=largest)
        if res is not None:
            return [(new_z_expected, new_digit)] + res
    return None


def solve(data, largest):
    input_blocks = split_blocks(data)
    rev_input_blocks = input_blocks[::-1]
    result = find_valid_number(0, rev_input_blocks, largest=largest)
    test = run(
        data,
        [x[1] for x in result[::-1]],
        z_start=result[-1][0],
    )
    assert test["z"] == 0
    z_start = result[-1][0]
    assert z_start == 0
    return int("".join(str(i) for _, i in result[::-1]))


# PART 1
@measure_time
def solve1(data):
    return solve(data, largest=True)


# PART 2
@measure_time
def solve2(data):
    return solve(data, largest=False)


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

    # blocks = split_blocks(data)
    # for i in range(len(blocks[0])):
    #      for block in blocks:
    #          print(f"{' '.join(block[i]):<12}", end="")
    #      print("\n", end="")
