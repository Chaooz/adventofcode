
import math
import dataclasses as dc
import heapq as heap

from advent_libs import *
from advent_libs_matrix import *
from advent_libs_vector2 import *

# Used in assignments
# 2023: Day 17

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
# The directions the pathfinding can move
#
class DefaultPathfindingRule:

    # All four directions
    default_directions:list = [ Vector2(-1,0), Vector2(1,0), Vector2(0,-1), Vector2(0,1) ]

    def GetTileCost(self,pathfinding, position:Vector2):
        return 1

    def GetDirections(self,pathfinding) -> list:
        return DefaultPathfindingRule.default_directions

    def DidReachGoal(self,pathfinding, current:PathNode, endPosition:Vector2) -> bool:
        return current.node.position == endPosition

    def CreateNewPathNode(self, pathfinding, current:PathNode, direction:Vector2) -> PathNode:
        nextPos = current.node.position + direction
        if not self.pathfindingMatrix.IsPointInside(nextPos):
            return None

        tileCost = self.GetTileCost(pathfinding, nextPos)
        newNode = Node(nextPos, direction, 1)
        return PathNode(current.cost + tileCost, newNode, current.node)

class HeuristicPathfindingRule(DefaultPathfindingRule):

    def GetTileCost(self, pathfinding, position:Vector2) -> int:
        return pathfinding.pathfindingMatrix.GetPoint(position)


class Pathfinding:

    MAX_ITERATINS = 1000000
    iterations:int

    pathfindingMatrix : Matrix
    costMatrix : Matrix
    debugPathMatrix : Matrix

    def __init__(self) -> None:
        global iterations
        iterations = 0
    
    #
    # Pathfinding rule:
    # Default rule: Can move in all positions inside matrix
    #
    def defaultPathRule(self, pathfinding, startPosition:Vector2, endPositon:Vector2, checkList:dict):
        # Outside of matrix?
        if not self.pathfindingMatrix.IsPointInside(endPositon):
            return None
        return endPositon

    #
    # Pathfinding rule:
    # Can move max 1 step up ( can always move forward or down )
    # Used in 2022-Day12
    #
    def oneStepPathRule(self, pathfinding, startPosition:Vector2, endPositon:Vector2, checkList:dict):
        pathfindingArea = pathfinding.pathfindingMatrix
        endPositon = self.defaultPathRule(startPosition, endPositon,checkList)
        if endPositon != None:
            a = int(pathfindingArea.GetPoint(startPosition))
            b = int(pathfindingArea.GetPoint(endPositon))
            if b > a + 1:
                return None
        return endPositon

    #
    # Return the cost of entering this tile
    #
    def tileNoCostRule(pathfinding, startPosition:Vector2, endPosition:Vector2):
        heuristicCost = math.sqrt((startPosition.x - endPosition.x) ** 2) + ((startPosition.y - endPosition.y) ** 2)
        return heuristicCost

    #
    # Normal heatmap cost rule (cost is 1 for each tile out)
    #
    def heatmapOneCostRule(pathfinding, startPosition:Vector2, endPosition:Vector2):
        baseCost = 0 #Pathfinding.tileNoCostRule(pathfinding,startPosition,endPosition)
        tileCost = 1
        newCost = pathfinding.costMatrix.GetPoint(startPosition) + tileCost + baseCost
        return newCost

    #
    # Normal heatmap cost rule (cost is the value of the tile)
    #
    def heatmapCostRule(pathfinding, startPosition:Vector2, endPosition:Vector2):
        baseCost = Pathfinding.tileNoCostRule(pathfinding,startPosition,endPosition)
        tileCost = pathfinding.pathfindingMatrix.GetPoint(endPosition)
        newCost = pathfinding.costMatrix.GetPoint(startPosition) + int(tileCost) + baseCost
        return newCost

    # 
    # Path between two points in a matrix
    #
    def HeuristicAstarPathTo(self, sourceMatrix:Matrix, startPosition:Vector2, endPositon:Vector2, pathRuleFunction, tileCostFunction = tileNoCostRule ) -> list:

        default_directions:list = [ Vector2(-1,0), Vector2(1,0), Vector2(0,-1), Vector2(0,1) ]

        self.pathfindingMatrix = sourceMatrix

        # Used for debug
        self.debugPathMatrix = self.pathfindingMatrix.EmptyCopy("debug path", 0)

        # Which neighbours to check

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
            if ( currentNode.node.position == endPositon ):
                print("Found path in " + str(iterations) + " iterations")
                break

            # Go through path
            for neighbour in default_directions:

                # Pathfinding rule
                nextPos = pathRuleFunction(self, currentNode.node.position, currentNode.node.position + neighbour)

                # Pathfinding rule is not allowing this move
                if nextPos == None:
                    continue

                # Calculate new cost to move into this tile
                oldCost = self.costMatrix.GetPoint(nextPos)
                newCost = tileCostFunction(self, currentNode.node.position, nextPos)

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
    def AStarPathTo(self, grid:Matrix, startPos:Vector2, endPosition:Vector2, 
                    ruleset = DefaultPathfindingRule()
                    ) -> Vector2List:

        self.pathfindingMatrix = grid

        done = dict[Node, Node]()
        startNode = Node(startPos, Vector2(0, 1), 0)
        frontier: list[PathNode] = [PathNode(0, startNode, None)]
        while frontier:
            current = heap.heappop(frontier)

            if current.node in done:
                continue
            done[current.node] = current.parent

            if ruleset.DidReachGoal(self, current, endPosition):
                node = current.node
                path = Vector2List()
                path.append(node.position)
                while True:
                    node = done[node]
                    if node is None:
                        break
                    path.append(node.position)
                return path.Reverse()

            nextDirections = ruleset.GetDirections(self, current)
            for facing in nextDirections:
                pathNode = ruleset.CreateNewPathNode(self, current, facing)
                if pathNode == None or pathNode.node in done:
                    continue
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

    def printDebugMatrix(self, pad:str = "00", space = " "):

        colorList = list()
        colorList.append(("S", bcolors.YELLOW))
        colorList.append(("E", bcolors.YELLOW))
        colorList.append(("P", bcolors.YELLOW))
        colorList.append(("0", bcolors.DARK_GREY))

        self.debugPathMatrix.PrintWithColor(colorList, bcolors.DARK_GREY , pad, space)

