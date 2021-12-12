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


# PART 1
@measure_time
def solve1(data):
    edges_from = defaultdict(list)
    for src, dst in data:
        edges_from[src].append(dst)
        edges_from[dst].append(src)

    #visited_big = set()
    #possible_paths = []

    def possible_paths_from(current_path):
        #print(f"possible_paths_from({current_path})")
        src = current_path[-1]
        if src == "end":
            return [current_path]
        paths = []
        #print(f"edges from {src}: {edges_from[src]}")
        for dst in edges_from[src]:
            #print(f"My path so far: {current_path}, Looking for paths through {dst}")
            if dst.islower() and dst in current_path:
                #print(f"{dst} is a small cave already visited!")
                continue
            for path in possible_paths_from(current_path + [dst]):
                if len(path) == 0:
                    continue
                if path[-1] == "end":
                    paths.append(path)
        return paths

    possible_paths = possible_paths_from(["start"])

    return len(possible_paths)


# PART 2
@measure_time
def solve2(data):
    edges_from = defaultdict(list)
    for src, dst in data:
        edges_from[src].append(dst)
        edges_from[dst].append(src)

    def possible_paths_from(current_path):
        #print(f"possible_paths_from({current_path})")
        src = current_path[-1]
        if src == "end":
            return [current_path]
        paths = []
        #print(f"edges from {src}: {edges_from[src]}")
        for dst in edges_from[src]:
            #print(f"My path so far: {current_path}, Looking for paths through {dst}")
            if dst == "start":
                continue
            if (
                    dst.islower() and dst in current_path
                    and any(current_path.count(other) >= 2 for other in set(current_path) if other.islower())
            ):
                # print(f"{dst} is a small cave already visited!")
                continue

            for path in possible_paths_from(current_path + [dst]):
                if len(path) == 0:
                    continue
                if path[-1] == "end":
                    paths.append(path)
        return paths

    possible_paths = possible_paths_from(["start"])

    #breakpoint()
    return len(possible_paths)


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
