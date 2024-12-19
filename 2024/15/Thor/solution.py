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
boxShapes = [ "O", "[", "]"]
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

def moveSmallBox(map, iteration, point, direction) -> bool:
    global boxShapes

    nextPoint = point + direction
    thisData = map.GetPoint(point)
    nextData = map.GetPoint(nextPoint)

    # Box is size of 1
    if nextData == ".": # Move box
        print_debug("[", iteration, "] Small-Box:Move free:", point.ToString(), "=>",nextPoint.ToString())
        map.SetPoint(nextPoint, thisData)
        map.SetPoint(point, ".")
        return True
    elif nextData in boxShapes:
        if moveSmallBox(map, iteration, nextPoint, direction):
            print_debug("[", iteration, "] Small-Box: Move other:", point.ToString(), "=>",nextPoint.ToString())
            map.SetPoint(nextPoint, thisData)
            map.SetPoint(point, ".")
            return True
        return False
    elif nextData == "#":
        print_debug("[", iteration, "] Small-Box: Hit wall", point.ToString(), "=>",nextPoint.ToString())
        return False
#    else:
#        print_error("ERROR: " + nextData)

def updateCurrent(name, largemap, currentPosA, nextPosA):

    thisDataA = largemap.GetPoint(currentPosA)
    nextDataA = largemap.GetPoint(nextPosA)

    # Find the other part of the box
    currentPosB = currentPosA + Vector2(-1,0)
    nextPosB = nextPosA + Vector2(-1,0)
    thisDataB = "["
    if thisDataA == "[":
        nextPosB = nextPosA + Vector2(1,0)
        currentPosB = currentPosA + Vector2(1,0)
        thisDataB = "]"
    nextDataB = largemap.GetPoint(nextPosB)

    if nextDataA == "." and nextDataB == ".":
        print_debug(name,"updateCurrent: ", currentPosA.ToString(), "=>",nextPosA.ToString(), thisDataA)
        print_debug(name,"updateCurrent: ", currentPosB.ToString(), "=>",nextPosB.ToString(), thisDataB)

        largemap.SetPoint(nextPosA, thisDataA)
        largemap.SetPoint(nextPosB, thisDataB)
        largemap.SetPoint(currentPosA, ".")
        largemap.SetPoint(currentPosB, ".")
    else:
        print_assert(False, "ERROR")


#
# Find all boxes that will be moved by robot
#
def findBoxes(map:Matrix, boxList:list, xPos:int, yPos:int, pushSize:int, boxSize:int, direction:Vector2) -> bool:
    for x in range(0,pushSize):
        pos:Vector2 = Vector2( xPos + (x * direction.x), yPos + direction.y)
        if map.IsOutOfBounds(pos):
            print_debug("Outofbounds:", pos)
            continue

        data = map.GetPoint(pos)
        if data == "#":
            return False
        elif data == "[" and x == 0:
            if not findBoxes(map,boxList, xPos + x + direction.x, yPos + direction.y, boxSize, boxSize, direction):
                return False
            if not findBoxes(map,boxList, xPos + x + 1 + direction.x, yPos + direction.y, boxSize, boxSize, direction):
                return False
#            boxList.append(pos)
            boxList.append(("[",Vector2(pos.x,pos.y)))
            boxList.append(("]",Vector2(pos.x+1,pos.y)))
        elif data == "]" and x==1:
            pass
        elif data == "[" and x==1:
            pass
        elif data == "]" and x == 0:
            if not findBoxes(map,boxList, xPos + x -1 + direction.x, yPos + direction.y, boxSize, boxSize, direction):
                return False
            if not findBoxes(map,boxList, xPos + x + direction.x, yPos + direction.y, boxSize, boxSize, direction):
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
def findSmallBoxes(map:Matrix, boxList:list, currentPos:Vector2, pushSize:int, boxSize:int, direction:Vector2) -> bool:
    if map.IsOutOfBounds(currentPos):
        print_debug("Outofbounds:", currentPos)
        return False

    nextPos = Vector2(currentPos.x + direction.x, currentPos.y)

    data = map.GetPoint(currentPos)
    if data == "#":
        return False
    elif data == "[" or data == "]":
        if not findSmallBoxes(map,boxList, nextPos, boxSize, boxSize, direction):
            return False
        boxList.append((data,nextPos))
    elif data == ".":
        return True
    else:
        print_assert(False,"unknown type: " + data)
    return True

# 
# Move all boxes in the list
#
def moveBoxList(map:Matrix, boxList:list, directionY:int):
    # First set all spaces to "."
    for data,boxPos in boxList:
        map.Set(boxPos.x, boxPos.y, ".")
    
    # First set all spaces to "."
    for data,boxPos in boxList:
        map.Set(boxPos.x, boxPos.y + directionY, data)

def moveRobot(map, moveLines, box) -> bool:
    startPoint = map.FindFirst("@")

    iteration = 0
    for move in moveLines:
        iteration += 1
        direction = dirmap.get(move)
        nextPoint = startPoint + direction
        data = map.GetPoint(nextPoint)

        # Hard block
        if data == "#":
            print_debug("[", iteration, "] Hit wall", startPoint.ToString(), "=>",nextPoint.ToString())
            continue

        # Free space
        elif data == ".":
            print_debug("[", iteration, "] Move free", startPoint.ToString(), "=>",nextPoint.ToString())
            map.SetPoint(startPoint, ".")
            startPoint = nextPoint
            map.SetPoint(startPoint, "@")

        # Box that might be moved
        elif data in box:
            if not moveSmallBox(map, iteration, nextPoint, direction):
                continue
            print_debug("[", iteration, "] Moved box", startPoint.ToString(), "=>",nextPoint.ToString())
            map.SetPoint(startPoint, ".")
            startPoint = nextPoint
            map.SetPoint(startPoint, "@")
        else:
            print_assert(False, "ERROR")

def moveRobotIcon(matrix:Matrix, fromPos:Vector2, direction:Vector2) -> bool:
    toPos = fromPos + direction
    if matrix.IsPointInside(toPos):
        matrix.SetPoint(fromPos, ".")
        matrix.SetPoint(toPos, robotShape)
        return True
    return False

def calculateSum1(map, box):
    sum = 0
    for x in range(0,map.sizeX):
        for y in range(0,map.sizeY):
            if map.Get(x,y) in box:
                sum += x + (y * 100)
    return sum

def calculateSum2(map):
    sum = 0
    for x in range(0,map.sizeX):
        for y in range(0,map.sizeY):
            if map.Get(x,y) == "[":
                sum += x + (y * 100)
    return sum

def solvePuzzle1(filename):
    matLines, moveLines = readInput(filename)
    smallMap = Matrix.CreateFromList("mat", matLines,".")
    box = ["O"]

    moveRobot(smallMap, moveLines, box)

    if UNITTEST.VISUAL_GRAPH_ENABLED:
        colorList = list()
        colorList.append(("X", bcolors.LIGHT_GREY))
        colorList.append(("O", bcolors.WHITE))
        colorList.append(("@", bcolors.YELLOW))
        colorList.append(("*", bcolors.YELLOW))
#        smallMap.PrintWithColor(colorList, bcolors.DARK_GREY, "", " ")

    return calculateSum1(smallMap, box)

def solvePuzzle2(filename):
    matLines, moveLines = readInput(filename)
    smallMap = Matrix.CreateFromList("mat", matLines,".")
    largeMap = Matrix("largemap", smallMap.width * 2, smallMap.height, ".")
    box = ["[","]"]

    colorList = list()
    colorList.append(("#", bcolors.DARK_GREY))
    colorList.append(("[", bcolors.WHITE))
    colorList.append(("]", bcolors.WHITE))
    colorList.append(("@", bcolors.YELLOW))
    colorList.append(("*", bcolors.YELLOW))

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

        # Moving boxes in the x axis is the same as before
        if direction.y == 0:
            nextPos = currentPos + direction
            if findSmallBoxes(largeMap, boxList, nextPos, 1, 1, direction):
                moveBoxList(largeMap, boxList, direction.y)
                if moveRobotIcon(largeMap, currentPos, direction):
                   currentPos = nextPos
        else:
            if findBoxes(largeMap, boxList, currentPos.x, currentPos.y, 1, 2, direction):
                moveBoxList(largeMap, boxList, direction.y)
                if moveRobotIcon(largeMap, currentPos, direction):
                    currentPos = currentPos + direction

#    if UNITTEST.VISUAL_GRAPH_ENABLED:
#        largeMap.PrintWithColor(colorList, bcolors.DARK_GREY, "", "")

    return calculateSum2(largeMap)

unittest(solvePuzzle1, 2028, "unittest1_1.txt")
unittest(solvePuzzle1, 10092, "unittest1_2.txt")
unittest(solvePuzzle2, 1751, "unittest1_1.txt")
unittest(solvePuzzle2, 9021, "unittest3.txt")

runCode(15,solvePuzzle1, 1436690, "input.txt")
runCode(15,solvePuzzle2, 1482350, "input.txt")