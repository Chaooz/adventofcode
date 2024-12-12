#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/0

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *
from advent_libs_matrix import *
from advent_libs_pathfinding_new import *

setupCode("Day 10: Hoof It")

#
# Pathfinding rule:
# Can move max 1 step up 
#
def oneStepUpPathRule( pathfinding, startPosition:Vector2, endPositon:Vector2):
    pathfindingArea = pathfinding.pathfindingMatrix
    endPositon = pathfinding.defaultPathRule(pathfinding,startPosition, endPositon)
    if endPositon != None:
        a = pathfindingArea.GetPoint(startPosition)
        b = pathfindingArea.GetPoint(endPositon)

        # Is something blocking the path?
        if a.isnumeric() == False or b.isnumeric() == False:
            return None
        
        a = int(a)
        b = int(b)
        if b - a != 1:
            return None
    return endPositon

class OneStepUpOnlyPathRule(DefaultPathfindingRuleSet):

    def GotoPosition(self, startPosition:Vector2, endPosition:Vector2):
        pathfindingArea = self.pathfinding.pathfindingMatrix
        endPosition = super().GotoPosition(startPosition, endPosition)
        if endPosition != None:
            a = pathfindingArea.GetPoint(startPosition)
            b = pathfindingArea.GetPoint(endPosition)

            # Is something blocking the path?
            if b.isnumeric() == False:
                return None
            
            a = int(a)
            b = int(b)
            if b - a != 1:
                return None
#            print("GotoPosition: " + str (startPosition) + " => " + str(endPosition) + " (" + str(a) + " => " + str(b) + ")")
        return endPosition


class OneStepUpOnlyMultiPathRule(OneStepUpOnlyPathRule):
    excludeList : list

    def __init__(self):
        self.excludeList = []
        super().__init__()

    def ClearExcludeList(self):
        self.excludeList.clear()

    def ExcludePath(self, pathList:list):
        self.excludeList.append( pathList.copy() )

    def GetTileCost(self, startPosition:Vector2, endPosition:Vector2):
        heuristicCost = math.sqrt((startPosition.x - endPosition.x) ** 2) + ((startPosition.y - endPosition.y) ** 2)
#        for pathList in self.excludeList:
#            if endPosition in pathList:
#                return heuristicCost + 100
        return heuristicCost
    
    def IsPathEqual(self,path1,path2):
        if len(path1) != len(path2):
            return False

        for i in range(0,len(path1)):
#            print("IsPathEqual", path1[i], path2[i])
            if path1[i] != path2[i]:
                return False

        return True

    def GetPathFromNode(self, current:PathNode, startPosition:Vector2, endPosition:Vector2, done) -> list:
        node = current.node
        path = []
        path.append(node.position)

        while True:
            node = done[node]
            if node is None:
                break
            path.append(node.position)

        path.reverse()
        return path

    def DidReachGoal(self, current:PathNode, startPosition:Vector2, endPosition:Vector2, done) -> bool:
        if current.node.position == endPosition:
            if len(self.excludeList) == 0:
#                print("Found path 1")
                return True

            path = self.GetPathFromNode(current, startPosition, endPosition, done)

            # If one path matches, we cannot go here
            for pathList in self.excludeList:
                if self.IsPathEqual(path, pathList):
#                    print("path is excluded", len(self.excludeList), path)
                    return False

#            print("path is NOT excluded", len(self.excludeList))
            return True

        return False

def solvePuzzle1(filename):
    matrix = Matrix.CreateFromFile(filename)

    startPosList = matrix.FindAll("0")
    endPosList = matrix.FindAll("9")

    pathRuleset = OneStepUpOnlyPathRule()
    pathfinding = Pathfinding(pathRuleset)

    sum = 0
    for startPos in startPosList:
        for endPos in endPosList:
            diff = endPos - startPos
            if ( abs(diff.x) + abs(diff.y) > 9 ):
                continue
            pathList = pathfinding.AStarPathTo( matrix, startPos, endPos )
            if pathList != None and len(pathList) > 0:
                sum += 1

    return sum

def solvePuzzle2(filename):
    matrix = Matrix.CreateFromFile(filename)

    startPosList = matrix.FindAll("0")
    endPosList = matrix.FindAll("9")

    pathRuleset = OneStepUpOnlyMultiPathRule()
    pathfinding = Pathfinding(pathRuleset)

    sum = 0
    for startPos in startPosList:
        t = 0
        for endPos in endPosList:

            diff = endPos - startPos
            if ( abs(diff.x) + abs(diff.y) > 9 ):
#                print("Skip this one", startPos, endPos)
                continue

            pathList = pathfinding.AStarAllPathsTo( matrix, startPos, endPos )
            if pathList != None and len(pathList) > 0:
                sum += len(pathList)

    return sum

unittest(solvePuzzle1, 2, "unittest1_1.txt")
unittest(solvePuzzle1, 4, "unittest1_2.txt")
unittest(solvePuzzle1, 36, "unittest1_3.txt")
unittest(solvePuzzle2, 3, "unittest2.txt")
unittest(solvePuzzle2, 81, "unittest1_3.txt")

runCode(10,solvePuzzle1, 607, "input.txt")
runCode(10,solvePuzzle2, 1384, "input.txt")