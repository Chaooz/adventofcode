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
bridgeLength = 1000

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
def moveKnotInPath( pathList:Vector2List ):

    # Get first position
    startPos = pathList.Get(0)

    # List with a visited points
    knotVisitedPositions = Vector2List("knotlist")
    knotVisitedPositions.append(startPos)

    knotPos = startPos
    for index in range(0, pathList.len()):
        firstPos = pathList.Get(index)

        if isNeighbour(firstPos,knotPos):
            continue

        # Find the direction from firstPos and the knotPos
        distance = firstPos - knotPos
        distance = distance.Normalize()

        # Move the knot position    
        knotPos += distance

        # Get the head previous position
#        knotPos = pathList.Get(index-1)

        # Only unique positions
        #if knotVisitedPositions.GetWithPos(knotPos) == None:
        knotVisitedPositions.append(knotPos)
        #elif index > 32:
        #    print("Dupe ["+ str(index) + "] head:" + firstPos.ToString() + " => knot:" + knotPos.ToString() + " distance:" + distance.ToString())


    # Return the visit list for the knot path
    return knotVisitedPositions

def debugAddGraphList(matrix:Matrix, pathList:Vector2List, name:str):
    if matrix != None:
        matrix.InsertFromVector2List(pathList, name)

def debugAddGraphPoint(matrix:Matrix, pathList:Vector2List, name:str):
    if matrix != None:
        p = pathList.Last()
        c = matrix.Get(p.x, p.y)
        if c == ".":
            matrix.Set( p.x, p.y, name)

def solveInternalPuzzle(matrix:Matrix, moveList:Vector2List, startPos:Vector2,numKnots:int):

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

    # set point in matrix debug
    debugAddGraphPoint(matrix, headVisitedPositions, "H")

    # Move a knot through a path
    pathList = headVisitedPositions
    for kIndex in range(0,numKnots):
        knotVisitedPositions = moveKnotInPath(pathList)
        pathList = knotVisitedPositions
        #debugAddGraphPoint(matrix, pathList, str(kIndex+1))

#    debugAddGraphList(matrix, pathList, "#")

    # Make unique list
    tailList = Vector2List("Tail")
    for point in pathList:
        if tailList.GetWithPos( point ) == None:
            tailList.append(point)

    # Return the length of the last path (tail also known as T9)
    return tailList.len()

#
#
#
def testSingleCommand(order, input):
    head, tail, debug = input.split(",")
    head = Vector2( int(head[0]), int(head[2]))
    tail = Vector2( int(tail[0]), int(tail[2]))
    debug = debug == "True"

    moveList = list()
    moveList.append( order.split(" "))

    matrix = None
    if debug:
        matrix = Matrix("testMove", 10, 20, ".")

    ret = solveInternalPuzzle(matrix, moveList, head, 1)
    return ret

def testCommandList( orders, input):
    inputParts = input.split(",")
    # StartPosX StartPosY, Num Knots, Debug 
    # 20 10,9,True"

    # Not optional
    strStartPos = inputParts[0].split(" ")
    startPos = Vector2( int(strStartPos[0]), int(strStartPos[1]))

    # Num Knots (Not optional)
    numKnots = int(inputParts[1])

    # Debug (optional)
    if len(inputParts) > 2:
        debug = inputParts[2] == "True"

    moveList = list()
    for order in orders.split(","):
        moveList.append( order.split(" "))

    matrix = None
    if debug:
        matrix = Matrix("testMove", startPos.x * 2, startPos.y * 2, ".")

    ret = solveInternalPuzzle(matrix, moveList, startPos, int(numKnots))
    if debug:
        matrix.Set( startPos.x, startPos.y, "s")
        matrix.Print(".", bcolors.DARK_GREY, "", "")
    return ret

def solvePuzzle1(filename):
    moveList = listFromFile(filename, " ")
    startPos = Vector2(0,0)
    return solveInternalPuzzle(None,moveList,startPos, 1)

def solvePuzzle2(filename):
    moveList = listFromFile(filename, " ")
    startPos = Vector2(0,0)
#    matrix = Matrix("testMove", 100, 1000, ".")
    return solveInternalPuzzle(None,moveList,startPos,9)

print("")
print_color("Day 9: Rope Bridge", bcolors.OKGREEN)
print("")

debug = "True"
#unittest_input(testSingleCommand, "0 5,0 5," + debug, 4, "R 4")
#unittest_input(testSingleCommand, "4 5,3 5," + debug, 4, "U 4")
#unittest_input(testSingleCommand, "4 0,4 1," + debug, 3, "L 3")
#unittest_input(testSingleCommand, "1 0,2 0," + debug, 1, "D 1")
#unittest_input(testSingleCommand, "1 1,2 0," + debug, 3, "R 4")
#unittest_input(testSingleCommand, "5 1,4 1," + debug, 1, "D 1")
#unittest_input(testSingleCommand, "5 2,4 1," + debug, 4, "L 5")
#unittest_input(testSingleCommand, "0 2,1 2," + debug, 1, "R 2")

#unittest_input(testCommandList, "10 10,1,False", 1, "R 5,U 8")
#unittest_input(testCommandList, "20 10,9,True", 1, "R 5")
#unittest_input(testCommandList, "20 10,9,True", 1, "R 5,U 8")
#unittest_input(testCommandList, "20 10,9,True", 1, "R 5,U 8,L 8")
#unittest_input(testCommandList, "20 10,1,True", 1, "R 5,U 8,L 8,D 3,R 8")
#unittest_input(testCommandList, "20 10,9,True", 1, "R 5,U 8,L 8,D 3,R 9")
#unittest_input(testCommandList, "20 10,9,True", 1, "R 5,U 8,L 8,D 3,R 17")
#unittest_input(testCommandList, "20 10,9,True", 1, "R 5,U 8,L 8,D 3,R 17,D 10")
#unittest_input(testCommandList, "20 10,9,True", 1, "R 5,U 8,L 8,D 3,R 17,D 10,L 25")
#unittest_input(testCommandList, "20 20,9,True", 1, "R 5,U 8,L 8,D 3,R 17,D 10,L 25,U 20")

#unittest(solvePuzzle1, 13, "unittest.txt")
#unittest(solvePuzzle1, 5, "unittest2.txt")
#unittest(solvePuzzle2, 1, "unittest.txt")

#unittest(solvePuzzle1, 3488, "puzzleinput.txt") # 3488 = TooLow
#unittest(solvePuzzle1, 3488, "puzzleinput_work.txt") # 3488 = TooLow

#unittest(solvePuzzle2, 36, "unittest3.txt")
unittest(solvePuzzle2, 2802, "input.txt")
