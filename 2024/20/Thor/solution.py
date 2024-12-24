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

def solveMaze(filename, minCheatSaved):
    matrix = Matrix.CreateFromFile(filename)
    pathfinding = Pathfinding(DefaultPathfindingRuleSet())

    startPos = matrix.FindFirst("S")
    endPos = matrix.FindFirst("E")
    
    nodePathList = pathfinding.AStarPathTo(matrix, startPos, endPos)

    posPaths = dict()
    checkedPath = []

    sum = 0

    # Create a path with position as keys
    for node in nodePathList:
        matrix.SetPoint(node.position, "o")
        posPaths[node.position] = node

    for index in range(0, len(nodePathList)):
        currentNode = nodePathList[index]
        checkedPath.append(currentNode.position)

        # Mark the spot where we are so we can se where we have checked the path
        matrix.SetPoint(currentNode.position, "O")

        # Go all 4 corners and check for other path nodes
        for pos, dir in DefaultPathfindingRuleSet.default_directions:

            # The position next to ours must be a wall
            wallPos = currentNode.position + dir
            if matrix.IsOutOfBounds(wallPos) or (matrix.GetPoint(wallPos) != "#" and matrix.GetPoint(wallPos) != "|"):
                continue

            # The position 2 steps away must an unpathed position in the path
            newPos = currentNode.position + dir * 2
            if matrix.IsOutOfBounds(newPos) or matrix.GetPoint(newPos) != "o":
                continue

            # Mark this positio
            matrix.SetPoint(wallPos, "|")

            node = posPaths.get(newPos)
            newIndex = nodePathList.index(node)
            newPathLength = index + 1 + (len(nodePathList) - newIndex)
            saved = len(nodePathList) - newPathLength - 1

            if saved >= minCheatSaved:
               sum += 1

    matrix.SetPoint(startPos, "S")
    matrix.SetPoint(endPos, "E")

    # Overengineering 101
    colorList = list()
    colorList.append(("#", bcolors.DARK_GREY))
    colorList.append(("o", bcolors.YELLOW))
    colorList.append(("O", bcolors.YELLOW))
    colorList.append(("|", bcolors.DARK_GREY))
    colorList.append(("S", bcolors.WHITE))
    colorList.append(("E", bcolors.WHITE))
#    matrix.PrintWithColor(colorList, bcolors.DARK_GREY, "", "")

    return sum

def solveUnittest1(filename):
    return solveMaze(filename, 1)

def solvePuzzle1(filename):
    return solveMaze(filename, 100)

def solvePuzzle2(filename):
    return 0

unittest(solveUnittest1, 44, "unittest1.txt")
#unittest(solvePuzzle2, -1, "unittest1.txt")
runCode(0,solvePuzzle1, 1307, "input.txt")
#runCode(0,solvePuzzle2, 986545, "input.txt")