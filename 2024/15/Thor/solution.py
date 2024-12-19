#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/15

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *
from advent_libs_matrix import *

setupCode("Day 15: Warehouse Woes")

dirmap = { "^": Vector2(0,-1), "v": Vector2(0,1), ">": Vector2(1,0), "<": Vector2(-1,0) }
robotShape = "@"

def readInput(filename):
    lines = loadfile(filename)
    matLines = list()
    moveLines = list()

    for line in lines:
        if line == "":
            continue
        if line[0] == "#":
            matLines.append(line)
        else:
            moveLines.append(line)

    movementList = list()
    for line in moveLines:
        for index in range(0,len(line)):
            dir = line[index]
            movementList.append(dir)
    return matLines, movementList



#
# Find all boxes that will be moved by robot
#
def finWideBoxes(map:Matrix, boxList:list, xPos:int, yPos:int, pushSize:int, boxSize:int, direction:Vector2) -> bool:
    for x in range(0,pushSize):
        pos:Vector2 = Vector2( xPos + (x * direction.x), yPos + direction.y)
        if map.IsOutOfBounds(pos):
            print_debug("Outofbounds:", pos)
            continue

        data = map.GetPoint(pos)
        if data == "#":
            return False
        elif data == "[" and x == 0:
            if not finWideBoxes(map,boxList, xPos + x + direction.x, yPos + direction.y, boxSize, boxSize, direction):
                return False
            if not finWideBoxes(map,boxList, xPos + x + 1 + direction.x, yPos + direction.y, boxSize, boxSize, direction):
                return False
#            boxList.append(pos)
            boxList.append(("[",Vector2(pos.x,pos.y)))
            boxList.append(("]",Vector2(pos.x+1,pos.y)))
        elif data == "]" and x==1:
            pass
        elif data == "[" and x==1:
            pass
        elif data == "]" and x == 0:
            if not finWideBoxes(map,boxList, xPos + x -1 + direction.x, yPos + direction.y, boxSize, boxSize, direction):
                return False
            if not finWideBoxes(map,boxList, xPos + x + direction.x, yPos + direction.y, boxSize, boxSize, direction):
                return False
            boxList.append(("[",Vector2(pos.x-1,pos.y)))
            boxList.append(("]",Vector2(pos.x,pos.y)))
        elif data == ".":
            return True
        else:
            print_assert(False,"unknown type: " + data)
    return True

#
# Find all boxes that will be moved by robot
#
def findSmallBoxes(map:Matrix, boxList:list, currentPos:Vector2, direction:Vector2) -> bool:
    if map.IsOutOfBounds(currentPos):
        print_debug("Outofbounds:", currentPos)
        return False

    nextPos = currentPos + direction

    data = map.GetPoint(currentPos)
    if data == "#":
        return False
    elif data == "[" or data == "]":
        if not findSmallBoxes(map,boxList, nextPos, direction):
            return False
        boxList.append((data,currentPos))
    elif data == "O":
        if not findSmallBoxes(map,boxList, nextPos, direction):
            return False
        boxList.append((data,currentPos))
    elif data == ".":
        return True
    else:
        print_assert(False,"unknown type: " + data)
    return True

# 
# Move all boxes in the list
#
def moveBoxList(map:Matrix, boxList:list, direction:Vector2):
    for data,boxPos in boxList:
        map.Set(boxPos.x, boxPos.y, ".")
    for data,boxPos in boxList:
        map.Set(boxPos.x + direction.x, boxPos.y + direction.y, data)

# 
# Move the robot to a new location
#
def moveRobot(matrix:Matrix, fromPos:Vector2, direction:Vector2) -> bool:
    toPos = fromPos + direction
    if matrix.IsPointInside(toPos):
        matrix.SetPoint(fromPos, ".")
        matrix.SetPoint(toPos, robotShape)
        return True
    return False

#
# Calculate the score/sum
#
def calculateSum(map):
    sum = 0
    for x in range(0,map.sizeX):
        for y in range(0,map.sizeY):
            data = map.Get(x,y)
            if data == "O" or data == "[":
                sum += x + (y * 100)
    return sum

def solvePuzzle1(filename):

    matLines, moveLines = readInput(filename)
    smallMap = Matrix.CreateFromList("mat", matLines,".")
    currentPos = smallMap.FindFirst("@")

    for move in moveLines:
        direction = dirmap.get(move)
        boxList = list()

        # Moving boxes in the x axis is the same as before
        nextPos = currentPos + direction
        if findSmallBoxes(smallMap, boxList, nextPos, direction):
            moveBoxList(smallMap, boxList, direction)
            if moveRobot(smallMap, currentPos, direction):
                currentPos = nextPos

    # if UNITTEST.VISUAL_GRAPH_ENABLED:
    #     colorList = list()
    #     colorList.append(("X", bcolors.LIGHT_GREY))
    #     colorList.append(("O", bcolors.WHITE))
    #     colorList.append(("@", bcolors.YELLOW))
    #     colorList.append(("*", bcolors.YELLOW))
    #     smallMap.PrintWithColor(colorList, bcolors.DARK_GREY, "", " ")

    return calculateSum(smallMap)

#
# Part two
#
def solvePuzzle2(filename):
    matLines, moveLines = readInput(filename)
    smallMap = Matrix.CreateFromList("mat", matLines,".")
    largeMap = Matrix("largemap", smallMap.width * 2, smallMap.height, ".")

    # Create widge map based off the small map
    for x in range(0,smallMap.sizeX):
        for y in range(0,smallMap.sizeY):
            data = smallMap.Get(x,y)
            xx = x * 2
            if data == "O":
                largeMap.Set(xx,y,"[")
                largeMap.Set(xx+1,y,"]")
            elif data == "#":
                largeMap.Set(xx,y,"#")
                largeMap.Set(xx+1,y,"#")
            elif data == "@":
                largeMap.Set(xx,y,"@")


    currentPos = largeMap.FindFirst("@")
   
    for move in moveLines:
        direction = dirmap.get(move)
        boxList = list()
        nextPos = currentPos + direction

        # Moving boxes in the x axis is the same as before
        if direction.y == 0:
            if findSmallBoxes(largeMap, boxList, nextPos, direction):
                moveBoxList(largeMap, boxList, direction)
                if moveRobot(largeMap, currentPos, direction):
                   currentPos = nextPos
        else:
            if finWideBoxes(largeMap, boxList, currentPos.x, currentPos.y, 1, 2, direction):
                moveBoxList(largeMap, boxList, direction)
                if moveRobot(largeMap, currentPos, direction):
                    currentPos = nextPos

    # if UNITTEST.VISUAL_GRAPH_ENABLED:
    #     colorList = list()
    #     colorList.append(("#", bcolors.DARK_GREY))
    #     colorList.append(("[", bcolors.WHITE))
    #     colorList.append(("]", bcolors.WHITE))
    #     colorList.append(("@", bcolors.YELLOW))
    #     colorList.append(("*", bcolors.YELLOW))
    #     largeMap.PrintWithColor(colorList, bcolors.DARK_GREY, "", "")

    return calculateSum(largeMap)

unittest(solvePuzzle1, 2028, "unittest1_1.txt")
unittest(solvePuzzle1, 10092, "unittest1_2.txt")
unittest(solvePuzzle2, 1751, "unittest1_1.txt")
unittest(solvePuzzle2, 9021, "unittest3.txt")

runCode(15,solvePuzzle1, 1436690, "input.txt")
runCode(15,solvePuzzle2, 1482350, "input.txt")