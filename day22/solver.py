#!/usr/bin/env python

from functools import wraps
from datetime import datetime
from collections import defaultdict
from itertools import product
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


def parse_gen(raw_data):
    for line in raw_data.split("\n"):
        onoff, coords = line.split()
        xr, yr, zr = coords.split(",")
        xr, yr, zr = [tuple(int(i) for i in s.split("=")[1].split("..")) for s in [xr, yr, zr]]
        yield onoff, xr, yr, zr


@measure_time
def parse(raw_data):
    return list(parse_gen(raw_data))


# PART 1
@measure_time
def solve1(data):
    cubes = defaultdict(bool)
    for onoff, xr, yr, zr in data:
        if any(r[0] < -50 or r[1] > 50 for r in (xr, yr, zr)):
            continue
        for x, y, z in product(
            range(xr[0], xr[1] + 1),
            range(yr[0], yr[1] + 1),
            range(zr[0], zr[1] + 1),
        ):
            cubes[(x, y, z)] = True if onoff == "on" else False
    return len([i for i in cubes.values() if i])


def find_bin_edges(data):
    edges_x = set()
    edges_y = set()
    edges_z = set()
    for onoff, xr, yr, zr in data:
        for edges, r in [(edges_x, xr), (edges_y, yr), (edges_z, zr)]:
            edges.add(r[0])
            # value of upper bin edge not included in bin
            edges.add(r[1] + 1)
    return sorted(edges_x), sorted(edges_y), sorted(edges_z)


def digitize(coord_range, bin_edges):
    indices = []
    for i, (low, up) in enumerate(zip(bin_edges, bin_edges[1:])):
        if low >= coord_range[0] and (up - 1) <= coord_range[1]:
            indices.append(i)
    return indices


# PART 2
@measure_time
def solve2(data):
    #cube_bin_indices = defaultdict(bool)
    ex, ey, ez = find_bin_edges(data)
    hist = np.zeros((len(ex) - 1, len(ey) - 1, len(ez) - 1), dtype=np.uint8)
    # volumen of each bin will be given by abs(ex[i + 1] - ex[i]) * abs(ey[j + 1] - ey[j]) ...
    from tqdm.auto import tqdm
    for onoff, xr, yr, zr in tqdm(data):
        # cuboids[(xr, yr, zr)] = True if onoff == "on" else False
        # n_on += abs(xr[1] - xr[0]) * abs(yr[1] - yr[0]) * abs(zr[1] - zr[0])
        # bin indices
        for ix, iy, iz in product(
                digitize(xr, ex),
                digitize(yr, ey),
                digitize(zr, ez),
        ):
            #cube_bin_indices[(ix, iy, iz)] = True if onoff == "on" else False
            hist[ix, iy, iz] = True if onoff == "on" else False
        #print(len(cube_bin_indices))
    # n_on = 0
    n_on = 0
    for ix, iy, iz in product(
            range(hist.shape[0]),
            range(hist.shape[1]),
            range(hist.shape[2]),
    ):
        if not hist[ix, iy, iz]:
            continue
        n_on += abs(ex[ix + 1] - ex[ix]) * abs(ey[iy + 1] - ey[iy]) * abs(ez[iz + 1] - ez[iz])
    # for (ix, iy, iz), is_on in cube_bin_indices.items():
    #     if not is_on:
    #         continue
    #     n_on += abs(ex[ix + 1] - ex[ix]) * abs(ey[iy + 1] - ey[iy]) * abs(ez[iz + 1] - ez[iz])
    return n_on
    # return hist.sum()


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
