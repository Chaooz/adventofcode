#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/2

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')
#sys.path.insert(1, '/Users/thorh/Develop/DarkFactor/adventofcode/Libs')

from advent_libs import *

setupCode("Day 2: Red-Nosed Reports")

def diffLine(siffer):
    # Convert to int array
    s = []
    for i in range(0,len(siffer)):
        s.append(int(siffer[i]))
    siffer = s

    if siffer == sorted(siffer) or siffer == sorted(siffer, reverse=True):        
        for i in range(1,len(siffer)):
            d = abs(int(siffer[i]) - int(siffer[i-1]))
            if d < 1 or d > 3:
                return False
        return True        
    return False


def solvePuzzle1(filename):
    sum = 0
    lines = loadfile(filename)
    for line in lines:
        siffer = line.split(" ")
        if diffLine(siffer):
            sum += 1
    return sum

def solvePuzzle2(filename):
    sum = 0
    lines = loadfile(filename)

    for line in lines:
        siffer = line.split(" ")
        if diffLine(siffer):
            sum += 1
        else:
            # 2 is same as 1 except
            # If we take out one number the line is safe
            for i in range(0,len(siffer)):
                siffer2 = siffer[:i] + siffer[i+1:]
                if diffLine(siffer2):
                    sum += 1
                    break
    return sum

def testunit(line,b):
    siffer = line.split(" ")
    if diffLine(siffer):
        return 1
    return 0

unittest_input(testunit, False, 1, "11 9 7 4 2")

unittest(solvePuzzle1, 2, "unittest1.txt")     
unittest(solvePuzzle2, 4, "unittest1.txt")

runCode(2,solvePuzzle1, 486, "input.txt")
runCode(2,solvePuzzle2, 540, "input.txt")

