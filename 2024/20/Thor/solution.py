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


def solveMaze(filename, maxCheatTime, minCheatSaved, debug):
    matrix = Matrix.CreateFromFile(filename)
    pathfinding = Pathfinding(DefaultPathfindingRuleSet())

    startPos = matrix.FindFirst("S")
    endPos = matrix.FindFirst("E")
    
    nodePathList = pathfinding.AStarPathTo(matrix, startPos, endPos)
    posPaths = dict()
    sum = 0

    # Create a path with position as keys
    for index in range(0,len(nodePathList)):
        node = nodePathList[index]
        # Place an "o" on the path
        matrix.SetPoint(node.position, SYMBOLS.NORMAL_PATH)
        # Create a dictory where we can look up the position and get the pathlength to that position
        posPaths[node.position] = index

    for index in range(0, len(nodePathList)):
        currentNode = nodePathList[index]
        pathStart = posPaths.get(currentNode.position)

        # Mark the spot where we are so we can se where we have checked the path
        matrix.SetPoint(currentNode.position, SYMBOLS.SCANNING_PATH)

        # Go all 4 corners and check for other path nodes
        for posY in range(-maxCheatTime, maxCheatTime + 1):
            # To make sure that the total length is not longer than maxCheatTime
            maxX = maxCheatTime - abs(posY)
            for posX in range(-maxX, maxX+1):
                currentPos = currentNode.position + Vector2(posX, posY)

                pathEnd = posPaths.get(currentPos)
                if pathEnd == None:
                    continue

                picoLen = abs(posX) + abs(posY)
                saved = pathEnd - pathStart - picoLen

                if saved >= minCheatSaved:
                    sum += 1

    # Overengineering 101
    if debug:
        matrix.SetPoint(startPos, "S")
        matrix.SetPoint(endPos, "E")

        colorList = list()
        colorList.append(("#", bcolors.DARK_GREY))
        colorList.append(("o", bcolors.YELLOW))
        colorList.append(("O", bcolors.YELLOW))
        colorList.append(("0", bcolors.DARK_GREY))
        colorList.append(("S", bcolors.WHITE))
        colorList.append(("E", bcolors.WHITE))
        matrix.PrintWithColor(colorList, bcolors.DARK_GREY, "", "")

    return sum

def solveUnittest1(filename):
    return solveMaze(filename, 2, 1, UNITTEST.VISUAL_GRAPH_ENABLED)

def solvePuzzle1(filename):
    return solveMaze(filename, 2, 100, False)

def solveUnittest2(filename):
    return solveMaze(filename, 20, 50, False)

def solvePuzzle2(filename):
    return solveMaze(filename, 20, 100, False)

unittest(solveUnittest1, 44, "unittest1.txt")
unittest(solveUnittest2, 285, "unittest1.txt")
runCode(20,solvePuzzle1, 1307, "input.txt")
runCode(20,solvePuzzle2, 986545, "input.txt")