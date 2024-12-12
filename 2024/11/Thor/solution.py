#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/11

import sys
import math
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *

setupCode("Day 11: Plutonian Pebbles")

# 
# Rules
#
# 1. If the stone is engraved with the number 0, it is replaced 
#    by a stone engraved with the number 1.
# 2. If the stone is engraved with a number that has an even number
#    of digits, it is replaced by two stones. The left half of the 
#    digits are engraved on the new left stone, and the right half 
#    of the digits are engraved on the new right stone. (The new 
#    numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
# 3. If none of the other rules apply, the stone is replaced by a new stone; 
#    the old stone's number multiplied by 2024 is engraved on the new stone.
#

# Use dictionary as lookup table to avoid going trough all calculations
cache = dict()

def blinkStone(stone:int, level:int, maxLevel:int):
    global cache

    # Return 1 if we reached max level
    if level >= maxLevel:
        return 1

    # Return cached value if it exists
    if stone in cache:
        fast_stone = cache[stone]
        if level in fast_stone:
            return cache[stone][level]
    else:
        cache[stone] = dict()

    # Change from 0->1
    if stone == 0:
        cache[stone][level] = blinkStone(1, level+1, maxLevel)

    # Split stone in two it is has equal number of digits
    elif int(math.log10(stone)) % 2 == 1:

        digits = int(math.log10(stone) / 2) + 1
        a = int(stone / (10 ** digits))
        b = stone % (10 ** digits)

        retA = blinkStone(a, level+1,maxLevel)
        retB = blinkStone(b, level+1,maxLevel)
        cache[stone][level] = retA + retB

    # Multiply stone
    else:        
        cache[stone][level] = blinkStone(stone * 2024, level+1,maxLevel)

    return cache[stone][level]


def solveLine(line, maxLevel):
    global cache
    stoneList = [ int(x) for x in line.split(" ") ]
    sum = 0

    cache = dict()
    for stone in stoneList:
        sum += blinkStone(stone, 0, maxLevel)
    return sum  

def solvePuzzle1(filename):
    line = loadfile_as_string(filename)
    return solveLine(line, 25)

def solvePuzzle2(filename):
    line = loadfile_as_string(filename)
    return solveLine(line, 75)

unittest_input(solveLine, 1, 3, "125 17")
unittest_input(solveLine, 25, 55312, "125 17")

unittest(solvePuzzle1, 55312, "unittest1.txt")
unittest(solvePuzzle2, 65601038650482, "unittest1.txt")

runCode(11,solvePuzzle1, 183484, "input.txt")
runCode(11,solvePuzzle2, 218817038947400, "input.txt")