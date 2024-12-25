#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/19

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *

setupCode("Day 19: Linen Layout")

def checkDesignVariants(towelPatterns, design):
    designLength = len(design)

    designPatterns = [0] * designLength
    for i in range(designLength):
        # The [:i+1] will take all the text from the start to the index i+1
        if design[:i+1] in towelPatterns:
            designPatterns[i] = 1

        for pattern in towelPatterns:            
            patternLen = len(pattern)

            if design[i-patternLen+1:i+1] == pattern:
#                print_debug("  ", i, pattern, designPatterns[i - patternLen])
                designPatterns[i] += designPatterns[i - patternLen]

 #   print_debug(designPatterns)

    # print_debug(design, dp)
    return designPatterns[-1]

# towelPatterns - The different stripe combinations in the towels
# design - How the patterns should be combined to make a full stack of towels
def checkDesign(towelPatterns, design):

    designLength = len(design)
    designPatterns = [False] * len(design)

    # Go through all designs
    for i in range(designLength):
        if design[:i+1] in towelPatterns:
#            print_debug("A [", i, design[:i+1], "] ", towelPatterns)
            designPatterns[i] = True
            continue

        for pattern in towelPatterns:            
            patternLen = len(pattern)
            if design[i-patternLen+1:i+1] == pattern and designPatterns[i - patternLen]:
#                print_debug("B [", i, pattern, "] ", design[-patternLen:], designPatterns[i - patternLen])
                designPatterns[i] = True
                break

    # [-1] means the last element in the list
#    print_debug(design, designPatterns, designPatterns[-1])
    return designPatterns[-1]


def solvePuzzle1(filename):
    lines = loadfile(filename)
    patterns = lines[0].split(", ")


    sum = 0
    for i in range(2,len(lines)):
        towelDesign = lines[i]
        if checkDesign(patterns, towelDesign):
            sum += 1
    return sum

def solvePuzzle2(filename):
    lines = loadfile(filename)
    patterns = lines[0].split(", ")

    sum = 0
    for i in range(2,len(lines)):
        towelDesign = lines[i]
        sum += checkDesignVariants(patterns, towelDesign)
    return sum

UNITTEST.DEBUG_ENABLED = True

unittest(solvePuzzle1, 6, "unittest1.txt")
unittest(solvePuzzle2, 16, "unittest1.txt")

runCode(19,solvePuzzle1, 242, "input.txt")
runCode(19,solvePuzzle2, 595975512785325, "input.txt")