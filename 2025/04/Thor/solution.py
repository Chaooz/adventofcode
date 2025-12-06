#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/24

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *
from advent_libs_matrix import *

def checkSurroundingRolls(matrix,startX,startY):

    numRolls = 0
    for x in range(0,3):
        for y in range(0,3):
            if x == 1 and y == 1:
                continue

            xx = startX + x - 1
            yy = startY + y - 1

            if matrix.IsInside(xx,yy):
                nval = matrix.Get(xx,yy)
#                print (f"Checking {xx},{yy} = {nval}")
                if nval == "@":
                    numRolls += 1
#    print(numRolls)
    return numRolls

def removeAllRolls(matrix):
    matrix2 = matrix.Duplicate("matrix2")
    total = 0
    for x in range(matrix.width):
        for y in range(matrix.height):
            nval = matrix.Get(x,y)
            if nval != "@":
                continue

            numRolls = checkSurroundingRolls(matrix,x,y)    
            if numRolls < 4:
                total += 1
                matrix2.Set(x,y,".")
    matrix.SetMatrix(matrix2)
    return total

def solvePuzzle1(filename):
    matrix = Matrix.CreateFromFile(filename)
    return removeAllRolls(matrix)

def solvePuzzle2(filename):
    matrix = Matrix.CreateFromFile(filename)
    total = 0
    nTotal = 1
    while nTotal != 0:
        nTotal = removeAllRolls(matrix)
        total += nTotal
    return total

setupCode("Day 4: Printing Department")

unittest(solvePuzzle1, 13, "unittest1.txt")
unittest(solvePuzzle2, 43, "unittest1.txt")

runCode(4,solvePuzzle1, 1356, "input.txt")
runCode(4,solvePuzzle2, 8713, "input.txt")