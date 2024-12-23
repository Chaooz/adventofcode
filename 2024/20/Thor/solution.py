#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/20

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *
from advent_libs_matrix import *
from advent_libs_pathfinding_astar import *

setupCode("Day 20: Race Condition")

def solvePuzzle1(filename):
    matrix = Matrix.CreateFromFile(filename)
    pathfinding = Pathfinding(DefaultPathfindingRuleSet())

    startPos = matrix.FindFirst("S")
    endPos = matrix.FindFirst("E")
    
    nodePathList = pathfinding.AStarPathTo(matrix, startPos, endPos)
    for path in nodePathList:
        matrix.SetPoint(path.position, "o")

    # Overengineering 101
    colorList = list()
    colorList.append(("#", bcolors.DARK_GREY))
    colorList.append(("o", bcolors.YELLOW))
    colorList.append(("S", bcolors.WHITE))
    colorList.append(("E", bcolors.WHITE))
    matrix.PrintWithColor(colorList, bcolors.DARK_GREY, "", " ")

    return len(nodePathList)

def solvePuzzle2(filename):
    return 0

unittest(solvePuzzle1, -1, "unittest1.txt")
#unittest(solvePuzzle2, -1, "unittest1.txt")

#runCode(0,solvePuzzle1, -1, "input.txt")
#runCode(0,solvePuzzle2, -1, "input.txt")