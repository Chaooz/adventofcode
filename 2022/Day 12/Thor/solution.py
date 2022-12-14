#!/usr/local/bin/python3

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_matrix import *
from advent_libs_list import *
from advent_libs_vector2 import *
from advent_libs_pathfinding import *

# Rules
# Start pos : S
# End pos :E
# Can only go 1 up or equal

print("")
print_color("Day 12: Hill Climbing Algorithm", bcolors.OKGREEN)
print("")

#
# Finds a character in the matrix and returns position
#
def getPosition(matrix:Matrix,character:str) -> Vector2:
    for y in range(0,matrix.sizeY):
        for x in range(0,matrix.sizeX):
            if matrix.Get(x,y) == character:
                return Vector2(x,y)
    return Vector2(-1,-1)

def solvePuzzle1(filename):
    matrix  = Matrix.CreateFromFile(filename, ".")

    startPos = getPosition(matrix,"S")
    endPos = getPosition(matrix,"E")
    print("Try to path " + startPos.ToString() + " => " + endPos.ToString() )

    valueList = list()
    valueList.append(26)
#    matrix.PrintMultiple(valueList, bcolors.YELLOW, bcolors.DARK_GREY, "000"," ")

    # Remap the heighmap into numbers
    for y in range(0,matrix.sizeY):
        for x in range(0,matrix.sizeX):
            character = matrix.Get(x,y)
            if character == "S":
                matrix.Set(x,y,0)
                pass
            elif character == "E":
                matrix.Set(x,y,0)
                pass
            else:
                number = int(ord(character) - ord("a"))
                matrix.Set(x,y,number)

    matrix.PrintMultiple(valueList, bcolors.YELLOW, bcolors.DARK_GREY, "00","")

    pathfinding = Pathfinding()
    shortestPath = pathfinding.AStarPathTo( matrix, startPos, endPos, 1 )
#    shortestPath = pathfinding.HeuristicAstarPathTo( matrix, startPos, endPos, 1 )

    # Print path in 
    pathMatrix = Matrix("Path", matrix.sizeX, matrix.sizeY, 0)
    for index in range(len(shortestPath)):
        point,cost = shortestPath[index]
        pathMatrix.Set(point.x,point.y, "X")
    pathMatrix.Print(0, bcolors.DARK_GREY,"0", "")

    return len(shortestPath) - 1

#unittest(solvePuzzle1, 31, "unittest.txt")
unittest(solvePuzzle1, 31, "puzzleinput.txt")           # 908 is too high
#unittest(solvePuzzle1, 31, "puzzleinput_work.txt")