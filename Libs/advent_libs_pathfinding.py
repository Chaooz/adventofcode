
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

#        if cost < 10000:
#            return

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

    def HeuristicAstarPathTo(self, matrix:Matrix, startPosition:Vector2, endPositon:Vector2, maxStep:int) -> Vector2List:

        # Add the start node with 0 cost
        checkList = Vector2List()
        checkList.append( PathNode( startPosition, 0) )

        # Add startpos with cost 0
        cellCost = {}
        cellCost[startPosition.Tuple()] = 0

        # Global path
        cameFrom = {}
        cameFrom[startPosition.Tuple()] = None

        while( checkList.len() > 0):
            currentNode:PathNode = checkList.GetWithIndex( 0 )

            # Success
            if ( currentNode.position == endPositon ):
                print("SUCCESS")
                break

            # Go through path
            for neighbour in self.neighbours:
                nextPos = currentNode.position + neighbour

                # Outside of matrix?
                if not matrix.IsPointInside(nextPos):
                    continue

                cost = cellCost[currentNode.position.Tuple()] 
                cost += self.heuristic(nextPos, currentNode.position)

                # If we should path here due to cost
                nextPosTuple = nextPos.Tuple()
                if not nextPosTuple in cellCost or cost < cellCost[nextPosTuple]:
                    cellCost[nextPosTuple] = cost

                i = 0
                while i < checkList.len():
                    checkPoint:PathNode = checkList.GetWithIndex(i)
                    if checkPoint.cost > cost:
                        break
                    i = i + 1

                checkList.SetWithIndex( i, PathNode(nextPos, cost) )
                cameFrom[nextPosTuple] = currentNode

        # Find the path
        currentPos = endPositon
        result = []
        if currentPos in cameFrom:
            while currentPos != startPosition:
                result.append(currentPos)
                currentPos = cameFrom[currentPos]
            if result:
                result.reverse
        return result

