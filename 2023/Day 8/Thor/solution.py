#!/usr/local/bin/python3
# https://adventofcode.com/2023/day/8

import sys
import math

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_vector2 import *
from advent_libs_matrix import *

setupCode("Day 8: Haunted Wasteland")

def read_input(filename:str) -> list:
    lines = loadfile(filename)

    instructions = ""
    path_map = {}

    for line in lines:
        line = line.replace("\n", "")
        line = line.replace("(","")
        line = line.replace(")","")

        if len(line) == 0:
            continue

        if ( line.find("=") > - 1):
            name, path = line.split("=")
            path_map[name.strip()] = [ x.strip() for x in path.split(",") ]
        else:
            instructions = line

    return path_map, instructions

def path_nodes(path_map:dict, instructions:str, start_list:list, end:str) -> int:
    index = 0
    sum = 0

    num_steps = list()

    while True:
        sum += 1
        char = instructions[index]

        new_start_list = []
        num_at_end = 0
        for start in start_list:
            path = path_map[start]

            if char == "L":
                start = path[0]
            elif char == "R":
                start = path[1]

            # If this path is at the end
            if start.endswith(end):
                num_at_end += 1
                num_steps.append(sum)
            else:
                # Not at end, so add to new start list
                new_start_list.append(start)

        # All start nodes are at the end
        if len(new_start_list) == 0:
            # print(num_steps)
            # Math.LCM finds number where multiple of them ends up the same
            # F.ex : 2 and 3 returns 6 because 2+2+2 = 3+3 = 6
            return math.lcm(*num_steps)
        
        # New start node list
        start_list = new_start_list

        # Make sure the index does not overflow, just start at the beginning
        index += 1
        index = index % len(instructions)

    print("ERROR: invalid path ")
    return 0

def solvePuzzle1(filename:str):
    path_map, instructions = read_input(filename)
    start_list = ["AAA"]

    sum = path_nodes(path_map, instructions, start_list, "ZZZ")
    return sum

def solvePuzzle2(filename:str):
    path_map, instructions = read_input(filename)

    start_list = []
    for path in path_map:
        if path[2] == "A":
            start_list.append(path)

    sum = path_nodes(path_map, instructions, start_list, "Z")
    return sum

unittest(solvePuzzle1, 2, "unittest1.txt")
unittest(solvePuzzle1, 6, "unittest2.txt")
unittest(solvePuzzle2, 6, "unittest3.txt")

runCode(8,solvePuzzle1, 17621, "input.txt")     
runCode(8,solvePuzzle2, 20685524831999, "input.txt")
