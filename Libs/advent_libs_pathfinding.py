
from advent_libs import *
from advent_libs_matrix import *
from advent_libs_vector2 import *

sys.setrecursionlimit(15000)

class PathNode:
    g = int()
    f = int()
    h = int()
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
    matrix:Matrix
    shortestPath:list
    iterations:int

    def __init__(self) -> None:
        global shortestPath, iterations

        shortestPath = list()
        iterations = 0
        pass

    def InternalAStarPath(self, matrix:Matrix, visitedMatrix:Matrix, path:list, fromPosition:Vector2, toPositon:Vector2, maxStep:int, totalCost:int ):

        global shortestPath, iterations

        if iterations > 200000:
            return

        # IS the position outside the matrix ?
        if not matrix.IsPointInside(fromPosition):
            return

        # If the cost is already lower, abandon this path
        cost = int(visitedMatrix.GetPoint(fromPosition))

        if cost <= totalCost:
            return


        # Get height/cost from point
        height = int(matrix.GetPoint(fromPosition))
#        totalCost += height
        totalCost += 1

        # Set the cost in the field
        visitedMatrix.SetPoint( fromPosition, totalCost )

        # Add position to path
        path.append((fromPosition, totalCost))

        # Did we reach the end position ?
        if fromPosition == toPositon:
            shortestPath = path.copy()

#        if iterations % 100000 == 0:
#            visitedMatrix.Print("999",bcolors.DARK_GREY, "000", "")
        iterations += 1

        for neighbour in self.neighbours:
            if matrix.IsPointInside(fromPosition+neighbour):
                nextHeight = int(matrix.GetPoint(fromPosition + neighbour))

                if maxStep == -1:
                    self.InternalAStarPath(matrix, visitedMatrix, path, fromPosition + neighbour, toPositon, maxStep, totalCost + 1)
                elif height + maxStep >= nextHeight:
                    self.InternalAStarPath(matrix, visitedMatrix, path, fromPosition + neighbour, toPositon, maxStep, totalCost + 1)

        path.pop()

    #
    # Path between fromPosition to toPosition
    #
    def AStarPathTo(self, matrix:Matrix, fromPosition:Vector2, toPositon:Vector2, maxStep:int) -> Vector2List:
        global shortestPath
        shortestPath.clear()
        path = list()
        visitedMatrix = Matrix("Visited", matrix.sizeX, matrix.sizeY, 10000)
        self.InternalAStarPath(matrix, visitedMatrix, path, fromPosition, toPositon, maxStep, 0 )

        # Debug
        #visitedMatrix.Print(10000, bcolors.DARK_GREY,"0000", " ")

        if len(shortestPath) > 0:
            print("Found path: " + str(len(shortestPath)))
        return shortestPath

    #
    # ###################
    #
    def heuristic(self,startPos:Vector2,endPos:Vector2):
        return ((startPos.x - endPos.x) ** 2) + ((startPos.y - endPos.y) ** 2)

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
    #
    def oneStepPathRule(self, pathfindingArea:Matrix, startPosition:Vector2, endPositon:Vector2):
        endPositon = self.defaultPathRule(pathfindingArea, startPosition, endPositon)
        if endPositon != None:
            a = pathfindingArea.GetPoint(startPosition)
            b = pathfindingArea.GetPoint(endPositon)
            if b > a + 1:
                return None
        return endPositon

    def HeuristicAstarPathTo(self, pathfindingArea:Matrix, startPosition:Vector2, endPositon:Vector2, pathRuleFunction) -> Vector2List:

        # Used for debug
        debugPathMatrix = pathfindingArea.EmptyCopy("debug path", 0)

        # Add the start node with 0 cost
        checkList = Vector2List()
        checkList.append( PathNode( startPosition, 0) )

        # Add start position to the cost matrix
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
                newCost = costMatrix.GetPoint(currentNode.position) + self.heuristic(nextPos, currentNode.position)
                if oldCost == -1 or newCost < oldCost:
                    costMatrix.SetPoint( nextPos, newCost )

                    i = 0
                    while i < checkList.len():
                        checkPoint:PathNode = checkList.GetWithIndex(i)
                        if checkPoint.cost > newCost:
                            break
                        i = i + 1

                    checkList.SetWithIndex( i, PathNode(nextPos, newCost) )
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

