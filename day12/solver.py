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
    return [line.split("-") for line in raw_data.split("\n")]


def possible_paths_from(current_path, edges_from, stopping_condition):
    src = current_path[-1]
    if src == "end":
        return [current_path]
    paths = []
    for dst in edges_from[src]:
        if stopping_condition(dst, current_path):
            continue
        for path in possible_paths_from(current_path + [dst], edges_from, stopping_condition):
            if len(path) == 0:
                continue
            if path[-1] == "end":
                paths.append(path)
    return paths


def get_edges_from(data):
    edges_from = defaultdict(list)
    for src, dst in data:
        edges_from[src].append(dst)
        edges_from[dst].append(src)
    return edges_from


# PART 1
@measure_time
def solve1(data):
    return len(
        possible_paths_from(
            ["start"],
            get_edges_from(data),
            # visit small caves at most once
            lambda dst, current_path: dst.islower() and dst in current_path,
        )
    )


# PART 2
@measure_time
def solve2(data):
    return len(
        possible_paths_from(
            ["start"],
            get_edges_from(data),
            lambda dst, current_path: (
                # don't go back to start
                dst == "start"
                # visit at most one small cave twice
                or (
                    dst.islower() and dst in current_path
                    and any(
                        current_path.count(other) >= 2
                        for other in set(current_path) if other.islower()
                    )
                )
            ),
        )
    )


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
