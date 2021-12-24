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
    out = []
    for line in raw_data.split("\n"):
        out.append(list(line))
    return out


class AmphiGame:
    def __init__(self, data):
        self.map = data
        #self.possible_pos = sum([[(i, j) for j, v in enumerate(line) if v in ".ABCD"] for i, line in enumerate(self.map)], [])
        self.destinations = dict(zip("ABCD", [3, 5, 7, 9]))
        # self.destinations = dict(zip("ABCD", range(4)))
        self.energies = dict(zip("ABCD", map(lambda x: 10 ** x, range(4))))
        # self.hallway = ["."] * 11
        # self.entrances = [2, 4, 6, 8]
        # self.map = [self.hallway] + self.rooms

    @property
    def occupied(self):
        for y, line in enumerate(self.map):
            for x, v in enumerate(line):
                if v in "ABCD":
                    yield (x, y)

    def possible_step(self, src, dst):
        x1, y1 = src
        x2, y2 = dst

        # spot free?
        if self.map[y2][x2] != ".":
            return False

        # adjacent?
        if not (abs(x2 - x1) == 1 or abs(y2 - y1) == 1):
            return False

        # if in hallway i can only go to final destination
        # (and the other one also has to be there)
        if y2 not in (2, 3):
            val = self.map[y1][x1]
            if self.destinations[val] != x2:
                return False
            if self.map[[y for y in (2, 3) if not y == y2][0]][x2] != val:
                return False

        return True

    def possible_paths_from(self, current_path):
        src = current_path[-1]
        paths = []
        for step in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            dst = (src[0] + step[0], src[1] + step[1])
            if not self.possible_step(src, dst):
                continue
            if dst in current_path:
                # don't go back
                continue
            for path in self.possible_paths_from(current_path + [dst]):
                paths.append(path)
        if len(paths) == 0:
            return [current_path]
        return paths

    @property
    def is_done(self):
        for x, y, expected in [
            (3, 2, "A"),
            (3, 3, "A"),
            (5, 2, "B"),
            (5, 3, "B"),
            (7, 2, "C"),
            (7, 3, "C"),
        ]:
            if self.map[y][x] != expected:
                return False
        return True

    # def find_min_energy(self):
    #     energies = []
    #     for src in self.occupied:
    #         c = self.map[src[1]][src[0]]
    #         for path in self.possible_paths_from([src]):
    #             energy = 0
    #             for pos in path[1:]:
    #                 energy += self.energies[c]
    #                 game = AmphiGame([line[:] for line in self.map])
    #                 print(src, pos)
    #                 game.map[src[1]][src[0]] = "."
    #                 game.map[pos[1]][pos[0]] = c
    #                 print(game)
    #                 if game.is_done:
    #                     energies.append(energy)
    #                     continue
    #                 min_energy_next = game.find_min_energy()
    #                 energies.append(energy + min_energy_next)
    #     return min(energies)


    def find_min_energy(self):
        for src in self.occupied:
            for step in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
                dst = (src[0] + step[0], src[1] + step[1])
            if not self.possible_step(src, dst):
                continue
            if dst in current_path:
                # don't go back
                continue
            for path in self.possible_paths_from(current_path + [dst]):
                paths.append(path)
        src = current_path[-1]
        paths = []
        for step in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            dst = (src[0] + step[0], src[1] + step[1])
            if not self.possible_step(src, dst):
                continue
            if dst in current_path:
                # don't go back
                continue
            for path in self.possible_paths_from(current_path + [dst]):
                paths.append(path)
        if len(paths) == 0:
            return [current_path]
        return paths

    def __repr__(self):
        return "\n".join("".join(line) for line in self.map)


# PART 1
@measure_time
def solve1(data):
    pass


# PART 2
@measure_time
def solve2(data):
    pass


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

    # interactive testing
    game = AmphiGame(data)
