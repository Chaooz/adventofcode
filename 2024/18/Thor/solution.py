#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/18

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *
from advent_libs_matrix import *
from advent_libs_pathfinding_astar import *

setupCode("Day 18: RAM Run")

def puzzleWithInput(filename, memorySize, startPathAt, xSize, ySize, showGraph):
    lines = loadfile(filename)

    matrix = Matrix("RAM", xSize,ySize, ".")
    pathRule = DefaultPathfindingRuleSet()
    pathfinding = Pathfinding(pathRule)

    startPos = Vector2(0,0)
    endPos = Vector2(xSize-1,ySize-1)

    if memorySize > len(lines):
        memorySize = len(lines)

    path = None
    for i in range(0, memorySize):
        x,y = lines[i].split(",")
        matrix.Set(int(x),int(y),"#")
        pos = (int(x),int(y))

        # Optimization
        # Do not bother to path before we have put the X first ( 12 in example and 1024 in
        # the proper solution ) blockers in the path. We already know that we can path from
        # there. This also works in part 1 since we want to place the X blocks first and then path
        if i >= startPathAt:

            # Optimization
            # Do not bother to repath if we are not blocking an already working path
            if path != None and pos not in path:
                continue

            nodePathList = pathfinding.AStarPathTo(matrix, startPos, endPos)
            path = pathfinding.GetPositions(nodePathList)
            if path == None:
                return (int(x),int(y))

    if not path is None:

        # Overengineering 101
        if showGraph:
            for x,y in path:
                position = Vector2(x,y)
                data = matrix.GetPoint(position)
                if data == ".":   
                    matrix.SetPoint(position, "o")
                elif data == "o":
                    matrix.SetPoint(position, "O")
                else:
                    matrix.SetPoint(position, "@")

            colorList = list()
            colorList.append(("#", bcolors.DARK_GREY))
            colorList.append(("o", bcolors.YELLOW))
            matrix.PrintWithColor(colorList, bcolors.DARK_GREY, "", " ")

        return len(path) - 1
    return -1

def solveUnittest1(filename):    
    return puzzleWithInput(filename,12,11,7,7, UNITTEST.VISUAL_GRAPH_ENABLED)

def solveUnittest2(filename):    
    return puzzleWithInput(filename,1000,12,7,7, UNITTEST.VISUAL_GRAPH_ENABLED)

def solvePuzzle1(filename):
    return puzzleWithInput(filename,1024,1023,71,71, False)

def solvePuzzle2(filename):
    return puzzleWithInput(filename,10000,1023,71,71, False)

unittest(solveUnittest1, 22, "unittest1.txt")
unittest(solveUnittest2, (6,1), "unittest1.txt")

runCode(18,solvePuzzle1, 306, "input.txt")
runCode(18,solvePuzzle2, (38,63), "input.txt")