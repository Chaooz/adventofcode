#!/usr/local/bin/python3
# https://adventofcode.com/2025/day/01

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *

def solvePuzzle1(filename):
    pos = 50
    num_dials = 100
    counts = 0
    lines = loadfile(filename)
    for line in lines:
        dir = line[0]
        length = int(line[1:])
        if dir == 'L':
            pos -= length
        elif dir == 'R':
            pos += length
        pos %= num_dials
        if pos == 0:
            counts += 1
    return counts

def solvePuzzle2(filename):
    pos = 50
    counts = 0
    lines = loadfile(filename)
    for line in lines:
        dir = line[0]
        length = int(line[1:])

        while ( length > 0 ):

            dist = 0
            if dir == 'R':
                dist = 100 - pos
            elif pos == 0:
                dist = 100
            else:
                dist = pos

            if length >= dist:
                pos = 0
                length -= dist
                counts += 1
            else:
                if dir == 'R':
                    pos += length
                else:
                    pos = dist - length
                length = 0

    return counts


setupCode("Day 1: Secret Entrance")

unittest(solvePuzzle1, 3, "unittest1.txt")
unittest(solvePuzzle2, 6, "unittest1.txt")

runCode(1,solvePuzzle1, 1076, "input.txt")
runCode(1,solvePuzzle2, 6379, "input.txt")