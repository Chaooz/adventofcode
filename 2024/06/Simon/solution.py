#!/usr/lib/python3
"""
    Description: Script to solve the Advent of Code 2024 Day 5 puzzle

    Returns:
        str: The solution to the puzzle
"""
import sys, re
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_matrix import *

expected_result_1 = 41
expected_result_2 = 6

vector_list = [ 
    Vector2(0,-1),
    Vector2(0,1),
    Vector2(1,0),
    Vector2(-1,0)
]

def movement_in_direction(new_direction:str) -> Vector2:
    match new_direction:
        case "N":
            return Vector2(0,-1)
        case "S":
            return Vector2(0,1)
        case "E":
            return Vector2(1,0)
        case "W":
            return Vector2(-1,0)

def findPath(matrix:Matrix, current_position:Vector2):
    directions = ["N", "E", "S", "W"]
    current_direction_index = 0
    current_direction_value = directions[current_direction_index]
    out_of_bounds = False
    visited_points = []

    while not out_of_bounds:
        direction_vector = movement_in_direction(current_direction_value)
        #direction_vector = vector_list[current_direction_index]
        new_position = current_position + direction_vector

        # Check if we are outside of matrix                       
        if matrix.IsOutOfBounds(new_position):
            out_of_bounds = True
            break

        data = matrix.GetPoint(new_position)
        if data == "#":
            # Turn and stuff
            current_direction_index = (current_direction_index + 1) % 4
            current_direction_value = directions[current_direction_index]
        else:
            current_position = new_position
            position_and_direction = (current_position, current_direction_value)

            # Add newPositon into list
            if position_and_direction not in visited_points:
                visited_points.append(position_and_direction)
            else:
                # LOOOOP
                return None

    return visited_points    

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
    for index in range(1,len(visited_points)):
        run_cycles = run_cycles + 1
        if run_cycles % 100 == 0:
            print("run cycle", run_cycles)

        visited_position_value = visited_points[index][0]

        matrix.SetPoint(visited_position_value, "#")
        new_path = findPath(matrix, guard_start_position)
        matrix.SetPoint(visited_position_value, ".")

        # We detected a loop!
        if new_path == None:
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