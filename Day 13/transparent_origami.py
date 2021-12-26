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

    print(max_point)
    matrix = create_empty_matrix(size_x, size_y)
#    print_matrix("empty", matrix)

    for point in point_list:
        x = int(point[0])
        y = int(point[1])
        matrix[x][y] = 1

    #print_matrix("initial", matrix)

    return matrix

def fold_data_x(matrix, fold_row):

    size = get_matrix_size(matrix)
    fold_line_x = int(fold_row)
    new_matrix = create_empty_matrix(fold_line_x, size[1])

    for x in range(fold_line_x):
        for y in range(size[1]):
            val1 = matrix[x][y]
            val2 = matrix[size[0] - x - 1][y]
            if val1 > 0 or val2 > 0:
                new_matrix[x][y] = 1

    markers = count_markers(new_matrix)
    print("Fold x : " + str(fold_row) + " =>  " + str(markers))

    #print_matrix("fold_x (at " + str(fold_row) + ")", new_matrix)
    return new_matrix

def fold_data_y(matrix, fold_line):

    size = get_matrix_size(matrix)
    fold_line_y = int(fold_line)
    new_matrix = create_empty_matrix(size[0],fold_line_y)

    for x in range(size[0]):
        for y in range(fold_line_y):
            val1 = matrix[x][y]
            val2 = matrix[x][size[1] - y - 1]
            if val1 > 0 or val2 > 0:
                new_matrix[x][y] = 1

    markers = count_markers(new_matrix)
    print("Fold y : " + str(fold_line) + " =>  " + str(markers))
    #print_matrix("fold_y (at " + str(fold_line) + ")", new_matrix)

    return new_matrix

def fold_first(data, folds):
    for fold in folds:
        fold_rule = fold.split("=")
        fold_axis = fold_rule[0].strip("fold along ")
        if fold_axis == "x":
            data = fold_data_x(data,fold_rule[1])
        else:
            data = fold_data_y(data,fold_rule[1])
        #print_matrix("fold first", data)

        return data

def fold_everything(data, folds):
    for fold in folds:
        fold_rule = fold.split("=")
        fold_axis = fold_rule[0].strip("fold along ")
        if fold_axis == "x":
            data = fold_data_x(data,fold_rule[1])
        else:
            data = fold_data_y(data,fold_rule[1])
    return data

def count_markers(matrix):
    num_cells = 0
    size = get_matrix_size(matrix)
    for y in range(size[1]):
        for x in range(size[0]):
            val = matrix[x][y]
            if val > 0:
                num_cells = num_cells + 1
    return num_cells

#
# Fold paper
#
def fold_paper_first(filename):
    file_data = loadfile(filename)
    data = decode_data(file_data)

    matrix = pointlist_to_matrix(data[0])
    matrix = fold_first(matrix, data[1])
    return count_markers(matrix)

def fold_paper_second(filename):
    file_data = loadfile(filename)
    data = decode_data(file_data)

    matrix = pointlist_to_matrix(data[0])
    markers = count_markers(matrix)
    print("Initial : " + str(markers))

    matrix = fold_everything(matrix, data[1])
    return count_markers(matrix)

unittest(fold_paper_first,17,"transparent_origami_data_example1.txt")
unittest(fold_paper_first,735,"transparent_origami_data.txt")
unittest(fold_paper_second,16,"transparent_origami_data.txt")
