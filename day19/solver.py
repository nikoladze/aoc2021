#!/usr/bin/env python

from functools import wraps
from itertools import permutations
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
    scanner_data = []
    for line in raw_data.split("\n"):
        if line == "":
            continue
        if line.startswith("---"):
            scanner_data.append([])
            continue
        scanner_data[-1].append(tuple(int(i) for i in line.split(",")))
    return scanner_data


def rotate(x, y, z, axis):
    return [
        (x, z, -y),
        (z, y, -x),
        (y, -x, z),
    ][axis]


def rotate_n(x, y, z, axis, n):
    for i in range(n):
        x, y, z = rotate(x, y, z, axis)
    return x, y, z


def flip(x, y, z, do_flip=True):
    if not do_flip:
        return x, y, z
    return -x, y, z


def all_transformations1(x, y, z):
    res = []
    for axis_rotate in range(3):
        for n_rotations in range(4):
            for do_flip in [True, False]:
                res.append(flip(
                        *rotate_n(
                            x, y, z,
                            axis=axis_rotate,
                            n=n_rotations,
                        ),
                        do_flip=do_flip,
                    ))
    return res


def all_transformations2(x, y, z):
    # res = []
    # for axis_rotate in range(3):
    #     for n_rotations in range(4):
    #         for do_flip in [True, False]:
    #             res.append(flip(
    #                     *rotate_n(
    #                         x, y, z,
    #                         axis=axis_rotate,
    #                         n=n_rotations,
    #                     ),
    #                     do_flip=do_flip,
    #                 ))
    # return res
    for permutation_indices in permutations([0, 1, 2]):
        for n in range(4):
            print([(x, y, z)[i] for i in permutation_indices])
            yield rotate_n(*[(x, y, z)[i] for i in permutation_indices], axis=0, n=n)
    # for x_new, y_new, z_new in permutations([x, y, z]):
    #     for n in range(4):
    #         yield rotate_n(x_new, y_new, z_new, axis=0, n=n)


def all_transformations3(x, y, z):
    for i_permutation, permute in enumerate(POINTING_PERMUTATIONS):
        for n_rotations in range(4):
            yield rotate_n(
                *permute(x, y, z),
                axis=2,
                n=n_rotations,
            )

POINTING_PERMUTATIONS = [
    lambda x, y, z: (x, y, z),
    lambda x, y, z: (x, z, -y),
    lambda x, y, z: (x, -y, -z),
    lambda x, y, z: (x, -z, y),
    lambda x, y, z: (-z, y, x),
    lambda x, y, z: (z, y, -x)
]


# def get_overlap(coords1, coords2, n_for_success=12):
#     for axis_rotate in range(3):
#         for n_rotations in range(4):
#             for do_flip in [True, False]:
#                 transformed = [
#                     flip(
#                         *rotate_n(
#                             *coords,
#                             axis=axis_rotate,
#                             n=n_rotations,
#                         ),
#                         do_flip=do_flip,
#                     )
#                     for coords in coords2
#                 ]
#                 overlapping = find_shift(coords1, transformed, n_for_success=n_for_success)
#                 if overlapping is not None:
#                     return (axis_rotate, n_rotations, do_flip), overlapping
#

def transform(x, y, z, i_permutation, n_rotations):
    permute = POINTING_PERMUTATIONS[i_permutation]
    return rotate_n(*permute(x, y, z), axis=2, n=n_rotations)


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
            permute = POINTING_PERMUTATIONS[i_permutation]
            transformed = [
                rotate_n(
                    #*coords,
                    *permute(*coords),
                    axis=2,
                    n=n_rotations,
                )
                for coords in coords2
            ]
            #transformed = [transform(*coords, i_permutation, n_rotations) for coords in coords2]
            #print(transformed)
            result = find_shift(coords1, transformed, n_for_success=n_for_success)
            if result is not None:
                shift, overlapping = result
                return i_permutation, n_rotations, shift, overlapping


def find_shift(coords1, coords2, n_for_success):
    for x1, y1, z1 in coords1:
        for x2, y2, z2 in coords2:
            dx, dy, dz = (x2 - x1), (y2 - y1), (z2 - z1)
            shifted = [
                (x - dx, y - dy, z - dz)
                for x, y, z in coords2
            ]
            overlapping = [coords for coords in shifted if coords in coords1]
            if len(overlapping) >= n_for_success:
                return (dx, dy, dz), overlapping


# PART 1
@measure_time
def solve1(data):
    n_total = len(data)
    scanner_dict = {k: v for k, v in enumerate(data)}
    solved_scanners = {0: scanner_dict.pop(0)}
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
                    #overlap = get_overlap(coords, coords_solved)
                    overlap = get_overlap(coords_solved, coords)
                    if overlap is not None:
                        print(f"Scanner {i} overlaps with scanner {j}")
                        i_permutation, n_rotations, shift, overlapping = overlap
                        print(f"-> Scanner {i} is at {tuple(-k for k in shift)}")
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
    #breakpoint()
    return len(beacons)

        


# PART 2
@measure_time
def solve2(data):
    n_total = len(data)
    scanner_dict = {k: v for k, v in enumerate(data)}
    solved_scanners = {0: scanner_dict.pop(0)}
    beacons = set(solved_scanners[0])
    first = 0
    not_overlapping = set()
    scanner_positions = {}
    while len(solved_scanners) != n_total:

        def run():
            for i, coords in scanner_dict.items():
                for j, coords_solved in solved_scanners.items():
                    if i == j:
                        continue
                    if (i, j) in not_overlapping:
                        continue
                    #overlap = get_overlap(coords, coords_solved)
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
    #breakpoint()
    #return len(beacons)
    distances = []
    for i in range(n_total):
        for j in range(n_total):
            x1, y1, z1 = scanner_positions[i]
            x2, y2, z2 = scanner_positions[j]
            distances.append(abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2))
    return max(distances)

if __name__ == "__main__":
    import sys

    data = parse(open("input.txt").read().strip())
    #print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in times)))
