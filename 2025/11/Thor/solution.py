#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/24

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *

def traversePath(path, pathList, indent):

    if path == "out":
        return 1

    valueList = pathList[path]

    total = 0
    for key in valueList:
        total += traversePath(key, pathList, indent + 1)

    return total

def solvePuzzle1(filename):
    lines = loadfile(filename)
    dictData = {}
    for line in lines:
        key, valueString = line.split(":")
        values = [x.strip() for x in valueString.strip().split(" ")]
        dictData[key.strip()] = values
    return traversePath("you", dictData, 0)

def solvePuzzle2(filename):
    return 0

setupCode("Day 11: Reactor")

unittest(solvePuzzle1, 5, "unittest1.txt")
#unittest(solvePuzzle2, -1, "unittest1.txt")

runCode(11,solvePuzzle1, 511, "input.txt")
#runCode(11,solvePuzzle2, -1, "input.txt") 