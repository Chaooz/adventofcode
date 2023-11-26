
import math

from advent_libs import *
from advent_libs_matrix import *
from advent_libs_vector2 import *

class PathNode:

    cost = int()
    position = Vector2()
    parent = None

    def __init__(self, position:Vector2, cost:int = 0):
#        self.parent = parent
        self.position = position

    def __eq__(self, other):
        return self.position == other.position

    def ToString(self):
        return str(self.position.x) + "x" + str(self.position.y) + " F:" + str(self.f) + " G:" + str(self.g) + " H:" + str(self.h)

class Pathfinding:

    MAX_ITERATINS = 1000000

    neighbours = [ Vector2(-1,0), Vector2(1,0), Vector2(0,-1), Vector2(0,1) ]
    iterations:int

    def __init__(self) -> None:
        global iterations
        iterations = 0

    #
    # Pathfinding rule:
    # Default rule: Can move in all positions inside matrix
    #
    def defaultPathRule(self,pathfindingArea:Matrix, startPosition:Vector2, endPositon:Vector2):
        # Outside of matrix?
        if not pathfindingArea.IsPointInside(endPositon):
            return None
        return endPositon

    #
    # Pathfinding rule:
    # Can move max 1 step up ( can always move forward or down )
    # Used in 2022-Day12
    #
    def oneStepPathRule(self, pathfindingArea:Matrix, startPosition:Vector2, endPositon:Vector2):
        endPositon = self.defaultPathRule(pathfindingArea, startPosition, endPositon)
        if endPositon != None:
            a = pathfindingArea.GetPoint(startPosition)
            b = pathfindingArea.GetPoint(endPositon)
            if b > a + 1:
                return None
        return endPositon

    # 
    # Path between two points in a matrix
    #
    def HeuristicAstarPathTo(self, pathfindingArea:Matrix, startPosition:Vector2, endPositon:Vector2, pathRuleFunction) -> Vector2List:

        # Used for debug
        debugPathMatrix = pathfindingArea.EmptyCopy("debug path", 0)

        # Add the start node with 0 cost
        checkList = Vector2List()
        checkList.append( PathNode( startPosition, 0) )

        # Add start position to the cost matrix (with 0 cost)
        costMatrix = pathfindingArea.EmptyCopy("CostMatrix", -1)
        costMatrix.SetPoint( startPosition, 0 )

        # Global path
        cameFrom = {}
        cameFrom[startPosition.Tuple()] = None

        iterations = 0

        while( checkList.len() > 0 and iterations < Pathfinding.MAX_ITERATINS ):
            iterations += 1
            currentNode:PathNode = checkList.GetWithIndex( 0 )
            checkList.RemoveWithIndex(0)

            # Success
            if ( currentNode.position == endPositon ):
                break

            # Go through path
            for neighbour in self.neighbours:

                # Pathfinding rule
                nextPos = pathRuleFunction(pathfindingArea, currentNode.position, currentNode.position + neighbour)

                # Pathfinding rule is not allowing this move
                if nextPos == None:
                    continue

                # Normal Heuristic A* path finding
                oldCost = costMatrix.GetPoint(nextPos)
                heuristicCost = math.sqrt((currentNode.position.x - nextPos.x) ** 2) + ((currentNode.position.y - nextPos.y) ** 2)
                newCost = costMatrix.GetPoint(currentNode.position) + heuristicCost
                if oldCost == -1 or newCost < oldCost:
                    costMatrix.SetPoint( nextPos, newCost )

                    i = 0
                    while i < checkList.len():
                        checkPoint:PathNode = checkList.GetWithIndex(i)
                        if checkPoint.cost > newCost:
                            break
                        i = i + 1

                    checkList.InsertWithIndex( i, PathNode(nextPos, newCost) )
                    cameFrom[nextPos.Tuple()] = currentNode.position

                    # Investigate this node
                    debugPathMatrix.SetPoint(nextPos, pathfindingArea.GetPoint(nextPos))

        # Find the path
        currentPos = endPositon
        result = []
        if cameFrom != None and currentPos.Tuple() in cameFrom:
            while currentPos != startPosition:
                result.append(currentPos)
                currentPos = cameFrom[currentPos.Tuple()]
            if result:
                result.append(startPosition)
                result.reverse

        debugPathMatrix.SetPoint(endPositon, "EE")
#        debugPathMatrix.Print(0, bcolors.DARK_GREY, "00", "")

        return result

    #
    # Show the path in a matrix
    #
    def DebugPrintPath( self, pathfindingArea:Matrix, shortestPath:Vector2List ):
        # Print path in 
        pathMatrix = pathfindingArea.EmptyCopy("ShowPath", ".")
        for index in range(len(shortestPath)):
            point = shortestPath[index]
            pathMatrix.Set(point.x,point.y, "X")
        pathMatrix.Print(".", bcolors.DARK_GREY, "0", "")
