#!/usr/local/bin/python3

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_matrix import *
from advent_libs_list import *
from advent_libs_vector2 import *
from advent_libs_astar import *

# Rules
# At most 5 up
# Start pos : S
# End pos :E

print("")
print_color("Day 12: Hill Climbing Algorithm", bcolors.OKGREEN)
print("")

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
    pathList = heuristic_astar_path4(startPos, endPos)
    print(pathList)

    return 0

unittest(solvePuzzle1, 13140, "unittest.txt")