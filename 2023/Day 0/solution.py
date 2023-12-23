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
print_color("Day 0: Template", bcolors.OKGREEN)
print("")

def solvePuzzle1(filename):
    sum = 0
    lines = loadfile(filename)
    return sum

def solvePuzzle2(filename):
    sum = 0
    matrix  = Matrix.CreateFromFile(filename, ".")

    colorList = list()
    colorList.append(("O", bcolors.WHITE))
    colorList.append(("#", bcolors.DARK_GREY))
    matrix.PrintWithColor(colorList, bcolors.DARK_GREY , " ", "")

    return sum

unittest(solvePuzzle1, 0, "unittest1.txt")     
unittest(solvePuzzle1, 0, "input.txt")     

unittest(solvePuzzle2, 0, "unittest2.txt")
unittest(solvePuzzle2, 0, "input.txt")     

