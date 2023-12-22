#!/usr/local/bin/python3
# https://adventofcode.com/2023/day/2

import sys
import math

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_vector2 import *
from advent_libs_matrix import *

print("")
print_color("Day 14: Parabolic Reflector Dish", bcolors.OKGREEN)
print("")

def next_free_up(matrix:Matrix, x, y):
    while y > 0:
        y -= 1
        if matrix.Get(x, y) != ".":
            return y + 1
    return y

def roll_stones_up(matrix:Matrix):
    for x in range(0, matrix.sizeX):
        for y in range(1, matrix.sizeY):
            if matrix.Get(x, y) == "O":
                yy = next_free_up(matrix, x, y)
                if yy != y:
                    matrix.Set(x,y,".")
                    matrix.Set(x,yy,"O")

def matrix_rotate_left(matrix:Matrix):
    newMatrix = Matrix(matrix.name, matrix.sizeY, matrix.sizeX, "." )
    for y in range(0, matrix.sizeY):
        for x in range(0, matrix.sizeX):
            newMatrix.Set(y, matrix.sizeX - x - 1, matrix.Get(x, y))
    return newMatrix

def matrix_rotate_right(matrix:Matrix):
    newMatrix = Matrix(matrix.name, matrix.sizeY, matrix.sizeX, "." )
    for y in range(0, matrix.sizeY):
        for x in range(0, matrix.sizeX):
            newMatrix.Set(matrix.sizeY - y - 1, x, matrix.Get(x, y))
    return newMatrix

def calc_weight(matrix:Matrix):
    sum = 0
    for y in range(0, matrix.sizeY):
        for x in range(0, matrix.sizeX):
            if matrix.Get(x, y) == "O":
                sum += matrix.sizeY - y
    return sum

#
# Return a number that is unique for the matrix pattern
#
def get_matrix_pattern(matrix:Matrix):
    sum = 0
    for y in range(0, matrix.sizeY):
        for x in range(0, matrix.sizeX):
            if matrix.Get(x, y) == "O":
                sum += (x + 1) + ((y + 1)*100)
    return sum

def solvePuzzle1(filename):
    matrix  = Matrix.CreateFromFile(filename, ".")
    roll_stones_up(matrix)
    return calc_weight(matrix)

def showRotate(filename):
    colorList = list()
    colorList.append(("O", bcolors.WHITE))
    colorList.append(("#", bcolors.DARK_GREY))

    matrix  = Matrix.CreateFromFile(filename, ".")
    matrix.PrintWithColor(colorList, bcolors.DARK_GREY , " ", " ")
    matrix = matrix_rotate_left(matrix)
    matrix.PrintWithColor(colorList, bcolors.DARK_GREY , " ", " ")
    matrix = matrix_rotate_right(matrix)
    matrix.PrintWithColor(colorList, bcolors.DARK_GREY , " ", " ")

    return 0

def solvePuzzle2(filename):
    matrix  = Matrix.CreateFromFile(filename, ".")

    # Just run some iterations to get the stones rolling
    startIterations = 200
    for i in range(0,startIterations):
        for j in range(0,4):
            roll_stones_up(matrix)
            matrix = matrix_rotate_right(matrix)

    # Just roll the stones and try to find a cycle pattern
    weight_list = list()
    matrix_pattern_list = list()
    for i in range(0,200):

        # Roll the stones up and rotate the matrix
        for j in range(0,4):
            roll_stones_up(matrix)
            matrix = matrix_rotate_right(matrix)

        weight = calc_weight(matrix)
        matrix_pattern = get_matrix_pattern(matrix)

        # If we have this unique pattern before, we have found a cycle
        if matrix_pattern in matrix_pattern_list:
            # Index where the pattern was found before
            j = matrix_pattern_list.index(matrix_pattern)
            # Pattern length
            cycle_length = i - j
            q = (1000000000 - startIterations - i - 1) % cycle_length
            n = (q+j) % cycle_length
            return weight_list[n]
        
        # Pattern not found so add it to the list and try next
        weight_list.append(weight)
        matrix_pattern_list.append(matrix_pattern)

#    colorList = list()
#    colorList.append(("O", bcolors.WHITE))
#    colorList.append(("#", bcolors.DARK_GREY))
#    matrix.PrintWithColor(colorList, bcolors.DARK_GREY , " ", "")

    # Should never happen
    return 0

unittest(solvePuzzle1, 136, "unittest1.txt")     
unittest(solvePuzzle1, 110128, "input.txt")     

#unittest(showRotate, 64, "unittest1.txt")

unittest(solvePuzzle2, 64, "unittest1.txt")
unittest(solvePuzzle2, 103861, "input.txt")
