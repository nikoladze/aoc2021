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


def tokenize(line):
    return [t for t in line if t != ","]


@measure_time
def parse(raw_data):
    return [tokenize(line) for line in raw_data.split("\n")]


def find_exploding_pair(tokens):
    level = 0
    for i, t in enumerate(tokens):
        if t == "[":
            level += 1
            continue
        if t == "]":
            level -= 1
            continue
        if level > 4 and tokens[i].isnumeric() and tokens[i + 1].isnumeric():
            return i - 1


def find_large_number(tokens):
    for i, t in enumerate(tokens):
        if t.isnumeric() and int(t) >= 10:
            return i


def explode_pair_at(tokens, i):
    tokens.pop(i) # [
    left = tokens.pop(i)
    right = tokens.pop(i)
    tokens.pop(i) # ]
    for j in range(i - 1, -1, -1):
        if tokens[j].isnumeric():
            tokens[j] = str(int(left) + int(tokens[j]))
            break
    for j in range(i, len(tokens)):
        if tokens[j].isnumeric():
            tokens[j] = str(int(right) + int(tokens[j]))
            break
    tokens.insert(i, "0")


def split_number_at(tokens, i):
    n = int(tokens.pop(i))
    tokens.insert(i, "]")
    tokens.insert(i, str(math.ceil(n / 2)))
    tokens.insert(i, str(math.floor(n / 2)))
    tokens.insert(i, "[")



def reduce_snailnum(tokens):
    while True:
        if (i := find_exploding_pair(tokens)) is not None:
            explode_pair_at(tokens, i)
            continue
        if (i := find_large_number(tokens)) is not None:
            split_number_at(tokens, i)
            continue
        break


def add_snailnums(tokens1, tokens2):
    sum_tokens = ["["] + tokens1 + tokens2 + ["]"]
    reduce_snailnum(sum_tokens)
    return sum_tokens


def sum_snailnums(token_list):
    total = token_list[0]
    for other in token_list[1:]:
        total = add_snailnums(total, other)
    return total


def to_string(tokens):
    return ",".join(tokens).replace("[,", "[").replace(",]", "]")


def reduce_magnitude(tokens):
    tokens = tokens[:]
    while True:
        for i, t in enumerate(tokens):
            if t == "[" and tokens[i + 1].isnumeric() and tokens[i + 2].isnumeric():
                tokens.pop(i)
                magnitude = 3 * int(tokens.pop(i))
                magnitude += 2 * int(tokens.pop(i))
                tokens.pop(i)
                tokens.insert(i, str(magnitude))
                break
        else:
            break
    return tokens


# PART 1
@measure_time
def solve1(data):
    return int(reduce_magnitude(sum_snailnums(data))[0])


# PART 2
@measure_time
def solve2(data):
    magnitudes = []
    for n1 in data:
        for n2 in data:
            magnitudes.append(int(reduce_magnitude(add_snailnums(n1, n2))[0]))
    return max(magnitudes)


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
