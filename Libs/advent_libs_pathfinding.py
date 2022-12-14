
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

    def __init__(self, parent = None, position = None ):
        self.parent = parent
        self.position = position

    def __eq__(self, other):
        return self.position == other.position

    def to_string(self):
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

    def HeuristicAstarPathTo(self, matrix:Matrix, fromPosition:Vector2, toPositon:Vector2, maxStep:int) -> Vector2List:

        open_list = Vector2List()
        closed_list = Vector2List()

        start_node = PathNode(None,Vector2(fromPosition))
        end_node = PathNode(None,Vector2(toPositon))

        # Add the start node
        open_list.append( start_node )

        while( open_list.len() > 0):

            current_node = open_list.GetWithIndex( 0 )
            current_index = 0

            # Find node with lowest F
            for index,item in enumerate(open_list):
                if ( item.f < current_node.f ):
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if ( current_node == end_node ):
                path = Vector2List()
                current = current_node
                current_cost = 0
                while current is not None:
                    path.append( (current.position, current_cost ) )
                    current = current.parent

                # TODO: Reverse pathlist
                #path = path[::-1]

                return path

            # Create list of children to path
            child_list = list()
            for neighbour in self.neighbours:

                # Child  position
                position = current_node.position + neighbour
#                position = ( current_node.position.x + neighbour[0], current_node.position.y + neighbour[1] )

                # Outside of matrix?
                if not matrix.IsPointInside(position):
                    continue

                # Make sure walkable terrain
#                if matrix[position[0]][position[1]] != 0:
#                    continue

                child = PathNode( current_node, position)
                child_list.append(child)

            # Path through all children        
            for child in child_list:

                # If child is in closed list, goto next child
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position.x - end_node.position.x) ** 2) + ((child.position.y - end_node.position.y) ** 2)
                child.f = child.g + child.h

                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add child to open list
                open_list.append(child)
        
        print("EOL")
        return None

# def node_list_has_higher_g( node_list, child_node ):
#     for node in node_list:
#         if ( node.position == child_node.position and node.g > child_node.g ):
#             return True
#     return False

# def count_parents(parent_node):
#     if parent_node.parent:
#         count = count_parents(parent_node.parent)
#         return count + 1
#     return 1


