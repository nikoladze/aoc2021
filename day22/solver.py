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
    ex, ey, ez = find_bin_edges(data)
    hist = np.zeros((len(ex) - 1, len(ey) - 1, len(ez) - 1), dtype=np.uint8)
    from tqdm.auto import tqdm
    for onoff, xr, yr, zr in tqdm(data):
        for ix, iy, iz in product(
                digitize(xr, ex),
                digitize(yr, ey),
                digitize(zr, ez),
        ):
            hist[ix, iy, iz] = True if onoff == "on" else False
    ex, ey, ez = (np.array(e) for e in (ex, ey, ez))
    wx, wy, wz = (e[1:] - e[:-1] for e in (ex, ey, ez))
    n_on = 0
    # iterate first dimension to save memory 🙈
    for i in range(len(wx)):
        wxx, wyy, wzz = np.meshgrid(wx[i], wy, wz, indexing='ij', sparse=True)
        n_on += (hist[i] * wxx * wyy * wzz).sum()
    return n_on


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
