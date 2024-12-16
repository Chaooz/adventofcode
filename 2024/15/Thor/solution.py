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
    else:
        print_error("ERROR")


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


def moveBigBox(map, iteration, level, currentPosA, direction, doMove) -> bool:
    global boxShapes
    global robotShape

    thisDataA = map.GetPoint(currentPosA)
    nextPosA = currentPosA + direction
    nextDataA = map.GetPoint(nextPosA)

    level += 1

    # Find the other part of the box
    currentPosB = currentPosA + Vector2(-1,0)
    nextPosB = nextPosA + Vector2(-1,0)
    thisDataB = "["
    if thisDataA == "[":
        nextPosB = nextPosA + Vector2(1,0)
        currentPosB = currentPosA + Vector2(1,0)
        thisDataB = "]"
    nextDataB = map.GetPoint(nextPosB)

    # Free space above or below the box, can move it freely
    if nextDataA == "." and nextDataB == ".":
        if doMove and thisDataA in boxShapes:
#            print_debug("[", iteration, "][", level, "] Big-Box:Move free A:", currentPosA.ToString(), "=>",nextPosA.ToString(),thisDataA)
#            print_debug("[", iteration, "][", level, "] Big-Box:Move free B:", currentPosB.ToString(), "=>",nextPosB.ToString(),thisDataB)
#            map.SetPoint(nextPosA, thisDataA)
#            map.SetPoint(nextPosB, thisDataB)
#            map.SetPoint(currentPosA, ".")
#            map.SetPoint(currentPosB, ".")
#            map.Print()
            updateCurrent("bottom",map, currentPosA, nextPosA)
        elif doMove and thisDataA == robotShape:
            print_debug("[", iteration, "][", level, "] Big-Box:Move free 2:", currentPosA.ToString(), "=>",nextPosA.ToString(),thisDataA)
            map.SetPoint(nextPosA, robotShape)
            map.SetPoint(currentPosA, ".")
        elif doMove:
            # This is a bug
            print_assert(False,"[" +  str(iteration) + "][" +  str(level) + "] Big-Box:Move free ??:", currentPosA.ToString(), "=>",nextPosA.ToString(),thisDataA)            
        return True

    # Something is blocking
    elif nextDataA == "#" or nextDataB == "#":
        print_debug("[", iteration, "][", level, "] Big-Box: Blocked A", currentPosA.ToString(), "=>",nextPosA.ToString(), nextDataA)
        print_debug("[", iteration, "][", level, "] Big-Box: Blocked B", currentPosB.ToString(), "=>",nextPosB.ToString(), nextDataB)
        return False

    # A box is blocking
    else:

        # Must be able to move block
        nextDataA = map.GetPoint(nextPosA)
        print_debug("[", iteration, "][", level, "] Big-Box: Box A", currentPosA.ToString(), "=>",nextPosA.ToString(), nextDataA)
        if nextDataA == "[" or nextDataA == "]":
            if not moveBigBox(map, iteration, level, nextPosA, direction, doMove):
                return False

        nextDataB = map.GetPoint(nextPosB)
        print_debug("[", iteration, "][", level, "] Big-Box: Box B", currentPosB.ToString(), "=>",nextPosB.ToString(), nextDataB)
        if nextDataB == "[" or nextDataB == "]":
            if not moveBigBox(map, iteration, level, nextPosB, direction, doMove):
                return False

        if doMove:            
            updateCurrent("box",map, currentPosA, nextPosA)

#            map.Print()

        return True

def moveBox(map, iteration, point, direction, box) -> bool:
    if len(box) == 1:
        return moveSmallBox(map, iteration, point, direction)
#    else:
#        if moveBigBox(map, iteration, point, direction, False):
#            return moveBigBox(map, iteration, point, direction, True)

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
            if not moveBox(map, iteration, nextPoint, direction, box):
                continue
            print_debug("[", iteration, "] Moved box", startPoint.ToString(), "=>",nextPoint.ToString())
            map.SetPoint(startPoint, ".")
            startPoint = nextPoint
            map.SetPoint(startPoint, "@")
        else:
            print_assert(False, "ERROR")

def calculateSum(map, box):
    sum = 0
    for x in range(0,map.sizeX):
        for y in range(0,map.sizeY):
            if map.Get(x,y) in box:
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

    return calculateSum(smallMap, box)

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


    UNITTEST.DEBUG_ENABLED = True

    currentPos = largeMap.FindFirst("@")
    iteration = 0
    for move in moveLines:
        iteration += 1
        direction = dirmap.get(move)

#        if UNITTEST.VISUAL_GRAPH_ENABLED:
#            largeMap.PrintWithColor(colorList, bcolors.DARK_GREY, "", " ")

        if direction.y == 0:
            moveSmallBox(largeMap, iteration, currentPos, direction)
            currentPos = currentPos + direction
        elif moveBigBox(largeMap, iteration, 0, currentPos, direction, False):
            moveBigBox(largeMap, iteration, 0, currentPos, direction, True)
            currentPos = currentPos + direction

#        if iteration > 5:
#            break

    if UNITTEST.VISUAL_GRAPH_ENABLED:
        largeMap.PrintWithColor(colorList, bcolors.DARK_GREY, "", " ")

#    moveRobot(largeMap, moveLines, box)

    UNITTEST.DEBUG_ENABLED = False


    return calculateSum(largeMap, box)

unittest(solvePuzzle1, 2028, "unittest1_1.txt")
unittest(solvePuzzle1, 10092, "unittest1_2.txt")
unittest(solvePuzzle2, -1, "unittest2_1.txt")
#unittest(solvePuzzle2, 9021, "unittest1_2.txt")

runCode(15,solvePuzzle1, 1436690, "input.txt")
runCode(15,solvePuzzle2, 1482350, "input.txt")