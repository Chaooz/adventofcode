#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/24

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *

def traversePath(path, endPath, pathList, cache):

    if path == endPath:
        return 1

    if path == "out":
        return 0

    if path in cache:
        return cache[path]

    valueList = pathList[path]

    total = 0
    for key in valueList:
        total += traversePath(key, endPath,pathList, cache)

    cache[path] = total
    return total

def solvePuzzle1(filename):
    lines = loadfile(filename)
    dictData = {}
    for line in lines:
        key, valueString = line.split(":")
        values = [x.strip() for x in valueString.strip().split(" ")]
        dictData[key.strip()] = values
    return traversePath("you", "out", dictData, {})

def solvePuzzle2(filename):
    lines = loadfile(filename)
    dictData = {}
    for line in lines:
        key, valueString = line.split(":")
        values = [x.strip() for x in valueString.strip().split(" ")]
        dictData[key.strip()] = values

    entries = ["svr", "fft", "dac", "out"]
    total = 1
    for i in range(0,len(entries)-1):
        start = entries[i]
        end = entries[i+1]
        total *= traversePath(start, end, dictData, {})

    return total

setupCode("Day 11: Reactor")

unittest(solvePuzzle1, 5, "unittest1.txt")
unittest(solvePuzzle2, 2, "unittest2.txt")

runCode(11,solvePuzzle1, 511, "input.txt")
runCode(11,solvePuzzle2, 458618114529380, "input.txt")