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
    template, rule_lines = raw_data.split("\n\n")
    rules = [line.split(" -> ") for line in rule_lines.split("\n")]
    return template, rules


def update(template, rules):
    new_template = [template[0]]
    for left, right in zip(template, template[1:]):
        key = left + right
        if key in rules:
            new_template.append(rules[key])
            new_template.append(right)
        else:
            new_template.append(right)
    return new_template


# PART 1
@measure_time
def solve1(data, steps=10):
    template, rules = data
    rules = dict(rules)
    for i in range(steps):
        template = update(template, rules)
    quantities = [template.count(q) for q in set(template)]
    return max(quantities) - min(quantities)


def update_counts(pair_counts, element_counts, rules):
    new_pair_counts = pair_counts.copy()
    element_counts = element_counts.copy()
    for rule_key, insertion in rules:
        left, right = rule_key
        new_left = left + insertion
        new_right = insertion + right
        new_pair_counts[rule_key] -= pair_counts[rule_key]
        new_pair_counts[new_left] += pair_counts[rule_key]
        new_pair_counts[new_right] += pair_counts[rule_key]
        element_counts[insertion] += pair_counts[rule_key]
    return new_pair_counts, element_counts


# PART 2
@measure_time
def solve2(data, steps=40):
    template, rules = data
    pair_counts = defaultdict(int)
    element_counts = defaultdict(int)
    for left, right in zip(template, template[1:]):
        pair_counts[left + right] += 1
    for element in template:
        element_counts[element] += 1
    for i in range(steps):
        pair_counts, element_counts = update_counts(pair_counts, element_counts, rules)
    return max(element_counts.values()) - min(element_counts.values())


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
