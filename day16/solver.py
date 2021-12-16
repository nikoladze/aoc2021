#!/usr/bin/env python

from functools import wraps, reduce
from operator import mul
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

HEX2BIT = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}

@measure_time
def parse(raw_data):
    return "".join([HEX2BIT[i] for i in raw_data])


class Decoder:
    def __init__(self, data):
        self.pos = 0
        self.data = data
        self.version_sum = 0

    def read(self, n, as_bits=False):
        pos = self.pos
        self.pos += n
        out = self.data[pos : pos + n]
        if as_bits:
            return out
        else:
            return int(out, 2)

    def parse_literal(self):
        value_bits = []
        last_group = False
        while not last_group:
            last_group = self.read(1) == 0
            value_bits.append(self.read(4, as_bits=True))
        return int("".join(value_bits), 2)

    def parse_operator(self, type_id):
        length_type_id = self.read(1)
        results = []
        if length_type_id == 0:
            total_length = self.read(15)
            stop = self.pos + total_length
            while self.pos != stop:
                results.append(self.parse())
        else:
            number_of_subpackets = self.read(11)
            for i in range(number_of_subpackets):
                results.append(self.parse())
        if type_id == 0:
            return sum(results)
        elif type_id == 1:
            return reduce(mul, results)
        elif type_id == 2:
            return min(results)
        elif type_id == 3:
            return max(results)
        elif type_id == 5:
            return 1 if results[0] > results[1] else 0
        elif type_id == 6:
            return 1 if results[0] < results[1] else 0
        elif type_id == 7:
            return 1 if results[0] == results[1] else 0
        raise Exception(f"Unknown type_id {type_id}")

    def parse(self):
        while self.pos < len(self.data):
            packet_version = self.read(3)
            self.version_sum += packet_version
            type_id = self.read(3)
            if type_id == 4:
                return self.parse_literal()
            else:
                return self.parse_operator(type_id)


# PART 1
@measure_time
def solve1(data):
    decoder = Decoder(data)
    decoder.parse()
    return decoder.version_sum

# PART 2
@measure_time
def solve2(data):
    decoder = Decoder(data)
    return decoder.parse()


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
