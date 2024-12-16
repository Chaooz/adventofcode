#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/16

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *
from advent_libs_matrix import *
from advent_libs_pathfinding_new import *

setupCode("Day 16: Reindeer Maze")

class MazeDefaultPathfindingRuleSet(DefaultPathfindingRuleSet):

    # Check if it is valid to go to the next/end position
    def GotoPosition(self, startPosition:Vector2, endPosition:Vector2):
        # Outside of matrix?
        if not self.pathfinding.pathfindingMatrix.IsPointInside(endPosition):
            return None
        
        if self.pathfinding.pathfindingMatrix.GetPoint(endPosition) == "#":
            return None
        
        return endPosition

    # Check if the previous step is valid ( not in wall or outside of matrix)
    # If it is then we increase cost by 1000
    # It is EXPENSIVE to turn :D
    def GetTileCost(self, startPosition:Vector2, endPosition:Vector2, facing:Vector2):
        cost = 1 #math.sqrt((startPosition.x - endPosition.x) ** 2) + ((startPosition.y - endPosition.y) ** 2)

        # If we turn, add 1000 to the cost
        dir = endPosition - startPosition
        if dir != facing:
            cost += 1000

        return cost

    # Return the different directions the pathfinding can go
    # Default is the 4 corners ( North/South and East/West )
    def GetDirections(self, curretNode:Node) -> list:
        direction = curretNode.facing
        leftDirection = direction.rotateLeft()
        rightDirection = direction.rotateRight()
        return [ direction, leftDirection, rightDirection ]
        #return super().GetDirections(curretNode)


def solvePuzzle1(filename):
    matrix = Matrix.CreateFromFile(filename)

    Pathfinding.DEBUG_PATH = True

    pathRuleset = MazeDefaultPathfindingRuleSet()
    pathfinding = Pathfinding(pathRuleset)

    startPos = matrix.FindFirst("S")
    endPos = matrix.FindFirst("E")
    path = pathfinding.AStarPathTo(matrix, startPos, endPos, Vector2(0,-1))

    matrix.SetPoint(startPos, ".")
    matrix.SetPoint(endPos, ".")

    # Overengineering 101
    colorList = list()
    colorList.append(("o", bcolors.YELLOW))
    colorList.append(("1", bcolors.YELLOW))
    colorList.append(("2", bcolors.YELLOW))
    colorList.append(("3", bcolors.RED))
    colorList.append((".", bcolors.DARK_GREY))
    colorList.append(("#", bcolors.DARK_GREY))

    for x in range(0, matrix.width):
        for y in range(0, matrix.height):
            if matrix.GetPoint(Vector2(x,y)) == "#":
                pathfinding.costMatrix.Set(x,y, "#")

#    pathfinding.costMatrix.PrintWithColor(colorList, bcolors.DARK_GREY, "  ", " ")

    if path is None:
        return -1

    direction = Vector2(0,0)
    cost = len(path) - 1 + 1000
    for index in range(1, len(path)):
        pointA = path[index-1]
        pointB = path[index]
        if direction == Vector2(0,0):
            direction = pointB - pointA
            continue

        if direction != pointB - pointA:
#            print("TURN", direction, pointA, pointB)
            direction = pointB - pointA
            cost += 1000

    for p in path:
        d = matrix.GetPoint(p)
        if d == ".":
            d = 1
        else:
            d = d + 1
        matrix.SetPoint(p, d)

    # Overengineering 101
#    matrix.PrintWithColor(colorList, bcolors.DARK_GREY, "", " ")

    return cost

def solvePuzzle2(filename):
    matrix = Matrix.CreateFromFile(filename)

    Pathfinding.DEBUG_PATH = True

    pathRuleset = MazeDefaultPathfindingRuleSet()
    pathfinding = Pathfinding(pathRuleset)

    startPos = matrix.FindFirst("S")
    endPos = matrix.FindFirst("E")
    pathList = pathfinding.AStarAllPathsTo(matrix, startPos, endPos, Vector2(0,-1))

    print("PATHS", len(pathList))

    if pathList is None:
        return -1

    matrix.SetPoint(startPos, ".")
    matrix.SetPoint(endPos, ".")

    # Overengineering 101
    colorList = list()
    colorList.append(("o", bcolors.YELLOW))
    colorList.append(("1", bcolors.YELLOW))
    colorList.append(("2", bcolors.YELLOW))
    colorList.append(("3", bcolors.RED))
    colorList.append((".", bcolors.DARK_GREY))
    colorList.append(("#", bcolors.DARK_GREY))

    for x in range(0, matrix.width):
        for y in range(0, matrix.height):
            if matrix.GetPoint(Vector2(x,y)) == "#":
                pathfinding.costMatrix.Set(x,y, "#")

#    pathfinding.costMatrix.PrintWithColor(colorList, bcolors.DARK_GREY, "  ", " ")

    sum = 0
    for path in pathList:
        sum += len(path)

    # Overengineering 101
#    matrix.PrintWithColor(colorList, bcolors.DARK_GREY, "", " ")

    return sum

unittest(solvePuzzle1, 7036, "unittest1_1.txt")
unittest(solvePuzzle1, 11048, "unittest1_2.txt")
#unittest(solvePuzzle2, -1, "unittest1.txt")

runCode(16,solvePuzzle1, 135536, "input.txt") # Too high
runCode(16,solvePuzzle2, 583, "input.txt")