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

def calculate_path(end_pos):
    shot_list = list()
    shot_list.append((0,3,"S"))
    shot_list.append((5,1,"#"))
    shot_list.append((9,0,"#"))
    shot_list.append((14,0,"#"))
    shot_list.append((18,1,"#"))
    shot_list.append((21,3,"#"))
    shot_list.append((23,6,"#"))
    shot_list.append((24,10,"#"))
    return shot_list

def fire_shot(input):

    x1 = 30
    y1 = 14
    yr1 = -10
    yr2 = -5

    end_pos = ( 20,20 )
    matrix = create_empty_matrix(x1,y1,".")
    mark_area(matrix,(x1-11,y1-6), (x1,y1))
    path = calculate_path(end_pos)
    matrix_plot_list(matrix,path)

    print_matrix_color_padded("path",matrix, ".", bcolors.DARK_GREY, "0","")

    return 0

# Unittests
unittest(fire_shot, (7,2), "target area: x=20..30, y=-10..-5")

# Puzzle input : target area: x=206..250, y=-105..-57