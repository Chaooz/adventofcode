#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/4

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *
from advent_libs_matrix import *

setupCode("Day 6: Guard Gallivant")

exclude = [ "#", "O", "+", "1","2","3","4","5","6","7","8","9","0" ]

#
# Return the Vector2 from the direction
#
def GetVectorFromDirection(direction:int):
    if direction == 0:
        return Vector2(0,-1) # North
    elif direction == 1:
        return Vector2(1,0) # East
    elif direction == 2:
        return Vector2(0,1)
    elif direction == 3:
        return Vector2(-1,0)

def findMapPathToExit(map:Matrix, currentPosition:Vector2):

    # Start direction is UP
    direction = 0

    path = []
    path.append((currentPosition, direction))

    while True:
        newPosition = currentPosition + GetVectorFromDirection(direction)

        # IS the new point outside the map ?
        if map.IsPointInside(newPosition) == False:
            return path

        if map.GetPoint(newPosition) != "#":
            path.append((newPosition,direction))
            currentPosition = newPosition
        else:
            # Rotate character
            direction = (direction + 1) % 4

def canPathToExit(map:Matrix, currentPosition:Vector2):

    # Start direction is UP
    direction = 0

    path = []
    path.append((currentPosition, direction))

    while True:
        newPosition = currentPosition + GetVectorFromDirection(direction)

        # IS the new point outside the map ?
        if map.IsPointInside(newPosition) == False:
            return path

        if map.GetPoint(newPosition) != "#":
            currentPosition = newPosition

            if newPosition not in path:
                path.append((newPosition,direction))

        else:
            # Rotate character
            direction = (direction + 1) % 4


#
# We want to sum all the pages we need to reorder in the book to make it follow the rules
#
def isPathLoop(map:Matrix, currentPosition:Vector2, currentDirection:int, corners) -> bool:
    interations = 0
    while True:

        # Deadlock block
        interations += 1
        if interations > 10000:
            print("Deadlock")
            return False

        newPosition = currentPosition + GetVectorFromDirection(currentDirection)

        # IS the new point outside the map ?
        if map.IsPointInside(newPosition) == False:
            return False

        if map.GetPoint(newPosition) != "#":
            currentPosition = newPosition
        else:
            currentDirection = (currentDirection + 1) % 4

            posAndRot = (currentPosition,currentDirection)
            if posAndRot in corners:
                return True

            corners.append(posAndRot)


#
# Return the number of unique points in the path the guard 
# has to take before leaving the map
#
def solvePuzzle1(filename):
    map = Matrix.CreateFromFile(filename,".")

    # Path from the start positon of the guard to the exit of the map
    startPosition = map.FindFirst("^")
    path = findMapPathToExit(map, startPosition)

    # Make sure the path is unique
    uniquePath = []
    for position, _ in path:
        if position not in uniquePath:
            uniquePath.append(position)
    return len(uniquePath)

#
# 
#
def solvePuzzle2(filename):
    map = Matrix.CreateFromFile(filename,".")

    # Path from the start positon of the guard to the exit of the map
    startPosition = map.FindFirst("^")
    path = findMapPathToExit(map, startPosition)

    startDirection = 0

    obsticleList = []
    startPath = []
    oldDirection = startDirection
    for i in range(1, len(path)):
#        position = path[i-1]
        obsticle = path[i][0]

        # Do not add the guard position
        if map.GetPoint(obsticle) == "^":
            continue

        map.SetPoint(obsticle, "#")
        isLoop = isPathLoop(map, startPosition, startDirection, [])
        if isLoop:
            if obsticle not in obsticleList:
                obsticleList.append(obsticle)
        map.SetPoint(obsticle, ".")

#        if oldDirection != direction:
#            startPath.append((position, direction))
#        oldDirection = direction

    return len(obsticleList)

unittest(solvePuzzle1, 41, "unittest1.txt")
unittest(solvePuzzle2, 6, "unittest1.txt")

runCode(6,solvePuzzle1, 4711, "input.txt")
runCode(6,solvePuzzle2, 1562, "input.txt")