#!/usr/local/bin/python3
# https://adventofcode.com/2023/day/2

import sys
import math


# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '/Users/thorh/Develop/DarkFactor/adventofcode/Libs')

from advent_libs import *
from advent_libs_vector2 import *
from advent_libs_matrix import *
from advent_libs_pathfinding import Pathfinding

MAX_COST = 2450

sys.setrecursionlimit(2500)

print("")
print_color("Day 10: Pipe Maze", bcolors.OKGREEN)
print("")

class DIRECTION:
    NONE = 0
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

PIPE_MAP = {
    "S": DIRECTION.NORTH | DIRECTION.SOUTH | DIRECTION.EAST | DIRECTION.WEST,
    "|": DIRECTION.NORTH | DIRECTION.SOUTH,
    "-": DIRECTION.EAST | DIRECTION.WEST,
    "L": DIRECTION.NORTH | DIRECTION.EAST,
    "J": DIRECTION.NORTH | DIRECTION.WEST,
    "7": DIRECTION.SOUTH | DIRECTION.WEST,
    "F": DIRECTION.SOUTH | DIRECTION.EAST,
    ".": DIRECTION.NONE    
}

CONNECTORS = {
    "F" : ["   ", " xx", " x "],
    "7" : ["   ", "xx ", " x "],
    "J" : [" x ", "xx ", "   "],
    "L" : [" x ", " xx", "   "],
    "|" : [" x ", " x ", " x "],
    "-" : ["   ", "xxx", "   "],
    "." : ["   ", " . ", "   "],
    "S" : ["SSS", "SSS", "SSS"],
    "I" : ["   ", " I ", "   "],
}

# Helper function: Check if a bit is set
def HasBit( value:int, bit:int) -> bool:
    return (value & bit) == bit

# Helper function : If a connector matches what is placd on map 
# This meas it has not changed due to flood fill and is inside the loop
def matchConnector(matrix:Matrix, x:int, y:int, connector):
    for i in range(0,3):
        for j in range(0,3):
            c = connector[j][i]
            gridC = matrix.Get((x*3)+i,(y*3)+j)
            if c != gridC:
                return False

    return True

# Helper functio: Place a connector
def placeConnector(matrix:Matrix, x:int, y:int, connector):
    for i in range(0,3):
        for j in range(0,3):
            c = connector[j][i]
            matrix.Set((x*3)+i,(y*3)+j, c)

#
# Pathfindingrule : Follow the pipe based on exit-entry on the pieces
#
def pipePathfindingRule(pathfinding:Pathfinding, startPosition:Vector2, endPositon:Vector2):

    if endPositon != None:
        pathfindingArea = pathfinding.pathfindingMatrix

        # Outside of matrix?

        if not pathfindingArea.IsPointInside(endPositon):
            return None

        a = pathfindingArea.GetPoint(startPosition)
        b = pathfindingArea.GetPoint(endPositon)
        direction = endPositon - startPosition

        # Cannot go through walls
        if b == ".":
            return None

        # Find directions
        pipe_direction_a = PIPE_MAP[a]
        pipe_direction_b = PIPE_MAP[b]

        # Check if the source is going up B is over A
        if HasBit(pipe_direction_a,DIRECTION.NORTH) and HasBit(pipe_direction_b,DIRECTION.SOUTH) and direction == Vector2(0,-1):
            return endPositon

        # Check if the source is going right (east)
        if HasBit(pipe_direction_a, DIRECTION.EAST ) and HasBit(pipe_direction_b, DIRECTION.WEST) and direction == Vector2(1,0):
            return endPositon

        # Check if the source is going down (south)
        if HasBit(pipe_direction_a, DIRECTION.SOUTH) and HasBit(pipe_direction_b, DIRECTION.NORTH) and direction == Vector2(0,1):
            return endPositon
        
        if HasBit(pipe_direction_a, DIRECTION.WEST) and HasBit(pipe_direction_b, DIRECTION.EAST) and direction == Vector2(-1,0) :
            return endPositon

        return None
    return endPositon


#
# Pathfindingrule: Can walk on "." and " "
#                  When we can walk, place an "O" on the area to mark it as OK
#
def closedLoopPathfindingRule(pathfinding:Pathfinding, startPosition:Vector2, endPositon:Vector2):

    if endPositon != None:
        pathfindingArea = pathfinding.pathfindingMatrix

        # Outside of matrix?
        if not pathfindingArea.IsPointInside(endPositon):
            return None

        a = pathfindingArea.GetPoint(startPosition)
        b = pathfindingArea.GetPoint(endPositon)

        # Special case for the start position
        if a == " " and ( a == " " or a == "."):
            pathfindingArea.SetPoint(startPosition, "O")

        # If end position is open, we have an open loop
        if a == "O" and ( b == " " or b == "." ):
            pathfindingArea.SetPoint(endPositon, "O")
            return endPositon

        # Channot pass
        return None

    return endPositon





def internalSolvePuzzle1(filename:str, debug):

    symbolMatrix  = Matrix.CreateFromFile(filename, ".")

    startPoint = symbolMatrix.FindFirst("S")
    endPoint = Vector2(0,0)

    # Path using the pipePathfindingRule
    pathfinding = Pathfinding()
    pathfinding.HeuristicAstarPathTo( symbolMatrix, startPoint, endPoint, pipePathfindingRule, Pathfinding.heatmapOneCostRule )

    # Find the point with the highest cost
    maxCost = 0
    mat = pathfinding.costMatrix
    for x in range(0, mat.sizeX):
        for y in range(0, mat.sizeY):
            cost = mat.Get(x,y)
            if cost > maxCost:
                maxCost = cost

    if debug:
        symbolMatrix.Print()
        pathfinding.costMatrix.Print()

    return maxCost

def solvePuzzle1(filename:str):
    return internalSolvePuzzle1(filename, False)
def debugPuzzle1(filename:str):
    return internalSolvePuzzle1(filename, True)

def internalPuzzle2(filename:str, showDebug:bool):
    symbolMatrix  = Matrix.CreateFromFile(filename, ".")

    # Debug print symbol list
    if showDebug:
        symbolMatrix.Print()

    # Create an expanded Matrix with the pipes
    extendedMatrix = Matrix("Extended", symbolMatrix.sizeX * 3, symbolMatrix.sizeY * 3, ".")
    for y in range (0, symbolMatrix.sizeY):       
        for x in range (0, symbolMatrix.sizeX):
            char = symbolMatrix.Get(x,y)
            connector = CONNECTORS[char]
            placeConnector(extendedMatrix,x,y,connector)

    # Extensive pathfinding from 0,0
    startPoint = Vector2(0,0)
    endPoint = Vector2(-1,-1)
    pathfinding = Pathfinding()
    pathfinding.HeuristicAstarPathTo( extendedMatrix, startPoint, endPoint, closedLoopPathfindingRule )

    # Replace pieces that wasnt changed by flood fill
    iConnector = CONNECTORS["I"]
    for y in range(0,symbolMatrix.sizeY):
        for x in range(0,symbolMatrix.sizeX):
            char = symbolMatrix.Get(x,y)
            connector = CONNECTORS[char]
            if char == "S":
                continue

            if matchConnector(extendedMatrix, x, y, connector ):
                placeConnector(extendedMatrix, x, y, iConnector )


    # Debug stuff
    if showDebug:
        colorList = list()
        colorList.append(("O", bcolors.WHITE))
        colorList.append(("I", bcolors.YELLOW))
        extendedMatrix.PrintWithColor(colorList, bcolors.DARK_GREY , " ", "")

    # Find number of I on the map
    sum = 0
    for y in range (0, extendedMatrix.sizeY):
        for x in range(0, extendedMatrix.sizeX):
            symbol = extendedMatrix.Get(x,y)
            if symbol == "I":
                sum += 1

    return sum

def solvePuzzle2(filename:str):
    return internalPuzzle2(filename, False)

def debugPuzzle2(filename:str):
    return internalPuzzle2(filename, True)

#unittest(debugPuzzle1, 4, "2023/Day 10/Thor/unittest1.txt")

unittest(solvePuzzle1, 4, "unittest1.txt")
unittest(solvePuzzle1, 8, "unittest2.txt")
unittest(solvePuzzle1, 6947, "input.txt")

unittest(solvePuzzle2, 1, "unittest1.txt")
unittest(solvePuzzle2, 1, "unittest2.txt")
unittest(solvePuzzle2, 4, "unittest3.txt")
unittest(solvePuzzle2, 4, "unittest4.txt")
unittest(solvePuzzle2, 8, "unittest5.txt")
unittest(solvePuzzle2, 10, "unittest6.txt")

unittest(solvePuzzle2, 273, "input.txt")
