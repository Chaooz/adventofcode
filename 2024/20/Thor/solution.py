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

class SYMBOLS:
    OPEN_SLOT = "."
    NORMAL_PATH = "o"
    SCANNING_PATH = "O"
    WALL = "#"

def solveMaze(filename, maxCheatTime, minCheatSaved):
    matrix = Matrix.CreateFromFile(filename)
    pathfinding = Pathfinding(DefaultPathfindingRuleSet())

    startPos = matrix.FindFirst("S")
    endPos = matrix.FindFirst("E")
    
    nodePathList = pathfinding.AStarPathTo(matrix, startPos, endPos)

    posPaths = dict()
    checkedPath = []

    sum = 0

    # Create a path with position as keys
    for index in range(0,len(nodePathList)):
        node = nodePathList[index]
        matrix.SetPoint(node.position, SYMBOLS.NORMAL_PATH)
        posPaths[node.position] = index

    for index in range(0, len(nodePathList)):
        currentNode = nodePathList[index]
        checkedPath.append(currentNode.position)

        # Mark the spot where we are so we can se where we have checked the path
        matrix.SetPoint(currentNode.position, SYMBOLS.SCANNING_PATH)

        # Go all 4 corners and check for other path nodes
        for pos, dir in DefaultPathfindingRuleSet.default_directions:

            currentPos = currentNode.position
            data ="#"
            for cheatIndex in range(0,maxCheatTime):

                currentPos = currentPos + dir
                if matrix.IsOutOfBounds(currentPos):
                    break

                # IF we go back to a different part of the path
                data = matrix.GetPoint(currentPos)
                if data == SYMBOLS.NORMAL_PATH or data == SYMBOLS.SCANNING_PATH:
                    break

            if data == "o":
                pathLen = posPaths.get(currentPos)
                newPathLength = index + 1 + (len(nodePathList) - pathLen)
                saved = len(nodePathList) - newPathLength - 1

                if saved >= minCheatSaved:
                    sum += 1
                    #break

    matrix.SetPoint(startPos, "S")
    matrix.SetPoint(endPos, "E")

    # Overengineering 101
    colorList = list()
    colorList.append(("#", bcolors.DARK_GREY))
    colorList.append(("o", bcolors.YELLOW))
    colorList.append(("O", bcolors.YELLOW))
    colorList.append(("0", bcolors.DARK_GREY))
    colorList.append(("S", bcolors.WHITE))
    colorList.append(("E", bcolors.WHITE))
#    matrix.PrintWithColor(colorList, bcolors.DARK_GREY, "", "")

    return sum

def solveUnittest1(filename):
    return solveMaze(filename, 2, 1)

def solvePuzzle1(filename):
    return solveMaze(filename, 2, 100)

def solveUnittest2(filename):
    return solveMaze(filename, 20, 50)

def solvePuzzle2(filename):
    return solveMaze(filename, 20, 100)

unittest(solveUnittest1, 44, "unittest1.txt")
#unittest(solvePuzzle2, -1, "unittest1.txt")
runCode(0,solvePuzzle1, 1307, "input.txt")
#runCode(0,solvePuzzle2, 986545, "input.txt")