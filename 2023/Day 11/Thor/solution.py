#!/usr/local/bin/python3
# https://adventofcode.com/2023/day/2

import sys
import math

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_vector2 import *
from advent_libs_matrix import *

setupCode("Day 11: Cosmic Expansion")

class Star:
    id:int
    x:int
    y:int

    def __init__(self, id:int,x:int,y:int):
        self.id = id
        self.x = x
        self.y = y

    def ToString(self):
        return str(self.id) + ":" + str(self.x) +  "x" + str(self.y)

def findRange(sourceStar:Star, destStar:Star):
    diffX = abs(destStar.x - sourceStar.x)
    diffY = abs(destStar.y - sourceStar.y)
    return diffX + diffY

def testRange(line:str):
    x1,y1,x2,y2 = line.split(" ")
    return findRange(Star(1,int(x1),int(y1)), Star(2,int(x2),int(y2)))

def internalSolve(filename:str, expandSize:int):
    sum = 0
    inLines = loadfile(filename)
    stars = list()

    # Expand universe

    width = len(inLines[0])
#    print(width)
    xDot = ""
    for x in range(0,width):
        xDot += "."

    # Find which lines needs to be expanded
    yLines = list()
    for y in range(0,len(inLines)):
        if inLines[y] == xDot:
            yLines.append(y)

    xLines = list()
    for x in range(0,width):
        isBlank = True
        for line in inLines:
            if line[x] != ".":
                isBlank = False
        if isBlank:
            xLines.append(x)

#    print("lines:", yLines, xLines)

    # Find stars
    starId = 0
    yy = 0
    for y in range(0,len(inLines)):
        line = inLines[y]
        yy += 1
        if y in yLines:
            yy += expandSize
        xx = 0
        for x in range(0,len(line)):
            xx += 1
            char = line[x]
            if x in xLines:
                xx += expandSize
            if char == "#":
                starId += 1
                stars.append( Star(starId,xx,yy) )

    #
    # Calculate distance between all groups
    #
    numStars = len(stars)
#    print("stars", numStars)
    for indexMyStar in range(0,numStars-1):
        myStar = stars[indexMyStar]
        for indexOtherStar in range(indexMyStar+1,numStars):
            otherStar = stars[indexOtherStar]
            sum += findRange(myStar, otherStar)

    return sum

def solvePuzzle1(filename:str):
    return internalSolve(filename, 1)

def solvePuzzle2(filename:str):
    return internalSolve(filename, 999999)

unittest(solvePuzzle1, 374, "unittest2.txt")

unittest_input(internalSolve, 9, 1030, "unittest2.txt")
unittest_input(internalSolve, 99, 8410, "unittest2.txt")

runCode(11,solvePuzzle1, 9965032, "input.txt")     
runCode(11, solvePuzzle2, 550358864332, "input.txt")
