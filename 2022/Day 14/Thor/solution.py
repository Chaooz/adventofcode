#!/usr/local/bin/python3

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_list import *
from advent_libs_matrix import *

CHARACTER_WALL = "#"
CHARACTER_AIR = "."
CHARACTER_AIR_DEBUG = "@"
CHARACTER_SAND = "o"
CHARACTER_SAND_DEBUG = "O"
CHARACTER_START = "+"

RET_TRUE = 1
RET_FALSE = 2
RET_DONE = 3

print("")
print_color("Day 14: Regolith Reservoir", bcolors.OKGREEN)
print("")

def points_on_line(x1, y1, x2, y2):
    xrange = range(x1, x2 + 1) if x2 >= x1 else range(x2, x1 + 1)
    yrange = range(y1, y2 + 1) if y2 >= y1 else range(y2, y1 + 1)
    return [(x, y) for x in xrange for y in yrange]

def createWalls(lines, offset):
    walls = []
    for line in lines:
        wall = Vector2List()
        points = line.split(" -> ")
        for point in points:
            x,y = point.split(",")            
            wall.append( Vector2(int(x)+offset.x, int(y) +offset.y) )
        walls.append(wall)
    return walls

def placeWallsInMatrix(matrix, walls, character):
    maxY = 0
    for wall in walls:
        startPos = wall.Get(0)
        for index in range(1, wall.len()):
            endPos = wall.Get(index)            
            points = points_on_line(startPos.x, startPos.y, endPos.x, endPos.y)
            for (x, y) in points:
                matrix.Set(x,y,character)
                if y>maxY:
                    maxY = y
            startPos = endPos
    return maxY

def AddSand(matrix:Matrix, startPos:Vector2,bottom:int, maxSand:int):
    sandNum = 0
    while True:
        sandNum += 1
        pos = Vector2(startPos.x,startPos.y)

        # Used for unittests
        if sandNum >= maxSand and maxSand > -1:
            return sandNum

        while True:
            if pos.y > bottom:
                return sandNum - 1
            # Drop downwards
            elif matrix.Get( pos.x, pos.y + 1 ) == CHARACTER_AIR:
#                print("Drop down")
                pos.y += 1
            # Fall left
            elif matrix.Get( pos.x - 1, pos.y + 1) == CHARACTER_AIR:
                pos.x -= 1
                pos.y += 1
            # Fall Right
            elif matrix.Get( pos.x + 1, pos.y + 1) == CHARACTER_AIR:
                pos.x += 1
                pos.y += 1
            elif matrix.Get( pos.x, pos.y) == CHARACTER_SAND:
                return sandNum - 1
            else:
                matrix.SetPoint( pos, CHARACTER_SAND )
#                print("Add Sand to : " + pos.ToString())
                break

def solvePuzzle(filename, offset, size, maxSand, puzzleNumber, debug):
    lines = loadfile(filename)
    walls = createWalls(lines, offset)

    startPos = Vector2(500+offset.x,0)

    matrix = Matrix("Sand", size.x, size.y, CHARACTER_AIR)
    matrix.SetPoint(startPos, CHARACTER_START)

    maxY = placeWallsInMatrix(matrix, walls, CHARACTER_WALL)

    # Add floor
    if puzzleNumber == 2:
        for x in range(0,size.x):
            matrix.Set( x, maxY + 2, CHARACTER_WALL )

    num = AddSand(matrix, startPos, maxY + 2, maxSand)

    colorList = list()
    colorList.append((CHARACTER_AIR, bcolors.DARK_GREY))
    colorList.append((CHARACTER_WALL, bcolors.LIGHT_GREY))
    colorList.append((CHARACTER_SAND, bcolors.YELLOW))
    colorList.append((CHARACTER_SAND_DEBUG, bcolors.RED))
    colorList.append((CHARACTER_START, bcolors.YELLOW))

    if debug:
        matrix.PrintWithColor(colorList,bcolors.DARK_GREY, "", "")
    return num

def testPuzzle1(filename, input):
    return solvePuzzle(filename, Vector2(-470,0), Vector2(120,25), input, 1, False )

def testPuzzle2(filename, input):
    return solvePuzzle(filename, Vector2(0,0), Vector2(1000,200), input, 2, False )

def solvePuzzle1(filename):
    return solvePuzzle(filename, Vector2(-470,0), Vector2(120,200), -1, 1, False )

def solvePuzzle2(filename):
    return solvePuzzle(filename, Vector2(0,0), Vector2(1000,200), -1, 2, False )

unittest_input(testPuzzle1, 1, 1, "unittest.txt")
unittest_input(testPuzzle1, 2, 2, "unittest.txt")
unittest_input(testPuzzle1, 3, 3, "unittest.txt")
unittest_input(testPuzzle1, 5, 5, "unittest.txt")
unittest_input(testPuzzle1, 22, 22, "unittest.txt")
unittest_input(testPuzzle1, 24, 24, "unittest.txt")
unittest_input(testPuzzle1, 26, 24, "unittest.txt")

unittest_input(testPuzzle2, 26, 26, "unittest.txt")
unittest_input(testPuzzle2, 100, 93, "unittest.txt")

#unittest(solvePuzzle2, 1, "unittest.txt")
unittest(solvePuzzle1, 763, "puzzleinput.txt")
unittest(solvePuzzle2, 23921, "puzzleinput.txt")