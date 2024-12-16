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
    cost:int

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

    def getPath(self):
        path = []
        node = self
        while node != None:
            path.append(node.position)
            node = node.parent
        return path

# 
# Default rule to navigate a pathfind map
#
class DefaultPathfindingRuleSet:
    default_directions:list = [ Vector2(-1,0), Vector2(1,0), Vector2(0,-1), Vector2(0,1) ]

    # Set the pathfinding class as parent to be able to access it if need be
    def SetParent(self,pathfinding):
        self.pathfinding = pathfinding

    # Return the different directions the pathfinding can go
    # Default is the 4 corners ( North/South and East/West )
    def GetDirections(self, curretNode:PathNode = None) -> list:
        return DefaultPathfindingRuleSet.default_directions

    # Return how much it cost to go to this tile
    # Heuristic is the default rule: It is more expensive the further you go from the position
    def GetTileCost(self, startPosition:Vector2, endPosition:Vector2, facing:Vector2 = None) -> int:
        heuristicCost = math.sqrt((startPosition.x - endPosition.x) ** 2) + ((startPosition.y - endPosition.y) ** 2)
        return heuristicCost

    # Check if it is valid to go to the next/end position
    def GotoPosition(self, startPosition:Vector2, endPosition:Vector2):
        # Outside of matrix?
        if not self.pathfinding.pathfindingMatrix.IsPointInside(endPosition):
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
    MAX_ITERATIONS = 1000000

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

        while( checkList.len() > 0 and iterations < Pathfinding.MAX_ITERATIONS ):
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
    def AStarPathTo(self, sourceMatrix:Matrix, startPos:Vector2, endPosition:Vector2, startFacing:Vector2 = Vector2(0,1) ):

        self.pathfindingMatrix = sourceMatrix
    
        if Pathfinding.DEBUG_PATH == True:
            self.costMatrix = self.pathfindingMatrix.EmptyCopy("CostMatrix", -1)
            self.costMatrix.SetPoint( startPos, 0 )

        done = dict[Node, Node]()
        startNode = Node(startPos, startFacing, 0)
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

            nextDirections = self.pathRuleset.GetDirections(current.node)
            for direction in nextDirections:

                pathNode = None
                nextPos = current.node.position + direction

                if self.pathRuleset.GotoPosition(current.node.position, nextPos):
                    tileCost = self.pathRuleset.GetTileCost(current.node.position,nextPos, current.node.facing)

                    newNode = Node(nextPos, direction, tileCost)
                    pathNode = PathNode(current.cost + tileCost, newNode, current.node)

                    if Pathfinding.DEBUG_PATH == True:
                        self.costMatrix.SetPoint( nextPos, tileCost )

                if pathNode == None or pathNode.node in done:
                    continue

                heap.heappush( frontier, pathNode )

        # Exhaused all possibilities
        print("ERROR: No path found")
        return None

    #
    # A-Star : Find all ways to the target
    #    
    def AStarAllPathsTo(self, sourceMatrix:Matrix, startPos:Vector2, endPosition:Vector2, startFacing:Vector2 = Vector2(0,1) ):
        maxIterations:int = Pathfinding.MAX_ITERATIONS

        self.pathfindingMatrix = sourceMatrix

        if Pathfinding.DEBUG_PATH == True:
            colorList = list()
            colorList.append(("X", bcolors.YELLOW))
            self.costMatrix = self.pathfindingMatrix.Duplicate("CostMatrix")
            self.costMatrix.SetPoint( startPos, 0 )

        done = dict[Node, Node]()
        startNode = Node(startPos, startFacing, 0)
        frontier: list[PathNode] = [PathNode(0, startNode, None)]

        allPaths = []
        iterations = 0
        while frontier:
            current = heap.heappop(frontier)

            if current.node in done:
                continue

            # Safety block for deadlock
            iterations = iterations + 1
            if iterations > maxIterations:
                #print_assert(False, "Max iterations reached for pathfinding!")
                print_error( "Max iterations reached for pathfinding!")
                return allPaths

            done[current.node] = current.parent

            if self.pathRuleset.DidReachGoal(current, startPos, endPosition, done):
                node = current.node
                path = []
                path.append(node.position)
                t = 0
                while True:
                    node = done[node]
                    if node is None:
                        break
                    path.append(node.position)
                    t = t + node.cost

                path.reverse()
                allPaths.append(path)
                print("T:" + str(t))

            nextDirections = self.pathRuleset.GetDirections(current.node)
            for direction in nextDirections:

                pathNode = None
                nextPos = current.node.position + direction

                if self.pathRuleset.GotoPosition(current.node.position, nextPos):
                    tileCost = self.pathRuleset.GetTileCost(current.node.position,nextPos,current.node.facing)
                    newNode = Node(nextPos, direction, tileCost)
                    pathNode = PathNode(current.cost + tileCost, newNode, current.node)

                    if Pathfinding.DEBUG_PATH:
                        self.costMatrix.SetPoint( nextPos, tileCost )

                if pathNode == None:
                    continue

                heap.heappush( frontier, pathNode )

        return allPaths

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
