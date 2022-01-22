#!/usr/bin/python3
#
# Day 17 Trick Shot : https://adventofcode.com/2021/day/17
# 

from dis import show_code
import sys
import time
sys.path.insert(1, '../Libs')
from advent_libs import *
from advent_libs_matrix import *

#
# Debug: Add a field in the printed graph with T that markes the
#        valid end position area.
#
def debug_mark_area(matrix, start_pos, end_pos, move_x, move_y):
    y1 = min(start_pos[1],end_pos[1])
    y2 = max(start_pos[1],end_pos[1])
    for y in range(y1,y2 + 1):
        for x in range(start_pos[0],end_pos[0] + 1):
            matrix[x + move_x][y + move_y] = "T"

#
# Debug: Adjust the path up/down on y-axis to make it fit in the 
#        pretty printed graph that we draw
#
def debug_move_path_on_matrix(path,incx,incy):
    new_path = list()
    for (x,y,value) in path:
        new_path.append( ( x + incx, y + incy, value ))
    return new_path

#
# Debug: Since graph in assignment is upside down ( y is negative ), 
#        flip matrix to make y go up ( to make it pretty in print )
#
def debug_flip_matrix_y(matrix):
    size = get_matrix_size(matrix)
    size_x = size[0]
    size_y = size[1]
    flipped_matrix = create_empty_matrix(size_x, size_y)
    for y in range(size_y):
        for x in range(size_x):
            flipped_matrix[x][size_y - y - 1] = matrix[x][y]
    return flipped_matrix

#
# Debug: Print a pretty graph to be able to see if the paths matches
#        the examples in the assignment
#
def debug_print_graph(path, target_start_pos, target_end_pos):

    (maxx,maxy) = max_point_in_list(path)
    (minx,miny) = min_point_in_list(path)

    # Make sure target pos fits in matrix
    minx = min( minx, target_start_pos[0])
    minx = min( minx, target_end_pos[0])
    miny = min( miny, target_start_pos[1])
    miny = min( miny, target_end_pos[1])

    maxx = max( maxx, target_start_pos[0])
    maxx = max( maxx, target_end_pos[0])
    maxy = max( maxy, target_start_pos[1])
    maxy = max( maxy, target_end_pos[1])

    diff_x = abs(min(0,minx))
    diff_y = abs(min(0,miny))

    # Since coordinates can go from - on the coordinates, adjust everthing to start at 0
    mx = maxx + diff_x
    my = maxy + diff_y

    # Move path to fit inside matrix
    matrix = create_empty_matrix(mx+1,my+1,".")
    matrix_path = debug_move_path_on_matrix(path, diff_x, diff_y)
    #flipped_path = flip_path_on_y(path)
    debug_mark_area(matrix,target_start_pos, target_end_pos, diff_x, diff_y)
    matrix_plot_list(matrix,matrix_path)
    flipped_matrix = debug_flip_matrix_y(matrix)
    print_matrix_color("path",flipped_matrix, ".", bcolors.DARK_GREY, "0","")


#
# Calculate the path based on the velocity vector
# Rules:
# * The probe's x position increases by its x velocity.
# * The probe's y position increases by its y velocity.
# * Due to drag, the probe's x velocity changes by 1 toward the value 0; that is, it decreases by 1 if it
#   is greater than # 0, increases by 1 if it is less than 0, or does not change if it is already 0.
# * Due to gravity, the probe's y velocity decreases by 1.
#
def calculate_path(target_start_pos, target_end_pos, velocity):
    shot_list = list()
    max_path_length = 1000

    (x,y) = (0,0)
    (vx,vy) = velocity
    shot_list.append((x,y, "S"))

    for i in range(max_path_length):
        # The probe's x position increases by its x velocity.
        x += vx
        # The probe's y position increases by its y velocity.
        y += vy
        # Due to drag, the probe's x velocity changes by 1 toward the value 0; that is, it decreases by 1 if it is greater than 0, increases by 1 if it is less than 0, or does not change if it is already 0.
        if vx > 0:
            vx -= 1

        # Due to gravity, the probe's y velocity decreases by 1.
        vy -= 1

        # If we have not passed end-point
        if x <= target_end_pos[0] and y >= target_end_pos[1]:
            shot_list.append((x,y, "#"))

        # If we have passed start point 
        if x > target_start_pos[0] and y < target_start_pos[1]:
            return shot_list
        
    return shot_list

#
# Split the input area text into start and end points
# "target area: x=20..30, y=-10..-5" will be split into (20,-10) and (30,-5)
# Argument: input_text  - The text we wan to split into landing points
#
def get_target_area(input_text):
    # "target area: x=20..30, y=-10..-5"
    points_text = input_text.split(":")  # => "target area" and " x=20..30, y=-10..-5"
    xy_text = points_text[1].split(",")  # => "x=20..30" and "y=-10..-5"
    str_xx = xy_text[0].split("=")[1]        # => "20..30"
    str_yy = xy_text[1].split("=")[1]        # => "-10..-5"
    xx = str_xx.split("..")                  # => "20" and "30"
    yy = str_yy.split("..")                  # => "-10" and "-5"

    y1 = int(yy[0])
    y2 = int(yy[1])

    start_point = (int(xx[0]),max(y1,y2))    # => (20,-10)
    end_point = (int(xx[1]),min(y1,y2))      # => (30,-5)
    return start_point,end_point

#
# Return the last point in a path if it is inside the landing area
# Argument: Path  - The path we want to check
# Argument: Start - Start point for the landing area, f.ex (20,-10)
# Argument: End   - End point for the landing area, f.ex (30,-5)
#
def get_point_in_area(path,start,end):
    if len(path) > 0:
        path.reverse()
        last_point = path[0]
        if last_point[0] >= start[0] and last_point[0] <= end[0]:
            if last_point[1] <= start[1] and last_point[1] >= end[1]:
                return (last_point[0],last_point[1])

    return None

def get_max_y_in_path(path):
    max_y = -99999
    for (x,y,value) in path:
        max_y = max(y,max_y)           
    return max_y

def fire_shot(input, parameters):

    velocity,show_graph = parameters
    start_pos, end_pos = get_target_area(input)

    path = calculate_path(start_pos, end_pos, velocity)

    # Check if last point is inside start/end position

    if show_graph:
        debug_print_graph(path, start_pos, end_pos)

    point = get_point_in_area(path, start_pos, end_pos)
    if not point is None:
        return get_max_y_in_path(path)
    return -1

def puzzle1_fire(input):
    start_pos, end_pos = get_target_area(input)

    max_y = 0
    p = (0,0)
    pp = None
    for y in range(1,1000):
        for x in range(1,21):
            velocity = (x,y)
            path = calculate_path(start_pos, end_pos, velocity)
            point = get_point_in_area(path, start_pos, end_pos)
            if not point is None:
                yy = get_max_y_in_path(path)
                if ( yy > max_y ):
                    max_y = yy
                    p = (x,y)
                    pp = path

    #print("fire_best_shot : " + str(p[0]) + "x" + str(p[1]) + " height:" + str(max_y))
    return max_y


def fire_best_shot_velocity(input, parameters):
    velocity, show_graph = parameters
    start_pos, end_pos = get_target_area(input)

    num_paths = 0
    path = calculate_path(start_pos, end_pos, velocity)
    point = get_point_in_area(path, start_pos, end_pos)
    if not point is None:
        num_paths += 1
    return num_paths

def puzzle2_fire(input):
    start_pos, end_pos = get_target_area(input)

    mx = 0
    miy = 0
    may = 0
    num_paths = 0
    for y in range(-200,200):
        for x in range(1,500):
            velocity = (x,y)
            path = calculate_path(start_pos, end_pos, velocity)
            point = get_point_in_area(path, start_pos, end_pos)
            if not point is None:
                #print("fire_best_shot_number : " + str(x) + "x" + str(y) + " height:" + str(point))
                num_paths += 1
                mx = max(mx,x)
                miy = min(miy,y)
                may = max(may,y)

#    print("range: max-x:" + str(mx) + " => min-y:" + str(miy) + " max-y:" + str(may))
    return num_paths


test_range = "target area: x=20..30, y=-10..-5"
puzzle_range = "target area: x=206..250, y=-105..-57"

# Unittests for exmample with velocity
unittest_input(fire_shot, ((7,2),True), 3, test_range)
unittest_input(fire_shot, ((6,3),False), 6, test_range)
unittest_input(fire_shot, ((9,0),False), 0, test_range)
unittest_input(fire_shot, ((17,-4),False), -1, test_range)
unittest_input(fire_shot, ((6,9),False), 45, test_range)

# Unittest for example (without velocity)
unittest(puzzle1_fire, 45, test_range)

# Unittest puzzle 2 : Test two if the numbers in the list to make sure it is correct
unittest_input(fire_best_shot_velocity, ((23,-10),False), 1, test_range)
unittest_input(fire_best_shot_velocity, ((8,0),False), 1, test_range)
unittest(puzzle2_fire, 112, test_range)

# Unittest puzzles
unittest(puzzle1_fire, 5460, puzzle_range)
unittest(puzzle2_fire, 3618, puzzle_range)

puzzle1 = puzzle1_fire(puzzle_range)
print("Day 17 puzzle 1: Height = " + str(puzzle1))
puzzle2 = puzzle2_fire(puzzle_range)
print("Day 17 puzzle 2: Number of occurances = " + str(puzzle2))
