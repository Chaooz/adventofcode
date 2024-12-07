#!/usr/lib/python3
"""
    Description: Script to solve the Advent of Code 2024 Day 5 puzzle

    Returns:
        str: The solution to the puzzle
"""
import sys
import re
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_matrix import *

expected_result_1 = 41
expected_result_2 = 6

vector_list = [ 
    Vector2(0,-1),
    Vector2(1,0),
    Vector2(0,1),
    Vector2(-1,0)
]

def movement_in_direction(new_direction:int) -> Vector2:
    if new_direction == 0:
        return Vector2(0,-1) # North
    elif new_direction == 1:
        return Vector2(1,0) # East
    elif new_direction == 2:
        return Vector2(0,1)
    elif new_direction == 3:
        return Vector2(-1,0)


def findPath(matrix:Matrix, current_position:Vector2):
#    directions = ["N", "E", "S", "W"]
    current_direction_index = 0
#    current_direction_value = directions[current_direction_index]
    out_of_bounds = False
    visited_points = []

    while True:
        #direction_vector = movement_in_direction(current_direction_value)
        direction_vector = movement_in_direction(current_direction_index)
        new_position = current_position + direction_vector

        # Check if we are outside of matrix                       
        if matrix.IsOutOfBounds(new_position):
            return visited_points

        data = matrix.GetPoint(new_position)
        if data == "#":
            # Turn and stuff
            current_direction_index = (current_direction_index + 1) % 4
#            current_direction_value = directions[current_direction_index]

        else:
            current_position = new_position

            # Add newPositon into list
            position_and_direction = (current_position, current_direction_index)
            if position_and_direction not in visited_points:
                visited_points.append(position_and_direction)
            else:
                # LOOOOP
                return None

    return visited_points    

def checkPath(matrix:Matrix, current_position:Vector2):
    current_direction_index = 0
    out_of_bounds = False
    visited_points = []

    while True:
        direction_vector = movement_in_direction(current_direction_index)
        new_position = current_position + direction_vector

        # Check if we are outside of matrix                       
        if matrix.IsOutOfBounds(new_position):
            return visited_points

        data = matrix.GetPoint(new_position)
        if data == "#":
            # Turn and stuff
            current_direction_index = (current_direction_index + 1) % 4

            # Add newPositon into list
            position_and_direction = (current_position, current_direction_index)
            if position_and_direction not in visited_points:
                visited_points.append(position_and_direction)
            else:
                # LOOOOP
                return None

        else:
            current_position = new_position

def move_through_room(filename:str):
    matrix = Matrix.CreateFromFile(filename,".")
    current_position = matrix.FindFirst("^")
    visited_points = findPath(matrix,current_position)

    # Make the list with unique points
    unique_visited_points = []
    for postion,direction in visited_points:
        if postion not in unique_visited_points:
            unique_visited_points.append(postion)

    return len(unique_visited_points)

def create_loopy_guard(filename:str):
    matrix = Matrix.CreateFromFile(filename,".")
    guard_start_position = matrix.FindFirst("^")
    visited_points = findPath(matrix, guard_start_position)
    
    unique_obsticles = []
    run_cycles = 0
    sum = 0
    for index in range(1,len(visited_points)):
        run_cycles = run_cycles + 1
        if run_cycles % 100 == 0:
            print("run cycle", run_cycles)

        visited_position_value = visited_points[index][0]

        if matrix.GetPoint(visited_position_value) != ".":
            continue

        matrix.SetPoint(visited_position_value, "#")
        new_path = checkPath(matrix, guard_start_position)
        matrix.SetPoint(visited_position_value, ".")

        # We detected a loop!
        if new_path == None:
            sum += 1
            if visited_position_value not in unique_obsticles:
                unique_obsticles.append(visited_position_value)

    return len(unique_obsticles)

test_result_1 = move_through_room("sample_input.txt")
test_result_2 = create_loopy_guard("sample_input.txt")

if test_result_1 == expected_result_1:
    print("Test 1 passed")
    print("The number of visited points is: ", move_through_room("input.txt"))
else:
    print(f"Test 1 failed. The returned value was {test_result_1}")
    
if test_result_2 == expected_result_2:
    print("Test 2 passed")
    print("The number of loops is: ", create_loopy_guard("input.txt"))
else:
    print(f"Test 2 failed. The returned value was {test_result_2}")