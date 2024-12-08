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
            path.append((currentPosition,direction))

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
            path.append((newPosition,direction))

        else:
            # Rotate character
            direction = (direction + 1) % 4
            path.append((newPosition,direction))


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
# Bruteforce solution to the problem. We will follow the path of the guard
# and place obstacles on the path. If the guard can still reach the exit
# it is not a loop
#
def solvePuzzle2Brute(filename):
    map = Matrix.CreateFromFile(filename,".")

    # Path from the start positon of the guard to the exit of the map
    startPosition = map.FindFirst("^")
    path = findMapPathToExit(map, startPosition)

    startDirection = 0
    obsticleList = []

    for position, _ in path:
        if map.GetPoint(position) == "^":
            continue

        map.SetPoint(position, "#")
        isLoop = isPathLoop(map, startPosition, startDirection, [])
        if isLoop:
            if position not in obsticleList:
                obsticleList.append(position)
        map.SetPoint(position, ".")

    return len(obsticleList)

#
# Seperate function to solve the puzzle in a smarter way
#
def solvePuzzle2Smart(filename):
    map = Matrix.CreateFromFile(filename,".")

    # Path from the start positon of the guard to the exit of the map
    startPosition = map.FindFirst("^")
    path = findMapPathToExit(map, startPosition)

    # Optimization 2
    # Make sure that the path is unique since we are starting
    # at different startpoints. Remove all points where we would
    # start at the same location later on because that would already
    # be blocked if the guard started on the start position
    uniquePath = []
    for position, direction in path:
        isInUnique = False
        for p2, v2 in uniquePath:
            if p2 == position:
                isInUnique = True
                break
        if isInUnique == False:      
            uniquePath.append((position,direction))

    startDirection = 0
    obsticleList = []
    corners = []

    for position, direction in uniquePath:

        # Do not add the guard position
        if map.GetPoint(position) == "^":
            continue

        map.SetPoint(position, "#")
        isLoop = isPathLoop(map, startPosition, startDirection, corners.copy())
        if isLoop:
            if position not in obsticleList:
                obsticleList.append(position)
        map.SetPoint(position, ".")

        # Optimization 1
        # Whenever we turn, we can start from there instead of starting
        # from the guard start position. This will save us a lot of time
        # to not have to start from the startposition on the path every time
        if startDirection != direction and startPosition != position:
            startPosition = position
            startDirection = direction
            corners.append((position,direction))

    return len(obsticleList)

unittest(solvePuzzle1, 41, "unittest1.txt")
unittest(solvePuzzle2Smart, 6, "unittest1.txt")

runCode(6,solvePuzzle1, 4711, "input.txt")
runCode(6,solvePuzzle2Smart, 1562, "input.txt")
runCode(6,solvePuzzle2Brute, 1562, "input.txt")
