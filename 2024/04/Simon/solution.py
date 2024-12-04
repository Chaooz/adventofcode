#!/usr/lib/python3
"""
    Description: Script to solve the Advent of Code 2024 Day 4 puzzle

    Returns:
        str: The solution to the puzzle
"""
import sys
sys.path.insert(1, '../../../Libs')
from advent_libs_matrix import *

expected_result_1 = 18
expected_result_2 = 9

directions = [
    Vector2(1,0),  # Right
    Vector2(0,1),  # Down
    Vector2(1,1),  # Down right
    Vector2(-1,1), # Down left
    Vector2(1,-1), # Up right
    Vector2(-1,-1),# Up left
    Vector2(0,-1), # Up
    Vector2(-1,0)   # Left
]

directions2 = [
    Vector2(1,1),  # Down right
    Vector2(-1,1), # Down left
    Vector2(1,-1), # Up right
    Vector2(-1,-1),# Up left
]

def find_word(matrix, start_point:tuple, direction:Vector2, word):
    for i in range(0,len(word)):
        xx = start_point[0] + i * direction.x
        yy = start_point[1] + i * direction.y
        if xx < 0 or yy < 0 or xx >= matrix.sizeX or yy >= matrix.sizeY:
            return 0
        if matrix.Get(xx,yy) != word[i]:
            return 0
    return 1

def find_cross(matrix, start_point:tuple):
    global directions2
    
    for direction in directions2:
        xx = start_point[0] + direction.x
        yy = start_point[1] + direction.y

        if xx < 0 or yy < 0 or xx >= matrix.sizeX or yy >= matrix.sizeY:
            return 0
            
    up_left = matrix.Get(start_point[0] -1,start_point[1] -1)
    down_right = matrix.Get(start_point[0] +1,start_point[1] +1)
    down_right = matrix.Get(start_point[0] +1,start_point[1] +1)
    up_right = matrix.Get(start_point[0] -1,start_point[1] +1)
    down_left = matrix.Get(start_point[0] +1,start_point[1] -1)        
    if up_left == "S" and down_right == "M" or up_left == "M" and down_right == "S":
        if up_right == "M" and down_left == "S" or up_right == "S" and down_left == "M":
            return 1
        else:
            return 0
    else:
        return 0
        
def solve_puzzle_1(filename):
    total = 0
    matrix = Matrix.CreateFromFile(filename,".")

    # Loop through all points to find X
    xList = []
    for x in range(0,matrix.sizeX):
        for y in range(0,matrix.sizeY):
            if matrix.Get(x,y) == "X":
                xList.append((x,y))

    # For all location of Xes find the word XMAS in a given direction
    for point in xList:
        for direction in directions:
            total += find_word(matrix, point, direction, "XMAS")
    return total

def solve_puzzle_2(filename):
    total = 0
    matrix = Matrix.CreateFromFile(filename,".")

    # Loop through all points to find A
    a_list = []
    for x in range(0,matrix.sizeX):
        for y in range(0,matrix.sizeY):
            if matrix.Get(x,y) == "A":
                a_list.append((x,y))

    # For all location of Ms find the word MAST in a given direction
    for point in a_list:
        total += find_cross(matrix, point)
    return total

if solve_puzzle_1("sample_input.txt") == expected_result_1:
    print(f"Test 1 Passed. The result matched the expected result of {expected_result_1}")
    print(f"Solution to puzzle part 1 is {solve_puzzle_1('input.txt')}")
else:
    print(f"Test 1 Failed. The result did not match the expected result of {expected_result_1}")
    
if solve_puzzle_2("sample_input_2.txt") == expected_result_2:
    print(f"Test 2 Passed. The result matched the expected result of {expected_result_2}")
    print(f"Solution to puzzle part 2 is {solve_puzzle_2('input.txt')}")
else:
    print(f"Test 2 Failed. The result ({solve_puzzle_2('sample_input_2.txt')} did not match the expected result of {expected_result_2}")
