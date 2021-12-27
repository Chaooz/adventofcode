#
# Day 13 Transparent Origami : https://adventofcode.com/2021/day/13
# 

import sys
sys.path.insert(1, '../Libs')
from advent_libs import *

#
# Decode data into point list and fold list
#
def decode_data(data):

    fold_list = list()
    point_list = list()

    for line in data:
        line = line.strip()

        # Fold rules
        if line.startswith("fold"):
            fold_list.append(line)
        elif line != "":
            point = line.split(",")
            point_list.append(point)
    
    result = list()
    result.append(point_list)
    result.append(fold_list)
    return result


def pointlist_to_matrix(point_list):

    max_point = max_point_in_list(point_list)
    size_x = max_point[0] + 1
    size_y = max_point[1] + 1

    if (size_x % 2 == 0):
        size_x = size_x + 1
    if size_y % 2 == 0:
        size_y = size_y + 1

    matrix = create_empty_matrix(size_x, size_y)

    for point in point_list:
        x = int(point[0])
        y = int(point[1])
        matrix[x][y] = 1

    return matrix

def fold_data_x(matrix, fold_row):

    size = get_matrix_size(matrix)
    fold_line_x = int(fold_row)

    new_matrix = create_empty_matrix(fold_line_x, size[1])

    for y in range(size[1]):
        for x in range(fold_line_x+1):
            val1 = matrix[fold_line_x - x][y]
            val2 = matrix[fold_line_x + x][y]
            if val1 > 0 or val2 > 0:
                new_matrix[ fold_line_x - x][y] = 1
        
    return new_matrix

def fold_data_y(matrix, fold_line):

    size = get_matrix_size(matrix)
    fold_line_y = int(fold_line)

    new_matrix = create_empty_matrix(size[0],fold_line_y)

    for x in range(size[0]):
        for y in range(fold_line_y + 1):

            val1 = 0
            if fold_line_y - y >= 0:
                val1 = matrix[x][fold_line_y - y]

            val2 = 0
            if fold_line_y + y < size[1]:
                val2 = matrix[x][fold_line_y + y]

            if val1 > 0 or val2 > 0:
                new_matrix[x][fold_line_y-y] = 1

    return new_matrix

def load_point_list(filename):
    file_data = loadfile(filename)
    decoded_data = decode_data(file_data)
    return decoded_data

def fold_paper(matrix, fold_list, stop_on_first):
    for fold in fold_list:
        fold_rule = fold.split("=")
        fold_axis = fold_rule[0].strip("fold along ")
        if fold_axis == "x":
            matrix = fold_data_x(matrix,fold_rule[1])
        elif fold_axis == "y":
            matrix = fold_data_y(matrix,fold_rule[1])
        else:
            print_error("Unknown fold : " + fold_axis)
        
        if stop_on_first:
            break

    return matrix

def count_markers(matrix):
    num_cells = 0
    size = get_matrix_size(matrix)
    for y in range(size[1]):
        for x in range(size[0]):
            val = matrix[x][y]
            if val > 0:
                num_cells = num_cells + int(val)
    return num_cells

#
# Fold paper
#
def fold_paper_base(filename, stop_on_first):
    data = load_point_list(filename)
    matrix = pointlist_to_matrix(data[0])
    matrix = fold_paper(matrix, data[1], stop_on_first)
    return matrix

def fold_paper_first(filename):
    matrix = fold_paper_base(filename, True)
    return count_markers(matrix)

def fold_paper_full(filename):
    matrix = fold_paper_base(filename, False)
    return count_markers(matrix)

# Run unitests
unittest(fold_paper_first,17,"transparent_origami_data_example1.txt")
unittest(fold_paper_full,16,"transparent_origami_data_example1.txt")
unittest(fold_paper_first,602,"transparent_origami_data.txt")
unittest(fold_paper_full,92,"transparent_origami_data.txt")

# Run actual code
matrix = fold_paper_base("transparent_origami_data.txt", False)
print_matrix_color("Code:", matrix, 0, bcolors.DARK_GREY)

