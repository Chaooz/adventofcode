#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/24

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *
from advent_libs_matrix import *

#
# Give points when the path splits
#
def navigateMatrix(matrix, startPos):
    if matrix.IsOutOfBounds(startPos):
        return 0
    
    val = matrix.GetPoint(startPos)
    if val == ".":
        matrix.SetPoint(startPos, "|")
        return navigateMatrix(matrix, startPos + Vector2(0,1))
    elif val == "^":
        d = 1
        d += navigateMatrix(matrix, startPos + Vector2(-1,0))
        d += navigateMatrix(matrix, startPos + Vector2(1,0))
        return d
    return 0

#
# Give points for every unique path
#
def navigateMatrix2(matrix, startPos):
    if matrix.IsOutOfBounds(startPos):
        return 1
    
    val = matrix.GetPoint(startPos)
    if val == ".":
        d = navigateMatrix2(matrix, startPos + Vector2(0,1))

        # Here is the magic to make it go fast
        # Do not revisit already calculated paths
        matrix.SetPoint(startPos, str(d))
        return d
    elif val == "^":
        d = 0
        d += navigateMatrix2(matrix, startPos + Vector2(-1,0))
        d += navigateMatrix2(matrix, startPos + Vector2(1,0))
        return d

    return int(val)

def solvePuzzle1(filename):
    matrix = Matrix.CreateFromFile(filename)
    startPos = matrix.FindFirst("S")
    ret = navigateMatrix(matrix, startPos + Vector2(0,1))
    colorList = list()
    colorList.append(("|", bcolors.YELLOW))
    colorList.append(("^", bcolors.WHITE))
#    matrix.PrintWithColor(colorList, bcolors.DARK_GREY , " ", " ")

    return ret

def solvePuzzle2(filename):
    matrix = Matrix.CreateFromFile(filename)
    startPos = matrix.FindFirst("S")
    ret = navigateMatrix2(matrix, startPos + Vector2(0,1))
    colorList = list()
    colorList.append(("|", bcolors.YELLOW))
    colorList.append(("^", bcolors.WHITE))
#    matrix.PrintWithColor(colorList, bcolors.DARK_GREY , "  ", " ")

    return ret

setupCode("Day 7: Laboratories")

unittest(solvePuzzle1, 21, "unittest1.txt")
unittest(solvePuzzle2, 40, "unittest1.txt")

runCode(7,solvePuzzle1, 1518, "input.txt")
runCode(7,solvePuzzle2, 25489586715621, "input.txt")