#####################################################################
#
# This is a new pathfinding library that is more flexible
# and can be used in more situations
#
#####################################################################

import math
import dataclasses as dc
import heapq as heap

from advent_libs import *
from advent_libs_matrix import *
from advent_libs_vector2 import *

#@dc.dataclass(frozen=True)
class PathNode:

    position:Vector2
    facing:Vector2
#    parent:PathNode
    cost:int

    f:int = 0
    g:int = 0
    h:int = 0

    def __init__(self, position, facing:Vector2, cost:int, parent ):
        self.cost = cost
        self.position = position
        self.facing = facing
        self.parent = parent

    def position(self):
        return self.position

    def __eq__(self, other):
        if isinstance(other, PathNode):    
            return self.position == other.position
        return False

    def __lt__(self, other):
        return self.cost < other.cost

    def Tuple(self):
        return self.position.Tuple()

    def ToString(self):
        return "" + self.position.ToString() + " > " + self.facing.ToString() + " Cost:" + str(self.cost)

    def getPath(self):
        path = []
        node = self
        while node != None:
            path.append(node)
            node = node.parent
        return path

# 
# Default rule to navigate a pathfind map
#
class DefaultPathfindingRuleSet:
    default_directions:list = [ 
        ( Vector2(-1,0), Vector2(-1,0) ),
        ( Vector2(1,0), Vector2(1,0) ), 
        ( Vector2(0,-1), Vector2(0,-1) ),
        ( Vector2(0,1), Vector2(0,1)) ]

    # Set the pathfinding class as parent to be able to access it if need be
    def SetParent(self,pathfinding):
        self.pathfinding = pathfinding

    # Return the different directions the pathfinding can go
    # Default is the 4 corners ( North/South and East/West )
    def GetDirections(self, pathNode:PathNode) -> list:
        return DefaultPathfindingRuleSet.default_directions

    # Return the different directions the pathfinding can go
    # Default is the 4 corners ( North/South and East/West )
    def GetReversedDirections(self, pathNode:PathNode) -> list:
        return DefaultPathfindingRuleSet.default_directions

    # Return how much it cost to go to this tile
    # Heuristic is the default rule: It is more expensive the further you go from the position
    def GetTileCost(self, startNode:PathNode, endPosition:Vector2, endFacing:Vector2 = None) -> int:
        heuristicCost = math.sqrt((startNode.position.x - endPosition.x) ** 2) + ((startNode.position.y - endPosition.y) ** 2)
        return heuristicCost

    # Check if it is valid to go to the next/end position
    def GotoPosition(self, startPosition:Vector2, endPosition:Vector2):
        # Outside of matrix?
        if not self.pathfinding.pathfindingMatrix.IsPointInside(endPosition):
            return None
        if self.pathfinding.pathfindingMatrix.GetPoint(endPosition) == "#":
            return None
        return endPosition

    # Return True if the goal position have been reached 
    def DidReachGoal(self, currentNode:PathNode, startPosition:Vector2, endPosition:Vector2, camFrom:list) -> bool:
        return currentNode.node.position == endPosition
    
    # Return true if the should return the first (and shortest path)
    def ReturnFirstPath(self):
        return True

#
# Pathfinding rule:
# Can only go UP ( numbers are increasing in the path going f.ex from 0->1->2->3)
#
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


#
# Standard implementation of pathfinding
#
class Pathfinding:

    DEBUG_PATH = False

    pathfindingMatrix : Matrix
    costMatrix : Matrix
    debugPathMatrix : Matrix

    visitedNodes: dict[Vector2, PathNode]

    pathRuleset:DefaultPathfindingRuleSet

    def __init__(self, pathRuleset:DefaultPathfindingRuleSet) -> None:
        self.pathRuleset = pathRuleset
        pathRuleset.SetParent(self) 

    def InternalAStarPathTo(self, sourceMatrix:Matrix, startPos:Vector2, endPosition:Vector2, startFacing:Vector2 ):
        self.pathfindingMatrix = sourceMatrix
    
        # All nodes that have been visited during pathfinding
        self.visitedNodes = dict[tuple, PathNode]()

        startNode = PathNode(startPos, startFacing, 0, None)
        frontier: list[PathNode] = [startNode]
        didFindExit = False
        while frontier:
            currentNode = heap.heappop(frontier)

            nodeKey = (currentNode.position,currentNode.facing)
            if nodeKey in self.visitedNodes:
                continue

            self.visitedNodes[nodeKey] = currentNode

            # We have reached the goal
            if currentNode.position == endPosition:
                didFindExit = True
                break

            # Path in the different directions
            directions = self.pathRuleset.GetDirections(currentNode)
            for moveDirection, facing in directions:
                nextPos = currentNode.position + moveDirection

                if self.pathRuleset.GotoPosition(currentNode.position, nextPos):
                    tileCost = self.pathRuleset.GetTileCost(currentNode, nextPos, facing)
                    pathNode = PathNode(nextPos, facing, currentNode.cost + tileCost, currentNode)

                    nodeKey = (nextPos,facing)
                    if nodeKey in self.visitedNodes:
                        continue

                    heap.heappush( frontier, pathNode )
        if didFindExit:
            return currentNode
        return None

    # 
    # AStarPathTo: Find the shortest path from start to end
    #
    def AStarPathTo(self, sourceMatrix:Matrix, startPos:Vector2, endPosition:Vector2, startFacing:Vector2 = Vector2(0,1) ):
        currentNode:PathNode = self.InternalAStarPathTo(sourceMatrix, startPos, endPosition, startFacing)
        if currentNode != None:
            path = currentNode.getPath()
            path.reverse()
            return path
        return None

    # 
    # AStarPathTo: Find the shortest path from start to end
    #
    def AStarAllPathsTo(self, sourceMatrix:Matrix, startPos:Vector2, endPosition:Vector2, startFacing:Vector2 = Vector2(0,1) ):
        currentNode:PathNode = self.InternalAStarPathTo(sourceMatrix, startPos, endPosition, startFacing)

        pathNode = currentNode
        path = []
        path.append(pathNode)
        checkPathNodes = [ pathNode ]

        reverseVisitList = list()
        start = (startPos, startFacing)
        while checkPathNodes:

            pathNode = heap.heappop(checkPathNodes)
            if pathNode == start:
                continue

            directions = self.pathRuleset.GetReversedDirections(pathNode)
            for cost, moveDirection, facing in directions:
                # Reverse movedirection
                moveDirection = moveDirection * -1
                pos = pathNode.position + moveDirection

                alternativePathNode = self.visitedNodes.get((pos,facing))
                if alternativePathNode == None:
                    continue

                # Add this node to the map
                if pathNode.cost == alternativePathNode.cost + cost:
                    if alternativePathNode not in path: 
                        path.append(alternativePathNode)

                    key = (cost,pos,facing)

                    if key in reverseVisitList:
                        continue
                    reverseVisitList.append(key)

                    heap.heappush( checkPathNodes, alternativePathNode )
        path.reverse()
        return path
    
    #
    # Retun number of unique ways to traverse this path
    #
    def GetPositions(self, path:list):
        if path is None:
            return None
        
        uniqueList = list()
        for step in path:
            if step.position in uniqueList:
                continue
            uniqueList.append((step.position.x, step.position.y))
        return uniqueList
        
    #
    # Show the path in a matrix
    #
    def DebugPrintPath( self, pathfindingArea:Matrix, shortestPath:Vector2List, char:str = "X", space = "" ):
        # Print path in 
        pathMatrix = pathfindingArea.Duplicate("ShowPath")
        for index in range(len(shortestPath)):
            point = shortestPath[index]
            pathMatrix.Set(point.x,point.y, char)

        colorList = list()
        colorList.append((char, bcolors.YELLOW))
        pathMatrix.PrintWithColor(colorList, bcolors.DARK_GREY, "", space)

    #
    # Show the path in a matrix
    #
    def DebugPrintVisitedPath( self, pathfindingArea:Matrix, shortestPath:list, char:str = "o", char2:str = "x", space = "" ):
        # Print path in 
        pathMatrix = pathfindingArea.Duplicate("ShowPath")

        for position,_ in self.visitedNodes:
            pathMatrix.SetPoint(position, char2)

        for path in shortestPath:
            pathMatrix.SetPoint(path, char)

        colorList = list()
        colorList.append((char, bcolors.YELLOW))
        colorList.append((char2, bcolors.LIGHT_GREY))
        pathMatrix.PrintWithColor(colorList, bcolors.DARK_GREY, "", space)

    def PrintDebugArea( self ):
        self.debugPathMatrix.Print(".", bcolors.DARK_GREY, "000", " ")

    def PrintCostArea( self ):
        self.costMatrix.Print(".", bcolors.DARK_GREY, "000", " ")
