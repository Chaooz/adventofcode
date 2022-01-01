#
# Heuristia A-Star pathfinding. 
#
# https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
#

from os import path
import sys
sys.path.insert(1, '../Libs')
from advent_libs_matrix import *

class Vector2():
    x = int()
    y = int()

    def __init__(self, xy = None):
        if xy is not None:
            self.x = xy[0]
            self.y = xy[1]

    def __eq__(self, other):
        if isinstance(other,Vector2):
            return self.x == other.x and self.y == other.y
        else:
            return self.x == other[0] and self.y == other[1]

    def tuple(self):
        return ( self.x, self.y )

class Node:
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

def heuristic_astar_path4(matrix, from_position, to_position):
    neightbour_list = ( (1,0), (-1,0), (0,1), (0,-1))
    return heuristic_astar_path(matrix,from_position, to_position, neightbour_list)

def heuristic_astar_path(matrix, from_position, to_position, neightbour_list):

    open_list = list()
    closed_list = list()

    start_node = Node(None,Vector2(from_position))
    end_node = Node(None,Vector2(to_position))

    # Add the start node
    open_list.append( start_node )

    while( len(open_list) > 0):

        current_node = open_list[0]
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
            path = list()
            current = current_node
            current_cost = 0
            while current is not None:
                path.append( (current.position.x, current.position.y, current_cost ) )
                current = current.parent

            path = path[::-1]

            return path

        # Create list of children to path
        child_list = list()
        for neighbour in neightbour_list:

            # Child  position
            position = ( current_node.position.x + neighbour[0], current_node.position.y + neighbour[1] )

            # Outside of matrix?
            if not is_in_matrix(matrix,position):
                continue

            # Make sure walkable terrain
            if matrix[position[0]][position[1]] != 0:
                continue

            child = Node( current_node, Vector2(position))
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

def node_list_has_higher_g( node_list, child_node ):
    for node in node_list:
        if ( node.position == child_node.position and node.g > child_node.g ):
            return True
    return False

def count_parents(parent_node):
    if parent_node.parent:
        count = count_parents(parent_node.parent)
        return count + 1
    return 1
