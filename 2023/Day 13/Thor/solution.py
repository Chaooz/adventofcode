#!/usr/local/bin/python3
# https://adventofcode.com/2023/day/13

import sys
import math

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_vector2 import *
from advent_libs_matrix import *

setupCode("Day 13: Point of Incidence")

def SetBit(number, bit):
#    print_debug ("SetBit:", number, bit)
    return number | ( 1 << bit )

def IsBitSet(number, bit):
#    print_debug ("IsBitSet:", number, bit)
    return number & ( 1 << bit )

# function to check if x is power of 2
def isPowerOfTwo( x ):
 
    # First x in the below expression is
    # for the case when x is 0
    return x and (not(x & (x - 1)))
 
# function to check whether the two numbers
# differ at one bit position only
def differAtOneBitPos( a , b ):
    return isPowerOfTwo(a ^ b)

#
# Return the bits that are different between two numbers
#
def getBitDiff(a,b):
    # 0b100000
    diff = a^b
    # 5 (the first position (backwards) which differs, 0 if a==b )
    return diff.bit_length() - 1

def is_mirror(mirror_list:list, line:int, check_bit:bool):

    mirror_once = True
    mirror_line = 0
    for i in range(1,line):

        aa = line - i-1
        bb = line + i

        if aa < 0 or bb >= len(mirror_list):
            return True,line

        a = mirror_list[line - i - 1]
        b = mirror_list[line + i]
        if check_bit == False and a != b:
            return False,0
        elif check_bit == True and a != b:
            if mirror_once and differAtOneBitPos(a,b):
                mirror_once = False
                mirror_line = i
            else:
#                print("IsMirror false [2]:", line, a,b, i, mirror_list)
                return False,0

    return check_bit != mirror_once, mirror_line


#
# Read all mirrors into a list of matrices
#
def read_mirrors(filename):
    lines = loadfile(filename)

    # Group lines
    mirror_list = list()
    mirror = list()
    for line in lines:
        if line == "":
            matrix = Matrix.CreateFromList(filename, mirror, ".")
            mirror_list.append(matrix)
            mirror.clear()
        else:
            mirror.append(line)

    if len(mirror) > 0:
        matrix = Matrix.CreateFromList(filename, mirror, ".")
        mirror_list.append(matrix)
    
    return mirror_list

#
# Convert each row in the matrix to a number based on # and . (bitwise)
#
def get_rows_from_matrix(matrix:Matrix):
    number_list = list()
    for x in range(0,matrix.sizeX):
        number = 0
        for y in range(0,matrix.sizeY):
            if ( matrix.Get(x,y) == "#"):
                number = SetBit(number, y)
        number_list.append(number)
    return number_list

#
# Convert each column in the matrix to a number based on # and . (bitwise)
#
def get_columns_from_matrix(matrix:Matrix):
    number_list = list()
    for y in range(0,matrix.sizeY):
        number = 0
        for x in range(0,matrix.sizeX):
            if ( matrix.Get(x,y) == "#"):
                number = SetBit(number, x)
        number_list.append(number)
    return number_list


def mirror_matrix(matrix:Matrix) -> int:
    number_list = get_rows_from_matrix(matrix)
    mirror_row, changed_row = mirror_value(number_list, check_bit)

    # If we have flipped a bit, set it in the matrix
    # Cannot change the column bit
    print_debug("row:",mirror_row,changed_row)
    if check_bit and changed_row > 0:
        numberA = number_list[changed_row]
        numberB = number_list[changed_row - 1]
        print_debug("Flip bit for line :", changed_row, "A:",numberA, "B:", numberB, " list:", number_list)
        check_bit = False
        
    number_list = get_columns_from_matrix(matrix)
    mirrow_col, change_col = mirror_value(number_list, check_bit)

    return mirror_row + mirrow_col * 100

#
# Check if all the lines around the line are equal
# 
def all_lines_around_are_equal(mirror_list:list, line:int) -> bool:
    for j in range(1, len(mirror_list)):
        indexA = line - j - 1
        indexB = line + j
        if indexA < 0 or indexB >= len(mirror_list):
            return True
        
        aa = mirror_list[indexA]
        bb = mirror_list[indexB]
        if aa != bb:
            return False
    return True

def smudge_in_mirror(mirror_list:list, line:int) -> bool:    
    smudgeLine = 0
    for j in range(1, len(mirror_list)):
        indexA = line - j - 1
        indexB = line + j
        if indexA < 0 or indexB >= len(mirror_list):
            return smudgeLine
        
        aa = mirror_list[indexA]
        bb = mirror_list[indexB]

        if differAtOneBitPos(aa,bb) and smudgeLine == 0:
            smudgeLine = j
        elif differAtOneBitPos(aa,bb):
            return 0
    return smudgeLine

#
# Return the line number where the mirror is equal
#
def mirror_equal(mirror_list) -> bool:
    for i in range(1,len(mirror_list)):
        a = mirror_list[i-1]
        b = mirror_list[i]
        if a == b and all_lines_around_are_equal(mirror_list, i):
            return i        
    return 0

#
# Return the line number where the mirror is equal, but the line is flipped
#
def mirror_equal_flipped(mirror_list) -> bool:
    for i in range(1,len(mirror_list)):
        a = mirror_list[i-1]
        b = mirror_list[i]
        if differAtOneBitPos(a,b) and all_lines_around_are_equal(mirror_list, i):
            return i        
    return 0

def mirror_equal_other_flipped(mirror_list) -> bool:
    smudge_line = 0
    for i in range(1,len(mirror_list)):
        a = mirror_list[i-1]
        b = mirror_list[i]
        if a==b:
            smudge_line = smudge_in_mirror(mirror_list, i)
            if smudge_line > 0:
                return i,smudge_line
    return 0,0

def solvePuzzle1(filename):
    sum = 0
    mirror_list = read_mirrors(filename)
    for mirror in mirror_list:
        rows = get_rows_from_matrix(mirror)
        cols = get_columns_from_matrix(mirror)
        mirror_row = mirror_equal(rows)        
        mirrow_col = mirror_equal(cols)
        sum += mirror_row + mirrow_col * 100
    return sum

# Line is 3, bit is 5
def flip_bit_in_line(line1:int, line2:int, source_list:list, dest_list:list):
    if line1 >= len(source_list) or line2 >= len(source_list):
        return dest_list

    a = source_list[line1]
    b = source_list[line2]
    c = getBitDiff(a,b)

    if c < 0:
        print_debug("WOA", line1, line2, a,b,c, source_list)

    if line1 == 0:
        print_debug("WOA2", a,b,c)

    if IsBitSet(a,c):
        dest_list[c] = SetBit(dest_list[c], line2)
    else:
        dest_list[c] = SetBit(dest_list[c], line1)

    return dest_list

#
# Explain this :D
#
def solvePuzzle2(filename):
    sum = 0

    # Overengineering 101
    colorList = list()
    colorList.append(("O", bcolors.YELLOW))
    colorList.append((":", bcolors.YELLOW))
    colorList.append(("#", bcolors.DARK_GREY))
    colorList.append((".", bcolors.DARK_GREY))

    mirror_list = read_mirrors(filename)
    for mirror in mirror_list:
        rows = get_rows_from_matrix(mirror)
        cols = get_columns_from_matrix(mirror)

        # Check if the line is flipped
        mirror_row = mirror_equal_flipped(rows)
        if mirror_row > 0:
            cols = flip_bit_in_line(mirror_row,mirror_row-1, rows, cols)

        mirror_col = mirror_equal_flipped(cols)
        if mirror_col > 0:
            rows = flip_bit_in_line(mirror_col,mirror_col-1, cols, rows)
            print_debug("smudge col: ", mirror_col, "len: ", len(rows), "x",len(cols))


        # Check if the smudge is somewhere else
        if mirror_row == 0 and mirror_col == 0:
            mirror_row, smudge_line = mirror_equal_other_flipped(rows)
            if smudge_line > 0:
                if UNITTEST.DEBUG_ENABLED:
                    mirror.PrintWithColor(colorList,"", " ")

                offset = mirror_row - smudge_line
                print_debug("smudge other row:", mirror_row, " line:", smudge_line, " offset:", offset, "len: ", len(rows), "x",len(cols))
                cols = flip_bit_in_line(smudge_line, mirror_row + offset, rows, cols)

            mirror_col, smudge_line = mirror_equal_other_flipped(cols)

        sum += mirror_row + mirror_col * 100
        return

    return sum


unittest(solvePuzzle1, 5 , "unittest1.txt")
unittest(solvePuzzle1, 400 , "unittest2.txt")
unittest(solvePuzzle1, 405 , "unittest3.txt")

unittest(solvePuzzle2, 300 , "unittest1.txt")   # Top left corner is flipped
unittest(solvePuzzle2, 100 , "unittest2.txt")   # Mirror line is flipped
unittest(solvePuzzle2, 400 , "unittest4.txt")

runCode(13, solvePuzzle1, 33780 , "input.txt")

UNITTEST.DEBUG_ENABLED = True

runCode(13, solvePuzzle2, 23479 , "input.txt")
