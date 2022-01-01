#
# Day 15 Chiton : https://adventofcode.com/2021/day/14
# 

import sys
import time
#from Libs.advent_libs import compress_matrix
sys.path.insert(1, '../Libs')
from advent_libs import *
from advent_libs_path import *
# Pathfinding lib
#from advent_libs_astar import heuristic_astar_path4
from advent_libs_heatmap import path_heatmap_astar

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

def debug_show_path_in_matrix(matrix, path, matrix_size):
    path_matrix = create_empty_matrix2(matrix_size)

    current_risk = 0
    for (x,y,r) in path:
        risk = matrix[x][y]
        path_matrix[x][y] = risk + current_risk
        current_risk += risk
    return path_matrix

def generate_path(filename):
    data_lines = loadfile(filename)

    # Create the risk matrix
    risk_matrix = create_risk_matrix_from_data(data_lines)
    end_pos = get_matrix_size(risk_matrix)
    (visited_matrix,path) = path_astar( risk_matrix, (0,0), (end_pos[0]-1,end_pos[1]-1))

    path_matrix = debug_show_path_in_matrix(risk_matrix,path,end_pos)

    # Show compressed version?
    if ( end_pos[0] > 25 ):
        path_matrix = compress_matrix(path_matrix, 10)
        visited_matrix = compress_matrix(visited_matrix, 10)
        risk_matrix = compress_matrix(risk_matrix, 10)

    print_matrix_color_padded("path-astar #1:", risk_matrix, 0, bcolors.DARK_GREY, "00")
    print_matrix_color_padded("path-astar #2:", visited_matrix, 0, bcolors.DARK_GREY, "00")
    print_matrix_color_padded("path-astar #3", path_matrix, 0, bcolors.DARK_GREY,"00")

    sum = summarize_path(risk_matrix, path)
    return sum

def generate_heat_path(filename):
    data_lines = loadfile(filename)

    # Create the risk matrix
    risk_matrix = create_risk_matrix_from_data(data_lines)
    #print_matrix_color_padded("path-heat-risk #1:", risk_matrix, 0, bcolors.DARK_GREY, "00")

    end_pos = get_matrix_size(risk_matrix)

    (visited_matrix,path) = path_heatmap_astar( risk_matrix, (0,0), (end_pos[0],end_pos[1]))
    #print_matrix_color_padded("path-fast-astar #3", visited_matrix, 0, bcolors.DARK_GREY,"00")

    comp_matrix = compress_matrix(visited_matrix, 5)
    #print_matrix_color_padded("inp", comp_matrix, 0, bcolors.DARK_GREY, "0000")

    # Print path
    path_matrix = create_empty_matrix2(end_pos)
    for (xx,yy,r) in path:
        path_matrix[xx][yy] = risk_matrix[xx][yy]
    print_matrix_color_padded("path-heat-path #3", path_matrix, 0, bcolors.DARK_GREY,"0")

    sum = summarize_path(risk_matrix, path)
    return sum

def generate_fast_path(filename):
    data_lines = loadfile(filename)

    # Create the risk matrix
    risk_matrix = create_risk_matrix_from_data(data_lines)
    end_pos = get_matrix_size(risk_matrix)

    empty_matrix = create_empty_matrix2(end_pos)

    (visited_matrix,path) = path_heatmap_astar( empty_matrix, (0,0), (end_pos[0]-1,end_pos[1]-1))
#    print_matrix_color_padded("path-fast-astar #3", visited_matrix, 0, bcolors.DARK_GREY,"00")

    comp_matrix = cut_matrix(visited_matrix, 5)
    print_matrix_color_padded("inp", comp_matrix, 0, bcolors.DARK_GREY, "0000")

    # Print path
    path_matrix = create_empty_matrix2(end_pos)
    for (xx,yy,r) in path:
        path_matrix[xx][yy] = risk_matrix[xx][yy]
    print_matrix_color_padded("path-heat-path #3", path_matrix, 0, bcolors.DARK_GREY,"0")

  #  print_matrix_color_padded("path-heat-risk #1:", risk_matrix, 0, bcolors.DARK_GREY, "000")

    sum = summarize_path(risk_matrix, path)
    return sum


unittest(generate_path, 40,"chiton_data_example.txt")
unittest(generate_heat_path, 40,"chiton_data_example.txt")
unittest(generate_heat_path, 447,"chiton_data.txt")
