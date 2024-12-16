#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/0

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *

setupCode("Day 0: Template")

def solvePuzzle1(filename):
    return 0

def solvePuzzle2(filename):
    return 0

unittest(solvePuzzle1, -1, "unittest1.txt")
unittest(solvePuzzle2, -1, "unittest1.txt")

runCode(0,solvePuzzle1, -1, "input.txt")
runCode(0,solvePuzzle2, -1, "input.txt")