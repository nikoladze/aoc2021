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
    return [int(i) for i in raw_data.split("\n")]


# PART 1
@measure_time
def solve1(data):
    n = 0
    for i in range(1, len(data)):
        if data[i] > data[i - 1]:
            n += 1
    return n


# PART 2
@measure_time
def solve2(data):
    windows = []
    n = 0
    for i in range(2, len(data)):
        windows.append(data[i - 2] + data[i - 1] + data[i])
        try:
            if windows[-2] < windows[-1]:
                n += 1
        except IndexError:
            pass
    return n


@measure_time
def solve2_alternative(data):
    "David told me he used zip to solve this so i had to ..."
    windows = list(map(sum, zip(data, data[1:], data[2:])))
    return sum(a < b for a, b in zip(windows, windows[1:]))


if __name__ == "__main__":
    import sys

    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))
    print("Part 2: {}".format(solve2_alternative(data)))

    print("\nTime taken:")
    for func, time in times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in times)))
