#!/usr/local/bin/python3

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_matrix import *
from advent_libs_list import *
from advent_libs_vector2 import *

# Rules
# Tail is trying to follow Head
# Bridge is 5 . wide
# If head is in 90 degree angle away from tail. Tail moves directly up/down/left/right
# if the head is outside row/column the tail moves diagonally
# R 4  -> Move head 4 step to the right
# After each step move tail

bridgeWidth = 6

#
# getDirection
# @str dir - The direction in RLDU letters
# return Vector with direction
#
def getDirection(dir:str):
    if dir == "R": return Vector2(1,0)
    elif dir == "L": return Vector2(-1,0)
    elif dir == "D": return Vector2(0,1)
    elif dir == "U": return Vector2(0,-1)
    return Vector2(0,0)

def isNeighbour(pos1,pos2):
    return abs(pos2.x - pos1.x) < 2 and abs(pos2.y - pos1.y) < 2

#
# Move a knot after a pathList
# @Vector2List pathList: list with all points we want a knot to follow
#
def moveKnotInPath( pathList ):

    # Get first position
    startPos = pathList.Get(0)

    # List with a visited points
    knotVisitedPositions = Vector2List("knotlist")
    knotVisitedPositions.append(startPos)

    knotPos = startPos
    for index in range(1, pathList.len()):
        firstPos = pathList.Get(index)

        if isNeighbour(firstPos,knotPos):
            continue

        # Find the direction from firstPos and the knotPos
        distance = firstPos - knotPos
        position += distance.Scale(1)
        
        # Get the head previous position
        knotPos = pathList.Get(index-1)

        # Only unique positions
        if knotVisitedPositions.GetWithPos(knotPos) == None:
            knotVisitedPositions.append(knotPos)

    # Return the visit list for the knot path
    return knotVisitedPositions

def solveInternalPuzzle(moveList, numKnots):

    startPos = Vector2(0,0)

    # All places the H is visiting
    headVisitedPositions = Vector2List("head")
    headVisitedPositions.append(startPos)

    # Move head
    position = startPos
    for index in range(0, len(moveList)):

        # One move commnd : example R 4
        move = moveList[index]
        direction = getDirection(move[0])
        steps = int(move[1])

        for index in range(0,steps):
            position += direction
            headVisitedPositions.append(position)

    # Move a knot through a path
    pathList = headVisitedPositions
    for kIndex in range(0,numKnots):
        knotVisitedPositions = moveKnotInPath(pathList)
        pathList = knotVisitedPositions

    return pathList.len()

#
#
#
def testMove(order, input):
    head, tail, debug = input.split(",")
    head = Vector2( int(head[0]), int(head[2]))
    tail = Vector2( int(tail[0]), int(tail[2]))
    debug = debug == "True"

    moveList = list()
    moveList.append( order.split(" "))

#    return solveInternalPuzzle(order, moveList, debug, head, tail)
    return 0

def solvePuzzle1(filename):
    moveList = listFromFile(filename, " ")
    return solveInternalPuzzle(moveList,1)

def solvePuzzle2(filename):
    moveList = listFromFile(filename, " ")
    return solveInternalPuzzle(moveList,9)

print("")
print_color("Day 9: Rope Bridge", bcolors.OKGREEN)
print("")

debug = "False"
unittest_input(testMove, "0 5,0 5," + debug, 4, "R 4")
unittest_input(testMove, "4 5,3 5," + debug, 4, "U 4")
unittest_input(testMove, "4 0,4 1," + debug, 3, "L 3")
unittest_input(testMove, "1 0,2 0," + debug, 1, "D 1")
unittest_input(testMove, "1 1,2 0," + debug, 3, "R 4")
unittest_input(testMove, "5 1,4 1," + debug, 1, "D 1")
unittest_input(testMove, "5 2,4 1," + debug, 4, "L 5")
unittest_input(testMove, "0 2,1 2," + debug, 1, "R 2")

unittest(solvePuzzle1, 13, "testinput.txt")
#unittest(solvePuzzle2, 1, "unittest.txt")
#unittest(solvePuzzle1, 6269, "input.txt") # 3488 = TooLow
unittest(solvePuzzle2, 1, "input.txt")
