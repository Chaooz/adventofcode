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

def moveBox(map, point, direction) -> bool:
    nextPoint = point + direction
    data = map.GetPoint(nextPoint)

    if data == ".": # Move box
#        print("Box:Move free:", point.ToString(), "=>",nextPoint.ToString())
        map.SetPoint(nextPoint, "O")
        map.SetPoint(point, ".")
        return True
    elif data == "O":
        if moveBox(map, nextPoint, direction):
#            print("Box: Move other:", point.ToString(), "=>",nextPoint.ToString())
            map.SetPoint(nextPoint, "O")
            map.SetPoint(point, ".")
            return True
        return False
    elif data == "#":
#        print("Box: Hit wall", point.ToString(), "=>",nextPoint.ToString())
        return False
    else:
        print("ERROR")

def solvePuzzle1(filename):
    matLines, moveLines = readInput(filename)

    map = Matrix.CreateFromList("mat", matLines,".")
    startPoint = map.FindFirst("@")

    loop = 0
    for move in moveLines:
        loop += 1
        direction = dirmap.get(move)
        nextPoint = startPoint + direction

        if map.GetPoint(nextPoint) == "#":
#            print("[", loop, "] Hit wall: ", move, startPoint.ToString(), "=>",nextPoint.ToString())
            continue

        elif map.GetPoint(nextPoint) == "O":
            if not moveBox(map, nextPoint, direction):
                continue
#            print("[", loop, "] Hit box: ",move, startPoint.ToString(), "=>",nextPoint.ToString())
            map.SetPoint(startPoint, ".")
            startPoint = nextPoint
            map.SetPoint(startPoint, "@")

        else:

#            print("[", loop, "] Move: ",move, startPoint.ToString(), "=>",nextPoint.ToString())
            map.SetPoint(startPoint, ".")
            startPoint = nextPoint
            map.SetPoint(startPoint, "@")


    sum = 0
    for x in range(0,map.sizeX):
        for y in range(0,map.sizeY):
            if map.Get(x,y) == "O":
                sum += x + (y * 100)


    if UNITTEST.VISUAL_GRAPH_ENABLED:
        colorList = list()
        colorList.append(("X", bcolors.LIGHT_GREY))
        colorList.append(("O", bcolors.WHITE))
        colorList.append(("@", bcolors.YELLOW))
        colorList.append(("*", bcolors.YELLOW))
#        map.PrintWithColor(colorList, bcolors.DARK_GREY, "", " ")

    return sum

def solvePuzzle2(filename):
    return 0

unittest(solvePuzzle1, 2028, "unittest1_1.txt")
unittest(solvePuzzle1, 10092, "unittest1_2.txt")
#unittest(solvePuzzle2, -1, "unittest1.txt")

runCode(15,solvePuzzle1, 1436690, "input.txt")
#runCode(15,solvePuzzle2, -1, "input.txt")