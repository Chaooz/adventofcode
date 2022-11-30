#
# Day 15 Chiton : https://adventofcode.com/2021/day/14
# 

import sys
import time
sys.path.insert(1, '../Libs')
from advent_libs import *
from advent_libs_path import *
# Pathfinding lib
from advent_libs_matrix import *
from advent_libs_heatmap import path_heatmap_astar
from advent_libs_brute_path import path_brute_path

sys.setrecursionlimit(1500)

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

def sum_path2(matrix, path):
    rp = path[::-1]
    (x,y,r) = rp[0]
#    print(rp[0])
    return r

def debug_show_path_in_matrix(matrix, path, matrix_size):
    path_matrix = create_empty_matrix2(matrix_size)

    current_risk = 0
    for (x,y,r) in path:
        risk = matrix[x][y]
        path_matrix[x][y] = risk + current_risk
        current_risk += risk
    return path_matrix

def show_matrix_graph(text, matrix, show_graph,t = 25, pad = "0000"):
    matrix_size = get_matrix_size(matrix)
    if show_graph:
        if ( matrix_size[0] > 50 ):
            scale = int(matrix_size[0] / t)
            matrix = compress_matrix(matrix, scale)
            print_matrix_color_padded(text + "(compressed)", matrix, 0, bcolors.DARK_GREY,pad, " ")
        else:
            print_matrix_color_padded(text, matrix, 0, bcolors.DARK_GREY,"0", " ")


def show_matrix_graph_cut(text, matrix, show_graph, t=25, pad = "0000"):
    matrix_size = get_matrix_size(matrix)
    if show_graph:
        if ( matrix_size[0] > t ):
            matrix = matrix_cut(matrix, matrix_size[0] - t,matrix_size[1] - t,matrix_size[0], matrix_size[1])
            print_matrix_color_padded(text + " (cut)", matrix, 0, bcolors.DARK_GREY,pad, " ")
        else:
            print_matrix_color_padded(text, matrix, 0, bcolors.DARK_GREY,"0", " ")


def show_matrix_graph_cut2(text, matrix, show_graph, t=25, pad = "0000"):
    matrix_size = get_matrix_size(matrix)
    if show_graph:
        if ( matrix_size[0] > t ):
            matrix = matrix_cut(matrix, 0,0,t,t)
            print_matrix_color_padded(text + " (cut)", matrix, 0, bcolors.DARK_GREY,pad, " ")
        else:
            print_matrix_color_padded(text, matrix, 0, bcolors.DARK_GREY,"0", " ")


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

def paste_matrix(source, destination, mul_x, mul_y ):

    (size_x, size_y) = get_matrix_size( source )

    multiplier = mul_x + mul_y

    xx = size_x * mul_x
    yy = size_y * mul_y

#    print("xx:" + str(xx) + ":" + str(x))

    for y in range(size_x):
        for x in range(size_y):
            v = source[x][y]

            for i in range(multiplier):
                v = (v + 1) % 10
                if v == 0:
                    v = 1

            destination[xx + x][yy + y] = v

def create_large_matrix(matrix, duplicates):

    end_pos = get_matrix_size(matrix)    
    large_risk_map = create_empty_matrix(end_pos[0] * duplicates, end_pos[1] * duplicates)
    
#    paste_matrix(risk_matrix,large_risk_map, 0,0, end_pos[0], end_pos[1], x, y )
    for y in range(duplicates):
        for x in range(duplicates):
            paste_matrix(matrix,large_risk_map,  x, y )

    return large_risk_map

def generate_heat_path2(filename, print_graph):
    data_lines = loadfile(filename)

    # Create the risk matrix
    risk_matrix = create_risk_matrix_from_data(data_lines)
    # Generate large matrix
    large_risk_matrix = create_large_matrix(risk_matrix,5)

    # Show map
    end_pos = get_matrix_size(large_risk_matrix)    
    #print_matrix_color_padded("path-heat-small-risk", risk_matrix, 0, bcolors.DARK_GREY,"0", "")
    #print_matrix_color_padded("path-heat-large-risk", large_risk_matrix, 0, bcolors.DARK_GREY,"0", "")

    (visited_matrix,path) = path_heatmap_astar( large_risk_matrix, (0,0), (end_pos[0],end_pos[1]))

    # Print path
    if print_graph:
        path_matrix = create_empty_matrix2(end_pos)
        for (xx,yy,r) in path:
            path_matrix[xx][yy] = large_risk_matrix[xx][yy]

        if ( end_pos[0] > 50 ):
            path_matrix = compress_matrix(path_matrix, 10)
            print_matrix_color_padded("path-heat-path", path_matrix, 0, bcolors.DARK_GREY,"00", "")
        else:
            print_matrix_color_padded("path-heat-path", path_matrix, 0, bcolors.DARK_GREY,"0", " ")

    sum = summarize_path(large_risk_matrix, path)
    return sum

def generate_brute_map_base(risk_matrix, print_graph):

    # Do pathfinding
    end_pos = get_matrix_size(risk_matrix)    
    (visited_matrix,path) = path_brute_path( risk_matrix, (0,0), (end_pos[0],end_pos[1]))


    # Print path
    if print_graph:
        path_matrix = create_empty_matrix2(end_pos)
        for (xx,yy,r) in path:
            path_matrix[xx][yy] = risk_matrix[xx][yy]
        #show_matrix_graph_cut("generate_brute_map: visited",visited_matrix,print_graph)
        #show_matrix_graph_cut("generate_brute_map: path",path_matrix,print_graph)

        show_matrix_graph_cut2("generate_brute_map: visited",visited_matrix,print_graph)
        #show_matrix_graph_cut2("generate_brute_map: path",path_matrix,print_graph)

        show_matrix_graph("generate_brute_map: path",path_matrix,print_graph, 25, "0")

    sum = sum_path2(risk_matrix, path)
    return sum

def generate_brute_map1(filename, print_graph):
    data_lines = loadfile(filename)
    # Create the risk matrix
    risk_matrix = create_risk_matrix_from_data(data_lines)
    # Run code
    return generate_brute_map_base(risk_matrix,print_graph)

def generate_brute_map2(filename, print_graph):
    data_lines = loadfile(filename)
    # Create the risk matrix
    risk_matrix = create_risk_matrix_from_data(data_lines)
    # Generate large matrix
    large_risk_matrix = create_large_matrix(risk_matrix,5)
    # Run code
    return generate_brute_map_base(large_risk_matrix,print_graph)




show_graphs = False

# Unittest first implementation
#unittest(generate_path, 40,"chiton_data_example.txt")
unittest_input(generate_heat_path2, show_graphs, 315,"day15_unittest_data.txt")
unittest_input(generate_brute_map1, show_graphs, 40,"day15_unittest_data.txt")
unittest_input(generate_brute_map2, show_graphs, 315,"day15_unittest_data.txt")

# Unittest actual puzzle
unittest_input(generate_brute_map1, show_graphs, 447,"thor_day15_data.txt")
unittest_input(generate_brute_map2, show_graphs, 2825,"thor_day15_data.txt")

# Show
print("Puzzle 1 : " + str(generate_brute_map1("thor_day15_data.txt",show_graphs)))
print("Puzzle 2 : " + str(generate_brute_map2("thor_day15_data.txt",show_graphs)))