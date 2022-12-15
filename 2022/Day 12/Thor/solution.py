#!/usr/local/bin/python3

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_matrix import *
from advent_libs_list import *
from advent_libs_vector2 import *
from advent_libs_pathfinding import *

def solvePuzzle1(filename):
    return solvePuzzle(filename, 1)

def solvePuzzle2(filename):
    return solvePuzzle(filename, 2)

def solvePuzzle(filename, puzzleNumber):
    matrix  = Matrix.CreateFromFile(filename, ".")

    #
    # Task:
    # Remap the heighmap into numbers
    # Find startpoints and endpoint
    #
    startPostList = Vector2List()
    for y in range(0,matrix.sizeY):
        for x in range(0,matrix.sizeX):
            character = matrix.Get(x,y)
            if character == "S":
                matrix.Set(x,y, 0)
                startPostList.append( Vector2(x,y) )
            elif character == "a" and puzzleNumber == 2:
                startPostList.append( Vector2(x,y) )
                matrix.Set(x,y, 0)
            elif character == "E":
                endPos = Vector2(x,y)
                matrix.Set(x,y, 26) # z value
            else:
                number = int(ord(character) - ord("a"))
                matrix.Set(x,y,number)

    shortestPath = 999
    for startPos in startPostList:
        #print("Path between " + startPos.ToString() + " => " + endPos.ToString())
        pathfinding = Pathfinding()
        pathList = pathfinding.HeuristicAstarPathTo( matrix, startPos, endPos, pathfinding.oneStepPathRule )
        #pathfinding.DebugPrintPath(matrix,shortestPath)
        if len(pathList) > 0 and len(pathList) < shortestPath:
            shortestPath = len(pathList)
    return shortestPath - 1

print("")
print_color("Day 12: Hill Climbing Algorithm", bcolors.OKGREEN)
print("")

unittest(solvePuzzle1, 31, "unittest.txt")
unittest(solvePuzzle2, 29, "unittest.txt")
unittest(solvePuzzle1, 423, "puzzleinput.txt")
unittest(solvePuzzle2, 416, "puzzleinput.txt")
#unittest(solvePuzzle1, 31, "puzzleinput_work.txt")