#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/13

#
# This assignment is a math problem have to be good in vector math to solve it
# Specifically inversed Matrix
#

import sys
import re
import math

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *
from advent_libs_vector2 import *

setupCode("Day 13: Claw Contraption")

def readInput(lines):
    prizes = list()
    for line in lines:
        if line.rstrip() == "":
            continue

        key,value = line.split(":")
        vector = value.split(",")

        if key == "Button A":
            x = vector[0].replace("X+", "").rstrip().lstrip()
            y = vector[1].replace("Y+", "").rstrip().lstrip()
            a = Vector2(int(x),int(y))
#            print ("A:", a)
        elif key == "Button B":
            x = vector[0].replace("X+", "").rstrip().lstrip()
            y = vector[1].replace("Y+", "").rstrip().lstrip()
            b = Vector2(int(x),int(y))
#            print ("B:", b)
        elif key == "Prize":
            x = vector[0].replace("X=", "").rstrip().lstrip()
            y = vector[1].replace("Y=", "").rstrip().lstrip()
            c = Vector2(int(x),int(y))
#            print ("C:", c)
            prizes.append( ( a,b,c ))
        else:
            print_assert("ERROR")

    return prizes

def calcButton(buttonA, buttonB, startPrize, offset ):

    # Offset price with 1m 
    prize = Vector2( offset + startPrize.x, offset + startPrize.y )

    # Example input
    # buttonA (94,34) and buttonB (22,67) and prize (8400,5400)

    # We need to sole this equation
    # ButtonA.x * a + ButtonB.y * b = prize.x
    # ButtonA.y * a + ButtonB.x * b = prize.y

    # Also represented by 
    # Matrix * ab vector = prize vector
    # [ 94 22 ][ a ] ≈ [ 8400 ]
    # [ 34 67 ][ b ]   [ 5400 ]

    # To find the ab vector we have to use this formula 
    # Inverse the Coefficient matrix
    #                     -1
    # [ a ] = ( [ 94 22] )    * [ 8400 ]
    # [ b ]   ( [ 34 67] )      [ 5400 ]
    #

    # To find the inverse matrix
    #            -1                  -1
    # ( [ 94 22] )       => ( [ a b ] )     =>   1  * [ d  -b ]    =>    1   * [ 67  -22 ]
    # ( [ 34 67] )       => ( [ c d ] )     =>  |A|   [ -c  a ]    =>   |A|    [ -34  94 ]
    #
    
    #
    # First find determinant |A|
    # |A| = ( x1 * y2 ) - ( x2 * y1 )
    # Example: ButtonA(94,34) and ButtonB(22,67) would be 
    # |A| = ( 94 * 67 ) - (22 * 34) that gives 6298 - 748 = 5550
    #
    determinant = (buttonA.x * buttonB.y) - ( buttonB.x * buttonA.y)

    #
    # Find the inverted matrix value
    #
    #  1    [ d  -b ]
    #  -  * [       ]
    # |A|   [ -c  a ]
    #
    # Example
    # 
    #  1     [ 67  -22 ]         [ 67/5550   -22/5550  ]     [ 0.01207207   -0.00397396  ]
    #  -   * [         ]     =>  [                     ]  => [                           ] 
    # 5550   [ -34  94 ]         [ -34/5550   94/5550  ]     [ -0.00612613   0.001693694 ]
    #

    # Finally
    # Multiply inverted matrix with vector #3 ( prize )
    #
    # [ d  -b] [prizeX]
    # [ -c  a] [prizeY]
    #
    # Example
    # [ 0,01207207   -0,00397396  ]    [ 8400 ]       [ (0,01207207 * 8400) + ( -0,00397396 * 5400 ) ]        [ 80 ]
    # [ -0,00612613   0,01693694 ]     [ 5400 ]    =  [ (-0,00612613 *8400) + ( 0,01693694 * 5400 )  ]  =     [ 40 ]
    #

    intervalA = (prize.x * buttonB.y) - ( prize.y * buttonB.x )
    aPresses = intervalA / determinant

    intervalB = (prize.y * buttonA.x) - ( prize.x * buttonA.y )
    bPresses = intervalB / determinant

    if (aPresses * buttonA.x) + (bPresses * buttonB.x == prize.x ) and (aPresses * buttonA.y) + (bPresses * buttonB.y == prize.y ):
        if int(aPresses) == aPresses and int(bPresses) == bPresses:
            return int((aPresses * 3) + bPresses)

    return 0


def solvePuzzle1(filename):
    lines = loadfile(filename)
    priceList = readInput(lines)

    sum = 0
    for price in priceList:
        a,b,p = price
        sum += calcButton(a, b, p, 0)
    return sum

def solvePuzzle2(filename):
    lines = loadfile(filename)
    priceList = readInput(lines)

    fixed = 10000000000000
    sum = 0
    for price in priceList:
        a,b,p = price
        sum += calcButton(a, b, p, fixed)
    return sum

unittest(solvePuzzle1, 480, "unittest1.txt")
unittest(solvePuzzle2, 875318608908, "unittest1.txt")
runCode(13,solvePuzzle1, 33427, "input.txt")
runCode(13,solvePuzzle2, 91649162972270, "input.txt")