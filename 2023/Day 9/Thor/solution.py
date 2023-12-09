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
print_color("Day 9: Mirage Maintenance", bcolors.OKGREEN)
print("")

def are_all_equal(list:list) -> bool:
    # All numbers are the same ?
    for index in range(1, len(list)):
        if list[index] != list[0]:
            return False
    return True


def find_next_extrapolated_number(nodes:list) -> int:
    new_nodes = []
    for index in range(1, len(nodes)):
        a = nodes[index]
        b = nodes[index - 1]
        diff = int(a) - int(b)
        new_nodes.append(diff)

    last_number = int(nodes[len(nodes) - 1])
    if are_all_equal(new_nodes):
        next_number = last_number + int(new_nodes[0])
        return next_number
    else:
        last_number += find_next_extrapolated_number(new_nodes)
        return last_number

def find_previous_extrapolated_number(nodes:list) -> int:
    new_nodes = []
    for index in range(1, len(nodes)):
        a = nodes[index]
        b = nodes[index - 1]
        diff = int(a) - int(b)
        new_nodes.append(diff)

    first_number = int(nodes[0])
    if are_all_equal(new_nodes):
        next_number = first_number - int(new_nodes[0])
        return next_number
    else:
        first_number -= find_previous_extrapolated_number(new_nodes)
        return first_number

def find_extrapolated_line(line:str):
    nodes = [ x.strip() for x in line.split(" ")]
    return find_next_extrapolated_number(nodes)

def find_extrapolated_line_reverse(line:str):
    nodes = [ x.strip() for x in line.split(" ")]
    return find_previous_extrapolated_number(nodes)

def solvePuzzle1(filename:str):
    sum = 0
    lines = loadfile(filename)
    for line in lines:
        line = line.replace("\n", "")
        nodes = [ x.strip() for x in line.split(" ")]
        sum += find_next_extrapolated_number(nodes)
    return sum

def solvePuzzle2(filename:str):
    sum = 0
    lines = loadfile(filename)
    for line in lines:
        line = line.replace("\n", "")
        nodes = [ x.strip() for x in line.split(" ")]
        sum += find_previous_extrapolated_number(nodes)
    return sum

unittest(find_extrapolated_line, 18, "0 3 6 9 12 15")

unittest(solvePuzzle1, 114, "unittest1.txt")
unittest(solvePuzzle1, 1853145119, "input.txt")     

unittest(find_extrapolated_line_reverse, 5, "10 13 16 21 30 45")
unittest(solvePuzzle2, 923, "input.txt")
