#!/usr/local/bin/python3

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *

print("")
print_color("Day 14: Regolith Reservoir", bcolors.OKGREEN)
print("")

def solvePuzzle1(filename):
    lines = loadfile(filename)
    return 0

def solvePuzzle2(filename):
    lines = loadfile(filename)
    return 0

unittest(solvePuzzle1, 1, "unittest.txt")
unittest(solvePuzzle2, 1, "unittest.txt")
unittest(solvePuzzle1, 1, "puzzleinput.txt")
unittest(solvePuzzle2, 1, "puzzleinput.txt")