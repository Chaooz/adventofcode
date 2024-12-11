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

@dc.dataclass(frozen=True)
class Node:
    position:Vector2
    facing:Vector2
    count:int

class PathNode:

    cost:int
    node:Node
    parent:Node
    neighbours:list

    f:int = 0
    g:int = 0
    h:int = 0

    def __init__(self, cost:int, node:Node, parent:Node):
        self.cost = cost
        self.node = node
        self.parent = parent
        self.neighbours = list()

    def position(self):
        return self.node.position

    def __eq__(self, other):
        if isinstance(other, PathNode):    
            return self.position == other.position
        return False

    def __lt__(self, other):
        return self.cost < other.cost

    def Tuple(self):
        return self.position.Tuple()

    def ToString(self):
        return str(self.position.x) + "x" + str(self.position.y)

# 
# Path between two points in a matrix
#
class DefaultPathfindingRuleSet:
    default_directions:list = [ Vector2(-1,0), Vector2(1,0), Vector2(0,-1), Vector2(0,1) ]

    def SetParent(self,pathfinding):
        self.pathfinding = pathfinding

    def GetDirections(self) -> list:
        return DefaultPathfindingRuleSet.default_directions

    def GetTileCost(self, startPosition:Vector2, endPosition:Vector2):
        heuristicCost = math.sqrt((startPosition.x - endPosition.x) ** 2) + ((startPosition.y - endPosition.y) ** 2)
        return heuristicCost

    def GotoPosition(self, startPosition:Vector2, endPositon:Vector2):
        # Outside of matrix?
        if not self.pathfinding.pathfindingMatrix.IsPointInside(endPositon):
            return None
        return endPositon

    def DidReachGoal(self, currentNode:PathNode, startPosition:Vector2, endPosition:Vector2, camFrom:list) -> bool:
        return currentNode.node.position == endPosition

class Pathfinding:

    MAX_ITERATINS = 1000000
    iterations:int

    pathfindingMatrix : Matrix
    costMatrix : Matrix
    debugPathMatrix : Matrix

    pathRuleset:DefaultPathfindingRuleSet

    def __init__(self, pathRuleset:DefaultPathfindingRuleSet) -> None:
        global iterations
        iterations = 0
        self.pathRuleset = pathRuleset
        pathRuleset.SetParent(self) 
    
    def PathTo(self, sourceMatrix:Matrix, startPosition:Vector2, endPositon:Vector2 ) -> list:

        self.directionList:list = self.pathRuleset.GetDirections()

        self.pathfindingMatrix = sourceMatrix
        # Used for debug
        self.debugPathMatrix = self.pathfindingMatrix.EmptyCopy("debug path", 0)

        # Add the start node with 0 cost
        checkList = Vector2List()
        startNode = PathNode(0, Node(startPosition, Vector2(0,0), 0), None )
        checkList.append(startNode)

        # Add start position to the cost matrix (with 0 cost)
        self.costMatrix = self.pathfindingMatrix.EmptyCopy("CostMatrix", -1)
        self.costMatrix.SetPoint( startPosition, 0 )

        # Global path
        cameFrom = {}
        cameFrom[startPosition.Tuple()] = None

        iterations = 0

        while( checkList.len() > 0 and iterations < Pathfinding.MAX_ITERATINS ):
            iterations += 1
            currentNode:PathNode = checkList.GetWithIndex( 0 )
            checkList.RemoveWithIndex(0)

            # Success
            if self.pathRuleset.DidReachGoal(currentNode, startPosition, endPositon, cameFrom):
#                print_debug("Found path in " + str(iterations) + " iterations")
                break

            # Go through path
            for neighbour in self.directionList:

                # Pathfinding rule
                nextPos = self.pathRuleset.GotoPosition(currentNode.node.position, currentNode.node.position + neighbour)

                # Pathfinding rule is not allowing this move
                if nextPos == None:
                    continue

                # Calculate new cost to move into this tile
                oldCost = self.costMatrix.GetPoint(nextPos)
                newCost = self.pathRuleset.GetTileCost(currentNode.node.position, nextPos)

                if oldCost == -1 or newCost < oldCost:
                    self.costMatrix.SetPoint( nextPos, int(newCost) )

                    # Insert in sorted order
                    i = 0
                    while i < checkList.len():
                        checkPoint:PathNode = checkList.GetWithIndex(i)
                        if checkPoint.cost > newCost:
                            break
                        i = i + 1

                    newNode = PathNode(newCost, Node(nextPos, None, 0), currentNode.node)
                    checkList.InsertWithIndex( i, newNode )

                    if nextPos.Tuple() not in cameFrom:
                        cameFrom[nextPos.Tuple()] = currentNode.node.position

                    # Investigate this node
                    self.debugPathMatrix.SetPoint(nextPos, self.pathfindingMatrix.GetPoint(nextPos))

        # Find the path
        currentPos = endPositon
        result = []
        if cameFrom != None and currentPos.Tuple() in cameFrom:
            while currentPos != startPosition:
                if currentPos in result:
                    print("ERROR: Loop detected")
                    exit(0)

                result.append(currentPos)
                currentPos = cameFrom[currentPos.Tuple()]

            if result:
                result.append(startPosition)
                result.reverse

        if self.debugPathMatrix.IsPointInside(startPosition):
            self.debugPathMatrix.SetPoint(startPosition, "S")
        if self.debugPathMatrix.IsPointInside(endPositon):
            self.debugPathMatrix.SetPoint(endPositon, "E")
#        debugPathMatrix.Print(0, bcolors.DARK_GREY, "00", "")

        return result

  #
    # Noprmal A-Star path
    #    
    def AStarPathTo(self, sourceMatrix:Matrix, startPos:Vector2, endPosition:Vector2 ):

        self.pathfindingMatrix = sourceMatrix

#        self.costMatrix = self.pathfindingMatrix.EmptyCopy("CostMatrix", -1)
#        self.costMatrix.SetPoint( startPos, 0 )

        done = dict[Node, Node]()
        startNode = Node(startPos, Vector2(0, 1), 0)
        frontier: list[PathNode] = [PathNode(0, startNode, None)]
        while frontier:
            current = heap.heappop(frontier)

            if current.node in done:
                continue

            done[current.node] = current.parent

            if self.pathRuleset.DidReachGoal(current, startPos, endPosition, done):
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

            nextDirections = self.pathRuleset.GetDirections()
            for direction in nextDirections:

                pathNode = None
                nextPos = current.node.position + direction

                if self.pathRuleset.GotoPosition(current.node.position, nextPos):
                    tileCost = self.pathRuleset.GetTileCost(current.node.position,nextPos)
                    newNode = Node(nextPos, direction, 1)
                    pathNode = PathNode(current.cost + tileCost, newNode, current.node)
#                    self.costMatrix.SetPoint( nextPos, tileCost )

                if pathNode == None:
                    continue

#                if pathNode == None or pathNode.node in done:
#                    continue

                heap.heappush( frontier, pathNode )

    #
    # Show the path in a matrix
    #
    def DebugPrintPath( self, pathfindingArea:Matrix, shortestPath:Vector2List, char:str = "X" ):
        # Print path in 
        pathMatrix = pathfindingArea.EmptyCopy("ShowPath", ".")
        for index in range(len(shortestPath)):
            point = shortestPath[index]
            pathMatrix.Set(point.x,point.y, char)
        pathMatrix.Print(".", bcolors.DARK_GREY, "0", "")

    def PrintDebugArea( self ):
        self.debugPathMatrix.Print(".", bcolors.DARK_GREY, "000", " ")

    def PrintCostArea( self ):
        self.costMatrix.Print(".", bcolors.DARK_GREY, "000", " ")


