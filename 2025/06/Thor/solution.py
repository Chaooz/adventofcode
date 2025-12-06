#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/24

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *
from advent_libs_matrix import *

def readIntoMatrix(filename):
    lines = loadfile(filename)
    numVals = lines[0].split(" ")
    matrix = Matrix("test", len(lines), len(numVals), " ")
    maxY = 0

    # Insert into matrix
    for x in range(len(lines)):
        val = lines[x].split(" ")
        yy = 0
        for y in range(len(val)):
            if val[y].strip() == "":
                continue
            matrix.Set(x, yy, val[y].strip())
            yy += 1
            if yy > maxY:
                maxY = yy

    return matrix.CropToContent()

def calcuateOperation(op, numberA, numberB):
    result = numberA
    if op == "+":
        result += numberB
    elif op == "-":
        result -= numberB
    elif op == "*":
        if result == 0:
            result = 1
        result *= numberB
    elif op == "/":
        if result == 0:
            result = numberB
        else:
            result /= numberA
    return result

def solvePuzzle1(filename):
    total = 0
    matrix = readIntoMatrix(filename)
#    matrix.Print("", bcolors.DARK_GREY, "     ", " ")
    opStartIndex = matrix.width - 1
    for y in range(0, matrix.height):
        for xx in range(opStartIndex, matrix.width):
            op = matrix.Get(xx,y)
            partResult = 0
            for x in range(0, opStartIndex):
                number = int(matrix.Get(x,y))
                partResult = calcuateOperation(op, partResult, number)
            total += partResult
    return total

def solvePuzzle2(filename):

    matrix = Matrix.CreateFromFile(filename, " ")
#    matrix.Print("", bcolors.DARK_GREY, "     ", " ")
    total = 0

    opIndexList = list()
    for x in range(0, matrix.width):
        op = matrix.Get(x,matrix.height - 1)
        if op in ["+","-","*","/"]:
            opIndexList.append(x)
    opIndexList.append(matrix.width+1)

    for opIndex in range(0, len(opIndexList)-1):
        startIndex = opIndexList[opIndex]
        endIndex = opIndexList[opIndex + 1] - 1
        op = matrix.Get(startIndex, matrix.height - 1)

        # Get numbers
        number = 0
        partResult = 0
        for x in range(startIndex, endIndex):
            number = 0
            for y in range(0, matrix.height - 1):
                val = matrix.Get(x, y)
                if val.strip() == "":
                    continue
                number = number * 10 + int(val)
            partResult = calcuateOperation(op, partResult, number)
        total += partResult

    return total

setupCode("Day 6: Trash Compactor")

unittest(solvePuzzle1, 4277556, "unittest1.txt")
unittest(solvePuzzle2, 3263827, "unittest1.txt")

runCode(6,solvePuzzle1, 4405895212738, "input.txt")
runCode(6,solvePuzzle2, 7450962489289, "input.txt")