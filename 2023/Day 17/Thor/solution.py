#!/usr/local/bin/python3
# https://adventofcode.com/2023/day/2

import sys
import math

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '/Users/thorh/Develop/DarkFactor/adventofcode/Libs')
from advent_libs import *
from advent_libs_vector2 import *
from advent_libs_matrix import *
from advent_libs_pathfinding import *

setupCode("Day 17: Clumsy Crucible")

class CustomPathfindingRule():

    min_straight:int
    max_straight:int

    def __init__(self, min_straight:int, max_straight:int):
        self.min_straight = min_straight
        self.max_straight = max_straight

    # Check if we reached the goal
    def DidReachGoal(self, pathfinding, current:PathNode, endPosition:Vector2):
        return current.node.position == endPosition and current.node.count >= self.min_straight

    # Get the directions we can move
    def GetDirections(self,pathfinding, current:PathNode):
        candidates = list[Vector2]()
        if current.node.count < self.max_straight:
            # can move forward
            candidates.append(current.node.facing)
        if self.min_straight <= current.node.count:
            # can turn
            candidates.append(current.node.facing.rot(1))
            candidates.append(current.node.facing.rot(-1))                
        return candidates

    # Create a new node
    def CreateNewPathNode(self, pathfinding:Pathfinding, current:PathNode, direction:Vector2):
        pos = current.node.position + direction
        if pathfinding.pathfindingMatrix.IsInside(pos.x,pos.y) == False:
            return None
        count = 1 + (direction == current.node.facing) * current.node.count
        newCost = int(pathfinding.pathfindingMatrix.GetPoint(pos))
        newNode = Node(pos, direction, count)
        return PathNode(current.cost + newCost, newNode, current.node)


def internalSolve(filename:str, min_straight:int, max_straight:int):
    matrix  = Matrix.CreateFromFile(filename, ".")
    
    startPos = Vector2(0,0)
    endPos = Vector2(matrix.sizeX-1,matrix.sizeY-1)

    pathfindingRule = CustomPathfindingRule(min_straight, max_straight)
    pathfinding = Pathfinding()
    vecPathList = pathfinding.AStarPathTo(matrix, startPos, endPos, pathfindingRule)

    # Get cost of path
    sum = 0
    for index in range(1, vecPathList.len() ):
        position = vecPathList.Get(index)
        sum += int(matrix.GetPoint(position))

    # Print path 
    showMatrix = matrix.Duplicate("ShowPath")
    for index in range(1, vecPathList.len() ):
        position = vecPathList.Get(index)
        p = showMatrix.GetPoint(position)
        showMatrix.Set(position.x,position.y, "X" + str(p))

    colorList = list()
    colorList.append(("1", bcolors.DARK_GREY))
    colorList.append(("2", bcolors.DARK_GREY))
    colorList.append(("3", bcolors.DARK_GREY))
    colorList.append(("4", bcolors.DARK_GREY))
    colorList.append(("5", bcolors.DARK_GREY))
    colorList.append(("6", bcolors.DARK_GREY))
    colorList.append(("7", bcolors.DARK_GREY))
    colorList.append(("8", bcolors.DARK_GREY))
    colorList.append(("9", bcolors.DARK_GREY))
    colorList.append(("X", bcolors.YELLOW))
#    matrix.PrintWithColor(colorList, bcolors.DARK_GREY, "0000", " ")
#    showMatrix.PrintWithColor(colorList, bcolors.DARK_GREY, "0000", " ")

    return sum

def solvePuzzle1(filename):
    return internalSolve(filename, 0,3)

def solvePuzzle2(filename):
    return internalSolve(filename, 4,10)

#unittest(solvePuzzle1, 102, "2023/Day 17/Thor/unittest1.txt")     
unittest(solvePuzzle1, 102, "unittest1.txt")     
unittest(solvePuzzle2, 110, "unittest1.txt")

runCode(17,solvePuzzle1, 665, "input.txt")     
runCode(17,solvePuzzle2, 809, "input.txt")     
