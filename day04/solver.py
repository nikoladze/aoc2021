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


class Board:

    def __init__(self, data):
        self.board = data
        self.marked = [[False for x in data] for y in data]
        self.done = False

    def mark(self, i):
        for y, row in enumerate(self.board):
            for x, val in enumerate(row):
                if val == i:
                    self.marked[y][x] = True

    def has_win(self):
        if (
            any(all([marked for marked in row]) for row in self.marked)
            or any(all(row[x] for row in self.marked) for x in range(len(self.board)))
        ):
            return True
        return False

    def __repr__(self):
        return (
            "\n".join([" ".join(str(i) for i in row) for row in self.board])
            + "\n\n"
            + "\n".join([" ".join("1" if i else "0" for i in row) for row in self.marked])
            + "\n"
        )


@measure_time
def parse(raw_data):
    raw_data = raw_data.split("\n")
    sequence = [int(i) for i in raw_data[0].split(",")]
    boards = []
    for data in "\n".join(raw_data[1:]).split("\n\n"):
        boards.append(
            Board(
                [[int(i) for i in line.split()] for line in data.split("\n")]
            )
        )
    return sequence, boards


# PART 1
@measure_time
def solve1(data):
    sequence, boards = data
    for i in sequence:
        for board in boards:
            board.mark(i)
            if board.has_win():
                print(board, i)
                sum_unmarked = 0
                for row, row_marked in zip(board.board, board.marked):
                    for val, marked in zip(row, row_marked):
                        if not marked:
                            sum_unmarked += val
                return sum_unmarked * i


# PART 2
@measure_time
def solve2(data):
    sequence, boards = data
    for i in sequence:
        for board in boards:
            board.mark(i)
            if board.has_win() and not board.done:
                board.done = True
                sum_unmarked = 0
                for row, row_marked in zip(board.board, board.marked):
                    for val, marked in zip(row, row_marked):
                        if not marked:
                            sum_unmarked += val
                solution = sum_unmarked * i
    return solution


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
