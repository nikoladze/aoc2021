#!/usr/bin/env python

import time
import sys
from solver import OctopusAutomaton, parse

with open("input.txt") as f:
    data = parse(f.read())

automaton = OctopusAutomaton(data)

for i in range(600):
    sys.stdout.write("\033c")
    sys.stdout.write(str(automaton) + "\n")
    sys.stdout.flush()
    time.sleep(0.1)
    automaton.step()
