#!/usr/bin/env python

import json
import time
import sys
from solver import AmphiGame

for label, filename in [("Part 1:\n", "path_part1.json"), ("Part 2:\n", "path_part2.json")]:

    with open(filename) as f:
        path = json.load(f)

    for key in path:
        sys.stdout.write("\033c")
        sys.stdout.write(label)
        sys.stdout.write("\n")
        output = str(AmphiGame(key))
        for i, letter in enumerate("ABCD"):
            output = output.replace(letter, f"\033[{91+i};1m{letter}\033[0m")
        output = output.replace("#", "█")
        sys.stdout.write(output)
        sys.stdout.write("\n")
        sys.stdout.flush()
        time.sleep(0.3)

    time.sleep(1)
