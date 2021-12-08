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


def parse_generator(raw_data):
    for line in raw_data.split("\n"):
        sequence, output = line.split("|")
        yield sequence.split(), output.split()

@measure_time
def parse(raw_data):
    return list(parse_generator(raw_data))


N_ACTIVATED = {
    0: 6,
    1: 2,
    2: 5,
    3: 5,
    4: 4,
    5: 5,
    6: 6,
    7: 3,
    8: 7,
    9: 6,
}

# PART 1
@measure_time
def solve1(data):
    unique_lens = set(N_ACTIVATED[i] for i in [1, 4, 7, 8])
    total = 0
    for sequence, output in data:
        for digit in output:
            if len(digit) in unique_lens:
                total += 1
    return total


def find_numbers(sequence):
    sequence = set(frozenset(i) for i in sequence)
    found_numbers = {
        k: [frozenset(x) for x in sequence if len(x) == N_ACTIVATED[k]][0]
        for k in [1, 4, 7, 8]
    }

    def matches(length, filter):
        found = [
            frozenset(x)
            for x in sequence
            if (
                len(x) == length
                and filter(set(x))
                and not frozenset(x) in found_numbers.values()
            )
        ]
        assert len(found) == 1
        return found[0]

    bd = found_numbers[4].difference(found_numbers[1])
    found_numbers[0] = matches(6, lambda x: not bd.issubset(x))
    cf = found_numbers[1]
    found_numbers[6] = matches(6, lambda x: not cf.issubset(x))
    found_numbers[9] = matches(6, lambda x: True)
    found_numbers[5] = matches(5, lambda x: bd.issubset(x))
    found_numbers[3] = matches(5, lambda x: cf.issubset(x))
    found_numbers[2] = matches(5, lambda x: True)
    return {v: k for k, v in found_numbers.items()}


# PART 2
@measure_time
def solve2(data):
    total = 0
    for sequence, output in data:
        number_map = find_numbers(sequence + output)
        total += int("".join(str(number_map[frozenset(letters)]) for letters in output))
    return total


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
