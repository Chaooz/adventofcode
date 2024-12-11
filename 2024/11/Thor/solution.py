#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/0

import sys
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
def blinkStone(stoneList:list) -> list:

    newList = list()
    for stone in stoneList:
        strStone = str(stone)

        # Change from 0->1
        if stone == 0:
            newList.append(1)
#            print("Stone: change 0 to 1")
        # Split stone in two
        elif len(strStone) % 2 == 0:
            i = int(len(strStone) / 2)
            a = strStone[:i]
            b = strStone[i:len(strStone)]
            newList.append(int(a))
            newList.append(int(b))
#            print("Stone: split " + strStone + " into " + a + " and " + b)
            pass
        # Multiply stone
        else:
            a = stone * 2024
            newList.append(a)
#            print("Stone: Multiply " + str(stone) + " x 2024 = " + str(a))

    return newList

def blinkStoneTest(input:str):
    stoneList = [ int(x) for x in input.split(" ") ]
    retList = blinkStone(stoneList)
    retList = [ str(x) for x in retList ]
    return " ".join(retList)

def solvePuzzle1(filename):
    line = loadfile_as_string(filename)

    stoneList = [ int(x) for x in line.split(" ") ]
    for i in range(0,25):
        stoneList = blinkStone(stoneList)
    retList = [ str(x) for x in stoneList ]
    return len(retList)

def solvePuzzle2(filename):
    line = loadfile_as_string(filename)

    stoneList = [ int(x) for x in line.split(" ") ]
    for i in range(0,75):
        stoneList = blinkStone(stoneList)
        if i % 5 == 0:
            print("running...", i)
    retList = [ str(x) for x in stoneList ]
    return len(retList)

unittest(blinkStoneTest, "1 2024 1 0 9 9 2021976", "0 1 10 99 999")

unittest(solvePuzzle1, 55312, "unittest1.txt")
#unittest(solvePuzzle2, -1, "unittest1.txt")

runCode(11,solvePuzzle1, 183484, "input.txt")
runCode(11,solvePuzzle2, -1, "input.txt")