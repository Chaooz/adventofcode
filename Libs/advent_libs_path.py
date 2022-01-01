#from advent_libs import bcolors, print_matrix_color
#from advent_libs import is_in_matrix, create_empty_matrix, create_empty_matrix2, get_matrix_size


from os import path
import sys
sys.path.insert(1, '../Libs')
from advent_libs import *

star_loops = 0

def path_astar(matrix, from_pos, to_position):

    global star_loops
    star_loops = 0

    matrix_size = get_matrix_size(matrix)
    visited_matrix = create_empty_matrix2(matrix_size)

    path = list()
    short_path = list()

    print("Start A-Star : " + str(from_pos) + " => " + str(to_position))

    opened_nodes = list()

    traverse_path(matrix,visited_matrix,path,opened_nodes,short_path,from_pos,to_position, 0)

    #new_path = list()
    #for (x,y,r) in short_path:
    #    new_path.append((x,y))

    return (visited_matrix,short_path)

def is_in_matrix(matrix, position):
    if ( position[0] < 0 or position[1] < 0 ):
        return False    
    size = get_matrix_size(matrix)
    if (position[0] >= size[0] or position[1] >= size[1] ):
        return False
    return True

def debug_path_contains(path,position):
    for (x,y,r) in path:
        if ( x == position[0] and y == position[1]):
            return True
    return False

def add_path_to_matrix(visited_matrix, path_list):
    for (full_x,full_y,full_risk) in path_list:
        v = visited_matrix[full_x][full_y]
        if v > full_risk or v == 0:
            visited_matrix[full_x][full_y] = full_risk

def traverse_path(matrix,visited_matrix, full_path, opened_nodes, short_path, position, to_position, cost):

    global star_loops
    star_loops += 1


    if not is_in_matrix(matrix,position):
        return

    if ( cost > 10000):
        return

    # Failsafe for now
    if len(full_path) > 500:
        return

    pos_x = position[0]
    pos_y = position[1]
    risk = cost + matrix[pos_x][pos_y]

    if ( star_loops % 100000 == 0):
        print("star loops:" + str(star_loops))
        empty_matrix = compress_matrix(visited_matrix, 10)
        print_matrix_color_padded("visited",empty_matrix,0,bcolors.DARK_GREY,"0000000")

    # is the point already in path, exit
    for (f_x,f_y,f_risk) in full_path:
        if ( f_x == pos_x and f_y == pos_y ):
            return

    opened_nodes.append( (pos_x, pos_y, risk ))
    full_path.append( (pos_x, pos_y, risk ) )

    # Pathing longer than shortest path -> exit
#    if len(short_path) > 0:
#        (x,y,r) = short_path[-1]
#        if risk > r:
#            add_path_to_matrix(visited_matrix, full_path)
#            full_path.pop()
#            return

    v = visited_matrix[pos_x][pos_y]
    if risk > v and v > 0:
        full_path.pop()
        return
    else:
        visited_matrix[pos_x][pos_y] = risk

    #print( "" + str(pos_x) + "x" + str(pos_y) + " vs " + str(end_position[0]) + "x" + str(end_position[1]) + " risk:" + str(risk))
    if pos_x == to_position[0] and pos_y == to_position[1]:
        old_risk = 100000
        if len(short_path) > 0:
            (xx,yy,old_risk) = short_path[-1]

        if old_risk > risk:
            #print ( "New path: R=" + str(risk) + " Old-R:" + str(old_risk))
            short_path.clear()
            for (full_x,full_y,full_risk) in full_path:
                short_path.append((full_x,full_y,full_risk))
                #visited_matrix[full_x][full_y] = full_risk
            #print_matrix_color("found short path:" + str(len(full_path)), visited_matrix, 0, bcolors.DARK_GREY)
            full_path.pop()
            return

    # Visit 4 neighbours
    traverse_path( matrix, visited_matrix, full_path, opened_nodes, short_path, (pos_x + 1, pos_y), to_position, risk + 1)
    traverse_path( matrix, visited_matrix, full_path, opened_nodes, short_path, (pos_x, pos_y + 1), to_position, risk + 1)
#    traverse_path( matrix, visited_matrix, full_path, opened_nodes, short_path, (pos_x - 1, pos_y), to_position, risk + 1)
 #   traverse_path( matrix, visited_matrix, full_path, opened_nodes, short_path, (pos_x, pos_y - 1), to_position, risk + 1)
    full_path.pop()


