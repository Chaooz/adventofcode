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
print_color("Day 13: Point of Incidence", bcolors.OKGREEN)
print("")

def SetBit(number, bit):
    return number | ( 1 << bit )

# function to check if x is power of 2
def isPowerOfTwo( x ):
 
    # First x in the below expression is
    # for the case when x is 0
    return x and (not(x & (x - 1)))
 
# function to check whether the two numbers
# differ at one bit position only
def differAtOneBitPos( a , b ):
    return isPowerOfTwo(a ^ b)

def is_mirror(mirror_list:list, line:int, check_bit:bool):

    mirror_once = True
    for i in range(1,line):

        aa = line - i-1
        bb = line + i

        if aa < 0 or bb >= len(mirror_list):
            return True

        a = mirror_list[line - i - 1]
        b = mirror_list[line + i]
        if check_bit == False and a != b:
            return False
        elif check_bit == True and a != b:
            if mirror_once and differAtOneBitPos(a,b):
                mirror_once = False
            else:
                print("IsMirror false [2]:", line, a,b, i, mirror_list)
                return False

    return check_bit != mirror_once

def mirror_value(mirror_list:list, check_bit:bool) -> int:
#    print("Find mirror value")
    line = 0
    for i in range(1,len(mirror_list)):
        a = mirror_list[i-1]
        b = mirror_list[i]
        if check_bit == False and a == b and is_mirror(mirror_list,i, False):
            line = i
            return i
        elif check_bit == True and a!=b and differAtOneBitPos(a,b):
            if is_mirror(mirror_list,i, False):
                line = i
                return i
        elif check_bit == True and a==b:
            if is_mirror(mirror_list,i, True):
                line = i
                return i
    return line
#    return abs(len(mirror_list) - line * 2)

def mirror_rows(matrix:Matrix, check_bit:bool) -> int:
    number_list = list()
    for y in range(0,matrix.sizeY):
        number = 0
        for x in range(0,matrix.sizeX):
            if ( matrix.Get(x,y) == "#"):
                number = SetBit(number, x)
        number_list.append(number)
    return mirror_value(number_list, check_bit)

def mirror_columns(matrix:Matrix, check_bit:bool) -> int:
    number_list = list()
    for x in range(0,matrix.sizeX):
        number = 0
        for y in range(0,matrix.sizeY):
            if ( matrix.Get(x,y) == "#"):
                number = SetBit(number, y)
        number_list.append(number)
    return mirror_value(number_list, check_bit)

def mirror_matrix(matrix:Matrix, check_bit:bool) -> int:
    number_list = list()
    for x in range(0,matrix.sizeX):
        number = 0
        for y in range(0,matrix.sizeY):
            if ( matrix.Get(x,y) == "#"):
                number = SetBit(number, y)
        number_list.append(number)
    sum1,check_bit = mirror_value(number_list, check_bit)

    number_list.clear()
    for y in range(0,matrix.sizeY):
        number = 0
        for x in range(0,matrix.sizeX):
            if ( matrix.Get(x,y) == "#"):
                number = SetBit(number, x)
        number_list.append(number)
    sum2, check_bit = mirror_value(number_list, check_bit)

    return sum1 + sum2 * 100


def solveInternal(filename:str, check_bit:bool):
    sum = 0

    lines = loadfile(filename)

    # Group lines
    mirror = list()
    for line in lines:
        if line == "":
            matrix = Matrix.CreateFromList(filename, mirror, ".")
#            sum += mirror_matrix(matrix, check_bit)
            col = mirror_columns(matrix, check_bit)
            sum += col
#            if col == 0:
            row = mirror_rows(matrix, check_bit)
            sum += row * 100
#                if row == 0:
#                    print("FOUND NO MIRROR")
            mirror.clear()
        else:
            mirror.append(line)

    matrix = Matrix.CreateFromList(filename, mirror, ".")
    col = mirror_columns(matrix, check_bit)
    sum += col
#    if col == 0:
    row = mirror_rows(matrix, check_bit)
    sum += row * 100
#        if row == 0:
#            print("FOUND NO MIRROR")
#    sum += mirror_matrix(matrix, check_bit)

    return sum

def solvePuzzle1(filename):
    return solveInternal(filename, False)

def solvePuzzle2(filename):
    return solveInternal(filename, True)

unittest(solvePuzzle1, 5 , "unittest1.txt")
unittest(solvePuzzle1, 400 , "unittest2.txt")
unittest(solvePuzzle1, 405 , "unittest3.txt")
unittest(solvePuzzle1, 33780 , "input.txt")

unittest(solvePuzzle2, 300 , "unittest1.txt")
unittest(solvePuzzle2, 100 , "unittest2.txt")
unittest(solvePuzzle2, 400 , "unittest4.txt")
unittest(solvePuzzle2, 23479 , "input.txt")
