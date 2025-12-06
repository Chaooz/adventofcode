#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/24

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *

def isWithinRanges(num, ranges):
    start, end = ranges
    if start <= num <= end:
#        print (f"Number {num} is within range {start}-{end}")
        return True
    return False

def nunRangeWithinRanges(num, ranges):
    start, end = ranges
    if start <= num <= end:
#        print (f"Number {num} is within range {start}-{end}")
        return True
    return False

def solvePuzzle1(filename):
    lines = loadfile(filename)

    total = 0
    ranges = list()
    for line in lines:
        if not line.strip():
            continue

        if "-" in line:
            idRange = line.split('-')
            start = idRange[0].strip()
            end = idRange[1].strip()
            ranges.append((int(start), int(end)))
        else:
            # Process single number
            num = int(line.strip())

            for range in ranges:
                if isWithinRanges(num, range):
                    total += 1
                    break

    return total

def solvePuzzle2(filename):
    lines = loadfile(filename)

    total = 0
    ranges = list()
    for line in lines:
        if not line.strip():
            continue

        if "-" in line:
            idRange = line.split('-')
            start = idRange[0].strip()
            end = idRange[1].strip()
            ranges.append((int(start), int(end)))

    # Merge ranges
    merged_ranges = []
    for start, end in sorted(ranges):
        if not merged_ranges or merged_ranges[-1][1] < start:
            merged_ranges.append((start, end))
        else:
            merged_ranges[-1] = (merged_ranges[-1][0], max(merged_ranges[-1][1], end))

    for r in merged_ranges:
        total += r[1] - r[0] + 1
#        print(f"Range: {r[0]}-{r[1]}")

    return total

setupCode("Day 5: Cafeteria")

unittest(solvePuzzle1, 3, "unittest1.txt")
unittest(solvePuzzle2, 14, "unittest1.txt")

runCode(5,solvePuzzle1, 865, "input.txt")
runCode(5,solvePuzzle2, 352556672963116, "input.txt")