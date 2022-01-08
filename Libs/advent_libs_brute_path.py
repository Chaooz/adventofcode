
from os import path
import sys
sys.path.insert(1, '../Libs')
from advent_libs import *
from advent_libs_matrix import *

global star_loops

def is_in_matrix(matrix, x,y):
    if ( x < 0 or y < 0 ):
        return False    
    size = get_matrix_size(matrix)
    if (x >= size[0] or y >= size[1] ):
        return False
    return True

def find_min(txt,visited_matrix, position, current_depth, max_depth, p):
    risk_left = 1000000
    risk_up   = 1000000

    pos1x = position[0] + 1
    pos1y = position[1]
    pos2x = position[0]
    pos2y = position[1] + 1

    (endx,endy) = get_matrix_size(visited_matrix)

    if position[0] < endx -1:
        risk_left = visited_matrix[pos1x][pos1y]
    if position[1] < endy - 1:
        risk_up = visited_matrix[pos2x][pos2y]

    t = ""
    for i in range(current_depth+1):
        t = t + "-"

    val = 0

    pos = (0,0)
    if risk_left < risk_up:
        pos = (pos1x,pos1y)
        #print(txt +t+" left:" + str(pos) + " depth:" + str(current_depth) + "/" + str(max_depth) + " left:" + str(risk_left) + " up:" + str(risk_up))
        val = risk_left
        p.append(pos)
    elif risk_left > risk_up:
        pos = (pos2x,pos2y)
        #print(txt+t+" up:" + str(pos) + " depth:" + str(current_depth) + "/" + str(max_depth) + " left:" + str(risk_left) + " up:" + str(risk_up))
        val = risk_up
        p.append(pos)

    # Search deeper?
    if ( current_depth < max_depth ):
        (a,pa) = find_min(txt,visited_matrix,(pos1x, pos1y), current_depth + 1, max_depth, p)
        (b,pb) = find_min(txt,visited_matrix,(pos2x, pos2y), current_depth + 1, max_depth, p)
        if a < b:
            val += a
        elif a > b:
            val += b
        else:
            return (0,p)
    return (val,p)
    
#    return min(risk_left,risk_up)
    
def generate_path(visited_matrix, path, position):

    val = visited_matrix[position[0]][position[1]]
    path.append( (position[0],position[1], val ))

    max = 1000000

    risk_left = 1000000
    risk_up   = 1000000

    (endx,endy) = get_matrix_size(visited_matrix)

    pos1x = position[0] + 1
    pos1y = position[1]
    pos2x = position[0]
    pos2y = position[1] + 1

    if position[0] < endx -1:
        risk_left = visited_matrix[pos1x][pos1y]
    if position[1] < endy - 1:
        risk_up = visited_matrix[pos2x][pos2y]

    if risk_left < risk_up:
        generate_path(visited_matrix,path, (pos1x, pos1y))
    elif risk_left > risk_up:
        generate_path(visited_matrix,path, (pos2x, pos2y))
    elif position[0] == endx-1 and position[1]==endy-1:        
        return path
    else:
        #print("Equal:" + str(position) + " val:" + str(risk_up))

        loop_it = True
        i = 0
        while ( loop_it ):
            p = list()
            (a,pa) = find_min("A", visited_matrix, (pos1x, pos1y),0,i,list())
            (b,pb) = find_min("B", visited_matrix, (pos2x, pos2y),0,i,list())
            if a < b:
                #print("going for A:" + str(a) + " => " + str((pos1x, pos1y)))
                generate_path(visited_matrix,path, (pos1x, pos1y))
                loop_it = False
            elif a > b:
                #print("going for B:" + str(b) + " =>" + str((pos2x, pos2y)))
                generate_path(visited_matrix,path, (pos2x, pos2y))
                loop_it = False
            else:
                #generate_path(visited_matrix,path, (position[0]-1, position[1]))

                # Does the two use same cell ?
                if (len(pa) == len(pb)):
                    for p in range(1,len(pa)):
                        if loop_it and pa[p][0] == pb[p][0] and pa[p][1] == pb[p][1]:
                            #print("looptrap:" + str(i) + ":" + str(pb[p]))
                            loop_it = False

                if loop_it:
                    i = i + 1
                    #print("inc i : " + str(i) + " => " + str(a) + ":" + str(b))
                else:
                    #print("Force go path A")
                    generate_path(visited_matrix,path, (pos1x, pos2y))
            
            if i > 5:
                loop_it = False
                print("SUPERERROR")
                print(p)

    return path


def path_brute_path(matrix, from_pos, to_position):

    (size_x,size_y) = get_matrix_size(matrix)    
    visited_matrix = create_empty_matrix2((size_x,size_y))
    end_pos = (size_x-1,size_y-1)

    iteration = 0

    # Set whole map with high value
    for y in range(size_y):
        for x in range(size_x):
            visited_matrix[x][y] = 1000000

    # First point to 0
    visited_matrix[0][0] = 0

    open_list = list()
    open_list.append( (0,1) )
    open_list.append( (1,0) )

    visited_matrix[0][1] = matrix[0][1]
    visited_matrix[1][0] = matrix[1][0]

    neightbour_list = ( (1,0), (-1,0), (0,1), (0,-1))

    path = list()

    while( len(open_list) > 0 ):

        iteration += 1
        #if iteration % 100 == 0:
        #    print("Iteration:" + str(iteration) + " listlen:" + str(len(open_list)))

        new_list = list()
        for (x,y) in open_list:

            risk = visited_matrix[x][y]

            for (px,py) in neightbour_list:
                xx = x + px
                yy = y + py

                if not is_in_matrix(matrix,xx,yy):
                    continue

                neigbour_risk = matrix[xx][yy]
                if visited_matrix[xx][yy] > risk + neigbour_risk:
                    visited_matrix[xx][yy] = risk + neigbour_risk
                    new_list.append((xx,yy))
            open_list = new_list


    #print( visited_matrix[end_pos[0]][end_pos[1]])
    path = generate_path(visited_matrix, path, (0,0))

    return (visited_matrix,path)



