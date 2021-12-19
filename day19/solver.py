#!/usr/bin/env python

from functools import wraps, cache
from datetime import datetime
import numpy as np

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
    scanner_data = []
    for line in raw_data.split("\n"):
        if line == "":
            continue
        if line.startswith("---"):
            scanner_data.append([])
            continue
        scanner_data[-1].append(tuple(int(i) for i in line.split(",")))
    return scanner_data


def rotate(x, y, z):
    return y, -x, z


def rotate_n(x, y, z, n):
    for i in range(n):
        x, y, z = rotate(x, y, z)
    return x, y, z


POINTING_PERMUTATIONS = [
    lambda x, y, z: (x, y, z),
    lambda x, y, z: (x, z, -y),
    lambda x, y, z: (x, -y, -z),
    lambda x, y, z: (x, -z, y),
    lambda x, y, z: (-z, y, x),
    lambda x, y, z: (z, y, -x)
]


def transform(x, y, z, i_permutation, n_rotations):
    permute = POINTING_PERMUTATIONS[i_permutation]
    return rotate_n(*permute(x, y, z), n=n_rotations)


def transform_and_shift_list(coord_list, i_permutation, n_rotations, shift):
    out = []
    for coords in coord_list:
        x, y, z = transform(*coords, i_permutation, n_rotations)
        dx, dy, dz = shift
        x, y, z = (x - dx, y - dy, z - dz)
        out.append((x, y, z))
    return out


def get_overlap(coords1, coords2, n_for_success=12):
    for i_permutation in range(6):
        for n_rotations in range(4):
            transformed = [transform(*coords, i_permutation, n_rotations) for coords in coords2]
            result = find_shift(coords1, transformed, n_for_success=n_for_success)
            if result is not None:
                shift, overlapping = result
                return i_permutation, n_rotations, shift, overlapping


def find_shift(coords1, coords2, n_for_success):
    set1 = set(coords1)
    for x1, y1, z1 in coords1:
        for x2, y2, z2 in coords2:
            dx, dy, dz = (x2 - x1), (y2 - y1), (z2 - z1)
            shifted = [
                (x - dx, y - dy, z - dz)
                for x, y, z in coords2
            ]
            overlapping = set(shifted).intersection(set1)
            if len(overlapping) >= n_for_success:
                return (dx, dy, dz), overlapping


@cache
def solve(data):
    n_total = len(data)
    scanner_dict = {k: v for k, v in enumerate(data)}
    solved_scanners = {0: scanner_dict.pop(0)}
    scanner_positions = {}
    beacons = set(solved_scanners[0])
    first = 0
    not_overlapping = set()
    while len(solved_scanners) != n_total:

        def run():
            for i, coords in scanner_dict.items():
                for j, coords_solved in solved_scanners.items():
                    if i == j:
                        continue
                    if (i, j) in not_overlapping:
                        continue
                    overlap = get_overlap(coords_solved, coords)
                    if overlap is not None:
                        print(f"Scanner {i} overlaps with scanner {j}")
                        i_permutation, n_rotations, shift, overlapping = overlap
                        print(f"-> Scanner {i} is at {tuple(-k for k in shift)}")
                        scanner_positions[i] = tuple(-k for k in shift)
                        solved_scanners[i] = transform_and_shift_list(
                            scanner_dict.pop(i),
                            i_permutation,
                            n_rotations,
                            shift
                        )
                        beacons.update(solved_scanners[i])
                        return
                    else:
                        not_overlapping.add((i, j))

        run()
    return beacons, scanner_positions


# PART 1
@measure_time
def solve1(data):
    beacons, scanner_positions = solve(tuple(tuple(x) for x in data))
    return len(beacons)


# PART 2
@measure_time
def solve2(data):
    beacons, scanner_positions = solve(tuple(tuple(x) for x in data))
    scanner_positions[0] = (0, 0, 0)
    distances = []
    for x1, y1, z1 in scanner_positions.values():
        for x2, y2, z2 in scanner_positions.values():
            distances.append(abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2))
    return max(distances)


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
