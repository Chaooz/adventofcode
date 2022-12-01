#!/usr/lib/python3

import sys

# Import custom libraries
sys.path.insert(1, '../../Libs')
from advent_libs import *

#
# Figure out which block contains most calories
# 
def get_elfs_with_calories(filename):
    lines = loadfile(filename)

    # Count calories
    caleries = 0
    elfs = []
    for line in lines:
        if line == "\n":
            elfs.append(caleries)
            caleries = 0
        else:
            caleries += int(line)

    elfs.append(caleries)
    return elfs

# 
# Return the calorie count for the top 3 elfs
#
def topElfsFoodLoad(filename, numElfs):
    elfs = get_elfs_with_calories(filename)

    # Sort the list
    elfs.sort(reverse=True)

    # Count the calories for the top X elfs
    maxCalories = 0
    for index in range(numElfs):
        maxCalories += elfs[index]
        
    return maxCalories

# Unittests for the data
unittest( get_elfs_with_calories, [6000,4000,11000,24000,10000], "unittest_example1.txt")
unittest_input( topElfsFoodLoad, 1, 24000, "unittest_example1.txt")
unittest_input( topElfsFoodLoad, 3, 45000, "unittest_example1.txt")

# Run puzzles
result1 = topElfsFoodLoad("puzzleinput.txt", 1)
result2 = topElfsFoodLoad("puzzleinput.txt", 3)

print_ok("Thor: Puzzle1 = " + str(result1))
print_ok("Thor: Puzzle2 = " + str(result2))