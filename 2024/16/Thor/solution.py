#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/16

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *
from advent_libs_matrix import *
from advent_libs_pathfinding_astar import *

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
    def GetTileCost(self, startNode:PathNode, endPosition:Vector2, endFacing:Vector2 = None):
        cost = 1 #math.sqrt((startPosition.x - endPosition.x) ** 2) + ((startPosition.y - endPosition.y) ** 2)

        # check if we only turn
        if endPosition == startNode.position and startNode.facing != endFacing:
            return 1000

        # If we turn, add 1000 to the cost
        dir = endPosition - startNode.position
        if dir != startNode.facing:
            cost = 1000

        return cost

    # Return the different directions the pathfinding can go
    # Default is the 4 corners ( North/South and East/West )
    def GetDirections(self, pathNode:PathNode) -> list:
        directions = [ 
            (pathNode.facing, pathNode.facing),
            (Vector2(0,0), pathNode.facing.rotateLeft()), 
            (Vector2(0,0), pathNode.facing.rotateRight()) 
            ]
        return directions

    # Return the different directions the pathfinding can go
    # Default is the 4 corners ( North/South and East/West )
    def GetReversedDirections(self, pathNode:PathNode) -> list:
        directions = [ 
            (1, pathNode.facing, pathNode.facing),
            (1000, Vector2(0,0), pathNode.facing.rotateLeft()), 
            (1000, Vector2(0,0), pathNode.facing.rotateRight()) 
            ]
        return directions

def solvePuzzle1(filename):
    matrix = Matrix.CreateFromFile(filename)

    Pathfinding.DEBUG_PATH = True

    pathRuleset = MazeDefaultPathfindingRuleSet()
    pathfinding = Pathfinding(pathRuleset)

    startPos = matrix.FindFirst("S")
    endPos = matrix.FindFirst("E")
    pathNodes = pathfinding.AStarPathTo(matrix, startPos, endPos, Vector2(1,0))

#    pathfinding.DebugPrintPath(matrix, path, "o")

    if path is None:
        return -1

    lastNode:PathNode = pathNodes[len(pathNodes)-1]
    return lastNode.cost

#    pathfinding.DebugPrintPath(matrix, path, "o")
#    pathfinding.DebugPrintVisitedPath(matrix, path, "o", "x", "")

    return cost

def solvePuzzle2(filename):
    matrix = Matrix.CreateFromFile(filename)

    Pathfinding.DEBUG_PATH = True

    pathRuleset = MazeDefaultPathfindingRuleSet()
    pathfinding = Pathfinding(pathRuleset)

    startPos = matrix.FindFirst("S")
    endPos = matrix.FindFirst("E")
    pathNodes = pathfinding.AStarAllPathsTo(matrix, startPos, endPos, Vector2(1,0))

#    pathfinding.DebugPrintPath(matrix, path, "o")
#    pathfinding.DebugPrintVisitedPath(matrix, path, "o", "x", "")

    return len(pathNodes)

unittest(solvePuzzle1, 7036, "unittest1_1.txt")
unittest(solvePuzzle1, 11048, "unittest1_2.txt")
unittest(solvePuzzle2, 45, "unittest1_1.txt")
unittest(solvePuzzle2, 64, "unittest1_2.txt")

runCode(16,solvePuzzle1, 135536, "input.txt") # Too high
runCode(16,solvePuzzle2, 583, "input.txt")