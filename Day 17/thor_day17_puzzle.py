#!/usr/bin/python3
#
# Day 17 Trick Shot : https://adventofcode.com/2021/day/17
# 

import sys
import time
sys.path.insert(1, '../Libs')
from advent_libs import *
from advent_libs_matrix import *

# Rules
# The probe's x position increases by its x velocity.
# The probe's y position increases by its y velocity.
# Due to drag, the probe's x velocity changes by 1 toward the value 0; that is, it decreases by 1 if it is greater than # 0, increases by 1 if it is less than 0, or does not change if it is already 0.
#Due to gravity, the probe's y velocity decreases by 1.

def mark_area(matrix, start_pos, end_pos):
    for y in range(start_pos[1],end_pos[1]):
        for x in range(start_pos[0],end_pos[0]):
            matrix[x][y] = "T"

def calculate_path(start_pos, end_pos, velocity):
    shot_list = list()

    (x,y) = start_pos
    (vx,vy) = velocity
    shot_list.append((x,y, "S"))
#    print(point_to_str("end", end_pos))

    for i in range(10):
        # The probe's x position increases by its x velocity.
        x += vx
        # The probe's y position increases by its y velocity.
        y += vy
        # Due to drag, the probe's x velocity changes by 1 toward the value 0; that is, it decreases by 1 if it is greater than 0, increases by 1 if it is less than 0, or does not change if it is already 0.
        if vx > 0:
            vx -= 1
#        else:
#            vx -= 1    

        # Due to gravity, the probe's y velocity decreases by 1.
        vy -= 1
        shot_list.append((x,y, "#"))

        if x > end_pos[0] and y < end_pos[1]:
            return shot_list
        
    return shot_list

def move_path_on_matrix(path,mx,my):

    if mx >= 0 and my >= 0:
        return path

    incx = 0
    incy = 0
    if mx < 0:
        incx = 0 - mx
    if my < 0:
        incy = 0 - my

    new_path = list()
    for (x,y,value) in path:
        new_path.append( ( x + incx, y + incy, value ))
    return new_path

def fire_shot(input,velocity):

    x1 = 30
    y1 = 14

    start_pos = (0,0)
    #velocity = input
    end_pos = ( -10,-5 )

    path = calculate_path(start_pos,end_pos, velocity)

    (maxx,maxy) = max_point_in_list(path)
    (minx,miny) = min_point_in_list(path)
    
    mx = maxx
    if ( minx < 0 ):
        mx -= minx
    my = maxy
    if ( miny < 0 ):
        my -= miny    

    matrix = create_empty_matrix(mx+1,my+1,".")

    # Move path to fit inside matrix
    path = move_path_on_matrix(path, minx, miny)

    #flipped_path = flip_path_on_y(path)

    # Mark areay on impact
    #mark_area(matrix,(x1-11,y1-6), (x1,y1))
    # Plot path    
    matrix_plot_list(matrix,path)
    print_matrix_color("path",matrix, ".", bcolors.DARK_GREY, "0","")

    return 0

# Unittests
unittest_input(fire_shot, (7,2), 0, "target area: x=20..30, y=-10..-5")
unittest_input(fire_shot, (6,3), 0, "target area: x=20..30, y=-10..-5")
unittest_input(fire_shot, (9,0), 0, "target area: x=20..30, y=-10..-5")
unittest_input(fire_shot, (17,-4), 0, "target area: x=20..30, y=-10..-5")
unittest_input(fire_shot, (6,9), 0, "target area: x=20..30, y=-10..-5")

# Puzzle input : target area: x=206..250, y=-105..-57