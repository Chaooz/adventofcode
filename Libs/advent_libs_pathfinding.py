
from advent_libs import *
from advent_libs_matrix import *
from advent_libs_vector2 import *

sys.setrecursionlimit(1500)

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
        if cost <= totalCost:
            return

        # Get height/cost from point
        height = int(matrix.GetPoint(fromPosition))
#        totalCost += height
        totalCost += 1

        # Set the cost in the field
        visitedMatrix.SetPoint( fromPosition, totalCost )

        # Add position to path
        path.append(fromPosition)

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
        visitedMatrix.Print(10000, bcolors.DARK_GREY,"0000", " ")
        print(shortestPath)
        return shortestPath

