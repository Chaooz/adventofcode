
#
# Load file
#

import sys
sys.path.insert(1, '../Libs')
from advent_libs import *

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

    matrix = createMatrix(filename)

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
def unittest_loops(steps, result, filename):
    code_res = run_code_loops(steps, filename,False)
    if code_res == result:
        print(bcolors.OKGREEN + "[OK]    Unittest loops " + filename + " with " + str(steps) + " steps is OK! " + bcolors.RESET)
    else:
        print(bcolors.WARNING + "[ERROR] Unittest loops " + filename + " with " + str(steps) + " steps is NOT OK! Got:" + str(code_res) + " Expected:" + str(result) + bcolors.RESET)

def unittest_allflash(needed_steps, filename):
    code_res = run_code_loops(10000, filename, True)
    if code_res == needed_steps:
        print(bcolors.OKGREEN + "[OK]    Unittest allflash " + filename + " with " + str(needed_steps) + " steps is OK! " + bcolors.RESET)
    else:
        print(bcolors.WARNING + "[ERROR] Unittest allflash " + filename + " with " + str(needed_steps) + " steps is NOT OK! Got:" + str(code_res) + " Expected:" + str(needed_steps) + bcolors.RESET)


#
# Main code
#

# Test algorithm for examples in challenge
unittest_loops(1,9, "dumbo_octopus_data_unittest_small.txt")
unittest_loops(2,9, "dumbo_octopus_data_unittest_small.txt")
unittest_loops(10,204, "dumbo_octopus_data_unittest_large.txt")
unittest_loops(100,1656, "dumbo_octopus_data_unittest_large.txt")

# Testing result of puzzle part 1
unittest_loops(100,1749, "dumbo_octopus_data_puzzle.txt")

# From example on webpage
unittest_allflash(195,"dumbo_octopus_data_unittest_large.txt")

# Run actual program
res = run_code_loops(100,"dumbo_octopus_data_puzzle.txt", False)
print("Puzzle #1 : Number of flashes after 100 loops = " + str(res))

res_allflash = run_code_loops(10000,"dumbo_octopus_data_puzzle.txt", True)
print("Puzzle #2 : Number of loops for all to flash at the same time = " + str(res_allflash))
