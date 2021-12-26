#!/usr/bin/env python

from functools import wraps
from datetime import datetime
from tqdm import tqdm

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


min_energy_for_map = {}

class AmphiGame:
    def __init__(self, data):
        self.map = data
        self.destinations = dict(zip("ABCD", [3, 5, 7, 9]))
        self.energies = dict(zip("ABCD", map(lambda x: 10 ** x, range(4))))
        self._highlight = None
        self._occupied = None
        self._unoccupied = None

    @property
    def occupied(self):
        if self._occupied is not None:
            return self._occupied
        self._occupied = []
        for y, line in enumerate(self.map):
            for x, v in enumerate(line):
                if v in "ABCD":
                    self._occupied.append((x, y))
        return self._occupied

    @property
    def unoccupied(self):
        if self._unoccupied is not None:
            return self._unoccupied
        self._unoccupied = []
        for y, line in enumerate(self.map):
            for x, v in enumerate(line):
                if v == ".":
                    self._unoccupied.append((x, y))
        return self._unoccupied

    def possible_move(self, src, dst):
        x1, y1 = src
        x2, y2 = dst

        # spot free/visitable?
        if self.map[y2][x2] != ".":
            assert False ### TODO
            return False

        # moving to a spot in front of a room is not allowed
        if y2 == 1 and x2 in (3, 5, 7, 9):
            return False

        # can't go from hallway to hallway
        if y1 == 1 and y2 == 1:
            return False

        # we have to go to the hallway if we are in the room
        if y1 in (2, 3)  and y2 != 1:
            return False

        # if that room is done, we stay there
        if y1 in (2, 3):
            val = self.map[y1][x1]
            other_y = 2 if y1 == 3 else 3
            other_val = self.map[other_y][x1]
            if self.destinations[val] == x1:
                if val == other_val:
                    return False
                if y1 == 3:
                    return False

        # if in hallway i can only go to final destination
        # (and the other one also has to be there or empty)
        if y1 == 1 and y2 in (2, 3):
            val = self.map[y1][x1]
            if self.destinations[val] != x2:
                return False
            if y2 == 2 and self.map[3][x2] != val:
                return False

        # if no contiguous path of free fields between src and dst we can't do this
        if self.possible_path_distance(src, dst) is None:
            return False

        return True

    def possible_path_distance(self, src, dst, current_path=None):
        "this routine might be problematic ..."
        if current_path is None:
            current_path = [src]
        src = current_path[-1]
        distance = None
        for step in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            pos = (src[0] + step[0], src[1] + step[1])
            if pos == dst:
                return len(current_path)
            if self.map[pos[1]][pos[0]] != ".":
                continue
            if pos in current_path:
                # don't go back
                continue
            if (distance := self.possible_path_distance(pos, dst, current_path + [pos])) is not None:
                break
        return distance

    @property
    def is_done(self):
        for x, y, expected in [
            (3, 2, "A"),
            (3, 3, "A"),
            (5, 2, "B"),
            (5, 3, "B"),
            (7, 2, "C"),
            (7, 3, "C"),
            (9, 2, "D"),
            (9, 3, "D"),
        ]:
            if self.map[y][x] != expected:
                return False
        return True

    @property
    def map_key(self):
        return tuple(tuple(line) for line in self.map)

    def find_min_energy(self, energy_so_far=0, min_energy=None, history=None, level=0):
        if history is None:
            history = set([self.map_key])
        if level == 0:
            iter_occ = tqdm(self.occupied)
        else:
            iter_occ = self.occupied
        for src in iter_occ:
            c = self.map[src[1]][src[0]]
            if min_energy is not None and energy_so_far + self.energies[c] >= min_energy:
                # need to do at least one step ...
                continue
            if level == 0:
                iter_unocc = tqdm(self.unoccupied)
            else:
                iter_unocc = self.unoccupied
            for pos in iter_unocc:
                if not self.possible_move(src, pos):
                    continue
                distance = self.possible_path_distance(src, pos)
                energy = energy_so_far + self.energies[c] * distance
                if min_energy is not None and energy >= min_energy:
                    continue
                game = AmphiGame([line[:] for line in self.map])
                game.map[src[1]][src[0]] = "."
                game.map[pos[1]][pos[0]] = c
                if game.map_key in min_energy_for_map and min_energy_for_map[game.map_key] <= energy:
                    continue
                else:
                    min_energy_for_map[game.map_key] = energy
                if game.map_key in history:
                    continue
                if game.is_done:
                    print("Done!")
                    print(energy)
                    min_energy_next = energy
                else:
                    min_energy_next = game.find_min_energy(
                        energy_so_far=energy,
                        min_energy=min_energy,
                        history=history | set([game.map_key]),
                        level=level + 1,
                    )
                if min_energy_next is None:
                    continue
                if min_energy is None or min_energy_next < min_energy:
                    min_energy = min_energy_next
        return min_energy

    def __repr__(self):
        return "\n".join(
            "".join(
                v if (x, y) != self._highlight else f"\033[;1m{v}\033[0m"
                for x, v in enumerate(line)
            )
            for y, line in enumerate(self.map)
        )

    def print_highlight(self, pos, indent=""):
        self._highlight = pos
        for line in self.__repr__().split("\n"):
            print(indent + line)
        self._highlight = None


# PART 1
@measure_time
def solve1(data):
    game = AmphiGame(data)
    return game.find_min_energy()


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
    # game = AmphiGame(data)

    # interactive testing
    # from test_solver import TESTDATA
    # game = AmphiGame(parse(TESTDATA.strip()))
