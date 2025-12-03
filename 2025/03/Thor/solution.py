#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/24

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *

def getLargestIndexDigit(line, startIndex, endIndex):
    highest = 0
    indexFound = -1
    for pos in range(startIndex, endIndex):
        n = int(line[pos])
        if n > highest:
            highest = n
            indexFound = pos
            if n == 9:
                break
#    print("Processing " + line + " index " + str(startIndex) + ":" + str(endIndex) + " => " + line[startIndex:endIndex] + " => Index:" + str(indexFound) + " Value:" + str(highest))
    return indexFound

def solvePuzzle1(filename):
    lines = loadfile(filename)
    total = 0
    for line in lines:
        startIndex = getLargestIndexDigit(line, 0, len(line)-1)
        endindex = getLargestIndexDigit(line, startIndex+1, len(line))

        highestFirstNumber = line[startIndex]
        highestSecondNumber = line[endindex]

        total += int(highestFirstNumber) * 10 + int(highestSecondNumber)

    return total

def solvePuzzle2(filename):
    lines = loadfile(filename)
    numDigits = 12
    total = 0
    for line in lines:
        startIndex = -1
        totalBattery = 0
        for n in range(0,numDigits):
            startIndex = getLargestIndexDigit(line, startIndex + 1, len(line) - numDigits + n + 1 )
            totalBattery *= 10
            totalBattery += int(line[startIndex])
        total += totalBattery
    return total

setupCode("Day 3: Lobby")

unittest(solvePuzzle1, 357, "unittest1.txt")
unittest(solvePuzzle2, 3121910778619, "unittest1.txt")

runCode(3,solvePuzzle1, 17324, "input.txt")
runCode(3,solvePuzzle2, 171846613143331, "input.txt")