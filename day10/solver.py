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
    return [line for line in raw_data.split("\n")]


MATCHING_PARENS = {"{": "}", "[": "]", "(": ")", "<": ">"}

def check_line(line):
    err = None
    exp = None

    def check(line, pos=0, expected=None):
        nonlocal err
        nonlocal exp
        if len(line) == 0:
            exp = expected
            raise StopIteration("Done")
        first = line[0]
        if first in "([{<":
            opening = first
            closing, rest, pos = check(line[1:], pos + 1, expected=MATCHING_PARENS[opening])
            if closing != MATCHING_PARENS[opening]:
                err = closing, pos
                raise SyntaxError(f"Expected {MATCHING_PARENS[opening]}, but found {closing} instead. Rest: {rest}")
            return check(rest, pos + 1, expected=expected)
        else:
            return first, line[1:], pos

    try:
        check(line)
    except StopIteration:
        return exp
    except SyntaxError:
        return err


ERR_SCORES = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


# PART 1
@measure_time
def solve1(data):
    score = 0
    for line in data:
        res = check_line(line)
        if res is None:
            continue
        if isinstance(res, tuple):
            closing, pos = res
            score += ERR_SCORES[closing]
            continue
    return score


def complete(line):
    closing_sequence = []
    while True:
        res = check_line(line + "".join(closing_sequence))
        if res is None or isinstance(res, tuple):
            return closing_sequence
        if isinstance(res, str):
            closing_sequence.append(res)


COMPLETION_ERR_SCORES = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


# PART 2
@measure_time
def solve2(data):
    scores = []
    for line in data:
        closing_sequence = complete(line)
        score = 0
        if len(closing_sequence) > 0:
            for c in closing_sequence:
                score = score * 5 + COMPLETION_ERR_SCORES[c]
            scores.append(score)
    return sorted(scores)[len(scores) // 2]


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
