#
# Day 15 Chiton : https://adventofcode.com/2021/day/14
# 

import sys
import time
sys.path.insert(1, '../Libs')
from advent_libs import *
from advent_libs_path import *

def create_risk_matrix_from_data(data_lines):

    first_line = data_lines[0]
    size_x = len(first_line) - 1
    size_y = len(data_lines)

    matrix = create_empty_matrix( size_x, size_y)

    # Fill matrix
    y = int()
    x = int()
    for line in data_lines:
        x = 0

        line = line.strip()
        for char in line:
            matrix[x][y] = int(char)
            x += 1
        y += 1

    return matrix

def summarize_path(matrix, path):
    sum = 0
    for (x,y,r) in path:
        if ( x != 0 or y != 0):
            v = matrix[x][y]
            sum += v
    return sum

def generate_path(filename):
    data_lines = loadfile(filename)

    # Create the risk matrix
    risk_matrix = create_risk_matrix_from_data(data_lines)
    end_pos = get_matrix_size(risk_matrix)
    (visited_matrix,path) = path_astar( risk_matrix, (0,0), (end_pos[0]-1,end_pos[1]-1))

    #print_matrix_color("path-astar #1:", risk_matrix, 0, bcolors.DARK_GREY)
    #print_matrix_color("path-astar #2:", visited_matrix, 0, bcolors.DARK_GREY)

    sum = summarize_path(risk_matrix, path)
    return sum


unittest(generate_path, 40,"chiton_data_example.txt")
unittest(generate_path, 40,"chiton_data.txt")
