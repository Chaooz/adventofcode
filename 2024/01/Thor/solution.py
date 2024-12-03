#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/1

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')
#sys.path.insert(1, '/Users/thorh/Develop/DarkFactor/adventofcode/Libs')

from advent_libs import *

setupCode("Day 1: Historian Hysteria")

def solvePuzzle1(filename):
    sum = 0
    lines = loadfile(filename)

    leftList = []
    rightList = []

    for line in lines:
        pair = line.split("   ")
        leftList.append(pair[0].lstrip().rstrip())
        rightList.append(pair[1].lstrip().rstrip())

    leftList.sort()
    rightList.sort()

    for i in range(len(leftList)):
        l = int(leftList[i])
        r = int(rightList[i])
        if l > r:
            sum += l - r
        else:   
            sum += r - l

    return sum

def solvePuzzle2(filename):
    sum = 0
    lines = loadfile(filename)

    leftList = []
    rightList = []

    for line in lines:
        pair = line.split("   ")
        leftList.append(pair[0].lstrip().rstrip())
        rightList.append(pair[1].lstrip().rstrip())

    for i in range(len(leftList)):
        l = int(leftList[i])

        c = 0
        for j in range(len(rightList)):
            r = int(rightList[j])
            if l == r:
                c += 1
        sum += c * l

    return sum

unittest(solvePuzzle1, 11, "unittest1.txt")     
unittest(solvePuzzle2, 31, "unittest1.txt")

runCode(1,solvePuzzle1, 2285373, "input.txt")     
runCode(1,solvePuzzle2, 21142653, "input.txt")     

