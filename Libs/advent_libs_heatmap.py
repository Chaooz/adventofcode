#from advent_libs import bcolors, print_matrix_color
#from advent_libs import is_in_matrix, create_empty_matrix, create_empty_matrix2, get_matrix_size


from os import path
import sys
sys.path.insert(1, '../Libs')
from advent_libs import *
from advent_libs_matrix import *

global star_loops

def path_heatmap_astar(matrix, from_pos, to_position):

    global star_loops
    star_loops = 0

    matrix_size = get_matrix_size(matrix)
    visited_matrix = create_empty_matrix2(matrix_size)

    path = list()
    short_path = list()

    #print("Start Heatmap : " + str(from_pos) + " => " + str(to_position))

    val = traverse_path(matrix, visited_matrix, from_pos[0], from_pos[1], to_position[0], to_position[1])
    new_path = create_path_from_matrix( visited_matrix, 0, 0, to_position[0] - 1, to_position[1] - 1)
    return (visited_matrix,new_path)

def is_in_matrix(matrix, x,y):
    if ( x < 0 or y < 0 ):
        return False    
    size = get_matrix_size(matrix)
    if (x >= size[0] or y >= size[1] ):
        return False
    return True

def create_path_from_matrix(matrix, x, y, end_x, end_y):

    if x > end_x or y > end_y:
        return list()

    v1 = 9999
    v2 = 9999
    if x + 1 <= end_x:
        v1 = matrix[x + 1][y]
    if y + 1 <= end_y:
        v2 = matrix[x][y + 1]

    if ( v1 < v2 ):
        path = create_path_from_matrix(matrix, x + 1, y, end_x,end_y)
    elif ( v1 > v2 ):
        path = create_path_from_matrix(matrix, x, y + 1, end_x,end_y)
    else:
        path = create_path_from_matrix(matrix, x, y + 1, end_x,end_y)
        #print("ERRR : " + str(x) + "x" + str(y) + " => " + str(v1) + ":" + str(v2))

    #print("pa:" + str(x) + "x" + str(y))
    path.append( (x, y, 1 ) )

    return path

def traverse_path(matrix, visited_matrix, from_x, from_y, to_x, to_y):

    global star_loops

    # Outside of matrix ?
    if not is_in_matrix(matrix, from_x, from_y ):
        return 0

    risk = matrix[from_x][from_y]

    vrisk = visited_matrix[from_x][from_y]

    if ( vrisk > 0 ):
        return vrisk

    # End position ?
    if ( from_x == to_x and from_y == to_y ):
        visited_matrix[from_x][from_y] = risk
        return risk

    if from_x + 1 >= to_x:
        risk += traverse_path( matrix, visited_matrix, from_x, from_y + 1, to_x, to_y)
    elif from_y + 1 >= to_y:
        risk += traverse_path( matrix, visited_matrix, from_x + 1, from_y, to_x, to_y)
    else:
        risk1 = traverse_path( matrix, visited_matrix, from_x + 1, from_y, to_x, to_y)
        risk2 = traverse_path( matrix, visited_matrix, from_x, from_y + 1, to_x, to_y)
        risk += min(risk1,risk2)

    star_loops += 1

    visited_matrix[from_x][from_y] = risk

    if star_loops % 1000000 == 0:

        cut_matrix = matrix_cut(visited_matrix, 90, 0, 100, 100)
        print_matrix_color_padded("inp", cut_matrix, 0, bcolors.DARK_GREY, "0000")

    return risk
