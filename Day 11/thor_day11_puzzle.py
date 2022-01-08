
#
# Load file
#

import sys
sys.path.insert(1, '../Libs')
from advent_libs import *
from advent_libs_matrix import *

# Flash blocks
def flash_block(x,y, size_x, size_y, matrix, visited_matrix):
    if x >= 0 and y >= 0 and x < size_x and y < size_y:
        visited = visited_matrix[x][y]

        # Only visit this block once
        if visited == 0:

            # Increase block value
            value = matrix[x][y]
            matrix[x][y] = value + 1

            # Block flashes, flash all around as well
            if value >= 9:
                visited_matrix[x][y] = 1
                flash_block( x - 1, y - 1, size_x, size_y, matrix,visited_matrix )
                flash_block( x, y - 1, size_x, size_y, matrix,visited_matrix )
                flash_block( x + 1, y - 1, size_x, size_y, matrix,visited_matrix )
                flash_block( x - 1, y, size_x, size_y, matrix,visited_matrix )
                flash_block( x + 1, y, size_x, size_y, matrix,visited_matrix )
                flash_block( x - 1, y + 1, size_x, size_y, matrix,visited_matrix )
                flash_block( x, y + 1, size_x, size_y, matrix,visited_matrix )
                flash_block( x + 1, y + 1, size_x, size_y, matrix,visited_matrix )

def increase_all_blocks(size_x, size_y, matrix):
    for y in range(size_y):
        for x in range(size_x):
            value = matrix[x][y]
            matrix[x][y] = value + 1

def reset_all_flashed_blocks(size_x, size_y, matrix):
    for y in range(size_y):
        for x in range(size_x):
            value = matrix[x][y]
            if value > 9:
                matrix[x][y] = 0

def count_reset_blocks(size_x, size_y, matrix):
    num_reset_blocks = 0
    for y in range(size_y):
        for x in range(size_x):
            value = matrix[x][y]
            if value == 0:
                num_reset_blocks = num_reset_blocks + 1
    return num_reset_blocks

#
# Run our code
#
def run_code_loops(steps, filename, exit_on_allflash):

    matrix = create_matrix_from_file(filename)

    size_y = int(len(matrix))
    size_x = int(len(matrix[0]))

    #print_matrix("Before run", matrix)

    num_resets = 0
    for step in range(steps):
        increase_all_blocks(size_x,size_y, matrix)
        visited_matrix = create_empty_matrix(size_x,size_y)

        for y in range(size_y):
            for x in range(size_x):
                #visited = visited_matrix[x][y]
                value = matrix[x][y]
                if value > 9:
                    flash_block(x,y, size_x, size_y, matrix, visited_matrix)

        reset_all_flashed_blocks(size_x, size_y, matrix)
        resets = count_reset_blocks(size_x, size_y, matrix)
        num_resets =  num_resets + resets

        if exit_on_allflash and resets == size_x * size_y:
            #print_matrix("After run #" + str(step),matrix)
            return step + 1

    #print_matrix("After run #" + str(resets),matrix)
    return num_resets

#
# Run code examples through our test to make sure the code runs ok
# 

def run_puzzle1(filename,steps):
    return run_code_loops(steps, filename, False)

def run_puzzle2(filename):
    return run_code_loops(10000, filename, True)

#
# Main code
#

# Test algorithm for examples in challenge
unittest_input(run_puzzle1,1,9, "day11_data_unittest_small.txt")
unittest_input(run_puzzle1,2,9, "day11_data_unittest_small.txt")
unittest_input(run_puzzle1,10,204, "day11_data_unittest_large.txt")
unittest_input(run_puzzle1,100,1656, "day11_data_unittest_large.txt")
unittest(run_puzzle2,195,"day11_data_unittest_large.txt")

# Unittest actual data
unittest_input(run_puzzle1,100,1749, "thor_day11_data.txt")
unittest(run_puzzle2,285,"thor_day11_data.txt")

# Run actual program
res = run_puzzle1("thor_day11_data.txt", 100)
print("Puzzle #1 : Number of flashes after 100 loops = " + str(res))

res_allflash = run_puzzle2("thor_day11_data.txt")
print("Puzzle #2 : Number of loops for all to flash at the same time = " + str(res_allflash))
