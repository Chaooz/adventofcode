#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/12

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *
from advent_libs_matrix import *

setupCode("Day 0: Template")

directions:list = [ Vector2(-1,0), Vector2(1,0), Vector2(0,-1), Vector2(0,1) ]
#directions:list = [ Vector2(-1,0), Vector2(0,-1) ]

def GetFieldOnMap(matrix, data, area, pos):

    area.append(pos)

    for direction in directions:
        xx = pos.x + direction.x
        yy = pos.y + direction.y

        newPos = Vector2(xx,yy)

        # Outside of the matrix?
        if matrix.IsOutOfBounds(newPos):
            continue

        # Different type of field? it does not belong to that field
        if matrix.GetPoint(newPos) != data:
            continue

        
        # If we already have a field, we can add this position to that field
        if newPos not in area:
            area = GetFieldOnMap(matrix, data, area, newPos)
    return area

# Returns the field that contains the position
def GetField(fieldList, data, posA, pos):
    fields = fieldList[data]
    for area in fields:
        if pos in area:
            return area
    return None


def getAreaPerimiter(matrix,area):

    perimiter = list()
    for pos in area:
        x = pos.x
        y = pos.y

        data = matrix.Get(x,y)

        for direction in directions:
            newPos = Vector2(x + direction.x, y + direction.y)

            # Outside of the matrix?
            if matrix.IsOutOfBounds(newPos):
                perimiter.append((pos, direction))
                continue

            neighborData = matrix.GetPoint(newPos)
            if neighborData != data:
                perimiter.append((pos, direction))

    return perimiter

# 
# Find same fence pices on the same line and deactivate them
#
def deactivateFence(perimiter, deactivated, pos, searchDir, dir):
    n = 0
    continueToLoop = True
    while continueToLoop:
        n += 1
        pos2 = Vector2(pos.x + (searchDir.x * n), pos.y + (searchDir.y * n))
        continueToLoop = False
        for j in range(0,len(perimiter)):
            fence = perimiter[j]
            if fence[0] == pos2 and fence[1] == dir:
                deactivated.append( fence )
                continueToLoop = True
                break
    return False


def getStraightLinePerimiter(perimiter):

    # TODO:
    # Loop through all points in the perimiter
    # 1. Does the point below have the same side perimiter?
    # 2. Does the point above have the same side perimiter?
    # if so, remove the point from the perimiter
    deactivated = []

    sum = 0
    for i in range(0,len(perimiter)):
        fence = perimiter[i]
        if fence in deactivated:
            continue

        sum += 1

        pos = fence[0]
        dir = fence[1]

        # Scan up and down
        if dir.y == 0:
            deactivateFence(perimiter, deactivated, pos, Vector2(0,-1), dir)
            deactivateFence(perimiter, deactivated, pos, Vector2(0,1), dir)
        # Scan up and down
        elif dir.x == 0:
            deactivateFence(perimiter, deactivated, pos, Vector2(-1,0), dir)
            deactivateFence(perimiter, deactivated, pos, Vector2(1,0), dir)

    return sum

# Scan matrix and generate unique fields
def createFields(matrix):
    fields = list()
    for x in range(0,matrix.width):
        for y in range(0,matrix.height):
            pos = Vector2(x,y)
            data = matrix.GetPoint(pos)

            if data == ".":
                continue

            area = GetFieldOnMap(matrix, data, list(), pos)
            perimiter = getAreaPerimiter(matrix, area)
            fields.append((data, area, perimiter))

            for pos in area:
                matrix.SetPoint(pos, ".")

    return fields

# Overengineering 101
def drawMap(matrix, fields, deactivated):
    colorList = list()
    colorList.append(("+", bcolors.YELLOW))
    colorList.append(("#", bcolors.WHITE))

    debugMap = Matrix("debug", matrix.sizeX * 3, matrix.sizeY * 3, ".")

    for key, area, perimiter in fields:

        for point in area:
            debugMap.Set(point.x*2 + 1,point.y*2 + 1, key)
        if key == "R":
            for post, dir in perimiter:
                print(post,dir)
                debugMap.Set(post.x*2 + dir.x + 1, post.y*2+dir.y+1, "+")


    for p,d in deactivated:
        debugMap.Set(p.x*2+d.x+1, p.y*2+d.y+1, "#")


    debugMap.PrintWithColor(colorList, bcolors.DARK_GREY,  " ", " ")

def solvePuzzle1(filename):
    matrix = Matrix.CreateFromFile(filename)

    sum = 0
    fields = createFields(matrix)
    for key, area, perimiter in fields:        
        sum += len(area) * len(perimiter)
    return sum

def solvePuzzle2(filename):
    matrix = Matrix.CreateFromFile(filename)

    sum = 0
    fields  = createFields(matrix)

    for key, area, perimiter in fields:
        linePerimiter = getStraightLinePerimiter(perimiter)
        sum += len(area) * linePerimiter
#    drawMap(matrix,fields,deactivated)

    return sum

unittest(solvePuzzle1, 772, "unittest1_1.txt")
unittest(solvePuzzle1, 1930, "unittest1_2.txt")
unittest(solvePuzzle2, 1206, "unittest1_2.txt")

runCode(12,solvePuzzle1, 1396562, "input.txt")
runCode(12,solvePuzzle2, 844132, "input.txt")