#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/4

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *
from advent_libs_matrix import *

setupCode("Day 4: Ceres Search")

directions = [
    Vector2(1,0),  # Right
    Vector2(0,1),  # Down
    Vector2(1,1),  # Down right
    Vector2(-1,1), # Down left
    Vector2(1,-1), # Up right
    Vector2(-1,-1),# Up left
    Vector2(0,-1), # Up
    Vector2(-1,0)   # Left
]

def findWord(matrix, startPoint:tuple, direction:Vector2, word):
    for i in range(0,len(word)):
        xx = startPoint[0] + i * direction.x
        yy = startPoint[1] + i * direction.y
        if xx < 0 or yy < 0 or xx >= matrix.sizeX or yy >= matrix.sizeY:
            return 0
        if matrix.Get(xx,yy) != word[i]:
            return 0
    return 1

def solvePuzzle1(filename):
    sum = 0
    matrix = Matrix.CreateFromFile(filename,".")

    # Overengineering 101
    colorList = list()
    colorList.append(("X", bcolors.YELLOW))
    colorList.append(("M", bcolors.DARK_GREY))
    colorList.append(("A", bcolors.DARK_GREY))
    colorList.append(("S", bcolors.DARK_GREY))
   #matrix.PrintWithColor(colorList,"", " ")

    # Loop through all points to find X
    xList = []
    for x in range(0,matrix.sizeX):
        for y in range(0,matrix.sizeY):
            if matrix.Get(x,y) == "X":
                xList.append((x,y))

    # For all location of Xes find the word XMAS in a given direction
    for point in xList:
        for direction in directions:
            sum += findWord(matrix, point, direction, "XMAS")

    return sum

#
# Check if the point is within the matrix and return the value
#
def getSafePoint(matrix, startPoint:tuple, direction:Vector2):
    xx = startPoint[0] + direction.x
    yy = startPoint[1] + direction.y
    if xx < 0 or yy < 0 or xx >= matrix.sizeX or yy >= matrix.sizeY:
        return ""
    return matrix.Get(xx,yy)

def solvePuzzle2(filename):
    sum = 0
    matrix = Matrix.CreateFromFile(filename,".")

    # Overengineering 101
    colorList = list()
    colorList.append(("M", bcolors.DARK_GREY))
    colorList.append(("A", bcolors.YELLOW))
    colorList.append(("S", bcolors.DARK_GREY))
    colorList.append((".", bcolors.DARK_GREY))
    # matrix.PrintWithColor(colorList,"", " ")

    # Loop through all points to find X
    xList = []
    for x in range(0,matrix.sizeX):
        for y in range(0,matrix.sizeY):
            if matrix.Get(x,y) == "A":
                xList.append((x,y))

    # For all location of Aes find the crossing S&M
    for point in xList:
        a1 = getSafePoint(matrix, point, Vector2(-1,-1))
        a2 = getSafePoint(matrix, point, Vector2(1,1))
        b1 = getSafePoint(matrix, point, Vector2(1,-1))
        b2 = getSafePoint(matrix, point, Vector2(-1,1))

        a = a1+a2
        b = b1+b2

        if ( a == "MS" or a == "SM" ) and ( b == "MS" or b == "SM" ):
            sum += 1

    return sum

unittest(solvePuzzle1, 4, "unittest1.txt")
unittest(solvePuzzle1, 18, "unittest2.txt")
unittest(solvePuzzle2, 9, "unittest3.txt")

runCode(4,solvePuzzle1, 2524, "input.txt")
runCode(4,solvePuzzle2, 1873, "input.txt")

