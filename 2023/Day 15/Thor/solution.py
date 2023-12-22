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
print_color("Day 15: Lens Library", bcolors.OKGREEN)
print("")

def get_hash_value(string) -> int:
    value = 0
    for char in string:
        value += int(ord(char))
        value *= 17
        value %= 256

    return value

def print_all_boxes(boxes, operation):
    print("------ ", operation, " ------")
    for i in range(0,256):
        lence_list = boxes[i]
        if lence_list != []:
            print(lence_list)

def solvePuzzle1(filename):
    lines = loadfile(filename)
    blocks = lines[0].split(",")
    sum = 0
    for block in blocks:
        sum += get_hash_value(block)
    return sum

def solvePuzzle2(filename):
    lines = loadfile(filename)
    blocks = lines[0].split(",")
    sum = 0
    boxes = {}

    # Init boxlist
    for i in range(0,256):
        boxes[i] = list()

    for block in blocks:
        operation = "="
        if block.find("-") != -1:
            operation = "-"

        label, value = block.split(operation)
        box_number = get_hash_value(label)
        lence_list = boxes[box_number]

        if operation == "-":
            # Add all entries except the one with the value
            boxes[box_number] = [lence for lence in lence_list if lence[0] != label]
#            print_all_boxes(boxes, block)
        else:
            updated = False
            for lence in lence_list:
                if lence[0] == label:
                    lence[1] = int(value)
                    updated = True
                    break
            if updated == False:
                # Add new entry
                boxes[box_number].append([label, int(value)])

#            print_all_boxes(boxes, block)



    for box_number in range(0,256):
        lens_list = boxes[box_number]
        if lens_list != []:
            for lens_index in range(0,len(lens_list)):
                lens = lens_list[lens_index]
                slot_number = lens_index + 1
                focal_length = lens[1]
                focus_power = (box_number + 1) * slot_number * focal_length
#                print("Box:", (box_number +1), " * slot number:", slot_number, " * focal length:", focal_length, " = Focus Power:", focus_power)
                sum += focus_power

    return sum

unittest(solvePuzzle1, 1320, "unittest1.txt")     
unittest(solvePuzzle1, 517315, "input.txt")     

unittest(solvePuzzle2, 145, "unittest1.txt")
unittest(solvePuzzle2, 247763, "input.txt")     

