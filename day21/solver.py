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
    line0, line1 = raw_data.split("\n")
    return int(line0[-1]), int(line1[-1])


def die_gen(n):
    while True:
        for i in range(1, n + 1):
            yield i


def play_game(start1, start2, die, win_at_score=1000):
    scores = [0, 0]
    pos = [start1, start2]
    n_rolls = 0
    game_ended = False
    while not game_ended:
        for i in range(2):
            pos[i] = (pos[i] - 1 + sum(next(die) for _ in range(3))) % 10 + 1
            scores[i] += pos[i]
            n_rolls += 3
            if scores[i] >= win_at_score:
                game_ended = True
                break
    return tuple(scores), tuple(pos), n_rolls


# PART 1
@measure_time
def solve1(data):
    start1, start2 = data
    die = die_gen(100)
    scores, pos, n_rolls = play_game(start1, start2, die)
    loosing_score = [score for score in scores if score < 1000][0]
    return loosing_score * n_rolls


POSSIBILITIES_FOR = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1
}


def number_of_games_win(scores, pos, player, level=0):
    other_player = (player + 1) % 2
    if scores[other_player] >= 21:
        n_wins = [0, 0]
        n_wins[other_player] = 1
        return n_wins
    n_wins = [0, 0]
    for x, n_possibilities in POSSIBILITIES_FOR.items():
        new_scores = scores[:]
        new_pos = pos[:]
        new_pos[player] = (pos[player] - 1 + x) % 10 + 1
        new_scores[player] += new_pos[player]
        n_wins_0, n_wins_1 = number_of_games_win(
            new_scores,
            new_pos,
            #(player + 1) % 2,
            other_player,
            level=level + 1,
        )
        n_wins[0] += n_possibilities * n_wins_0
        n_wins[1] += n_possibilities * n_wins_1
        if level == 0:
            print(x, n_wins)
    return n_wins


# PART 2
@measure_time
def solve2(data):
    start1, start2 = data
    scores = [0, 0]
    pos = [start1, start2]
    n_wins = number_of_games_win(scores, pos, 0)
    return max(n_wins)


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
