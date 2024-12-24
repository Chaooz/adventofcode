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

    # Find cheat tracks
    # Check all nodes where I turn go 1-2 forward
      # Do I go out of bounds -> Not good path
      # Do I go to a path node existing in the current cheat path -> No good route
      # Do I go to a path node further in the normal path ! Good . Create it as new cheat path
    posPaths = dict()
    checkedPath = []

    sum = 0

    # Create a path with position as keys
    for node in nodePathList:
        posPaths[node.position] = node

    for index in range(0, len(nodePathList)):
        currentNode = nodePathList[index]
        checkedPath.append(currentNode.position)

        # Go all 4 corners and check for other path nodes
        for pos, dir in DefaultPathfindingRuleSet.default_directions:
            newPos = currentNode.position + dir * 2
            if matrix.IsOutOfBounds(newPos):
                continue

            # Make sure we do not try to cheat and connect to an earlier part of the path
            if newPos in checkedPath:
#                print("Already in path:", newPos )
                continue

            # If we are connecting to another point in the full path
            # find that place in the path
            if newPos in posPaths:
#                print("Pos is in normal path:", newPos )

                matrix.SetPoint(newPos, "O")

                node = posPaths.get(newPos)
                newIndex = nodePathList.index(node)
                # We have a shortcut path
                # Splice the path together
                newPath = nodePathList[:index] + nodePathList[newIndex:]

                # Print path 
#                print(len(newPath), len(nodePathList), len(nodePathList) - len(newPath)  )
                sum += 1

    # Overengineering 101
    colorList = list()
    colorList.append(("#", bcolors.DARK_GREY))
    colorList.append(("o", bcolors.YELLOW))
    colorList.append(("O", bcolors.WHITE))
    colorList.append(("S", bcolors.WHITE))
    colorList.append(("E", bcolors.WHITE))
    matrix.PrintWithColor(colorList, bcolors.DARK_GREY, "", " ")

    return sum

def solvePuzzle2(filename):
    return 0

unittest(solvePuzzle1, -1, "unittest1.txt")
#unittest(solvePuzzle2, -1, "unittest1.txt")

#runCode(0,solvePuzzle1, -1, "input.txt")
#runCode(0,solvePuzzle2, -1, "input.txt")