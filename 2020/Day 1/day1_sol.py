#!/usr/bin/python3

#
# Day 1 Report Despair : https://adventofcode.com/2020/day/1
# 

import sys

# Import custom libraries
sys.path.insert(1, '../../Libs')
from advent_libs import *

# Function to find which two numbers adds up to 2020
def find2020Sum(input):
    for number1 in input:        
        iNumber1 = int(number1)
        for number2 in input:
            iNumber2 = int(number2)

            #print_warning("Testing number " + str(iNumber1) + " and " + str(iNumber1) + " = " + str(iNumber1 + iNumber2) )
            if (iNumber1 + iNumber2 == 2020):
                #print_ok("Found number! " + str(iNumber1) + " and " + str(iNumber2))
                return [iNumber1,iNumber2]
    return [0,0]    

def find2020SumWithThree(input):
    for number1 in input:
        iNumber1 = int(number1)
        for number2 in input:
            iNumber2 = int(number2)
            for number3 in input:
                iNumber3 = int(number3)
                if (iNumber1 + iNumber2 + iNumber3 == 2020):
                    #print_ok("Success! " + str(iNumber1) + ", " + str(iNumber2) + " and " + str(iNumber3))
                    return [iNumber1, iNumber2, iNumber3]

#
# Read assignment 2 from file and print
#
def find2020SumFile(filename):
    input = loadfile(filename)
    numbers = find2020Sum(input)
    result = numbers[0] * numbers[1]
    print_ok("Assignment 1 : " + filename + " => " + str(result))

#
# Read assignment 2 from file and print
#
def find2020SumWithTreeFile(filename):
    input = loadfile(filename)
    numbers = find2020SumWithThree(input)
    result = numbers[0] * numbers[1] * numbers[2]
    print_ok("Assignment 2 : " + filename + " => " + str(result))

# Test example
unittest_list(find2020Sum, [1721,299], [1721,979,366,299,675,1456])
unittest_list(find2020SumWithThree, [979,366,675], [1721,979,366,299,675,1456])

find2020SumFile("simon_puzzledata.txt")
find2020SumFile("thor_puzzledata.txt")

find2020SumWithTreeFile("simon_puzzledata.txt")
find2020SumWithTreeFile("thor_puzzledata.txt")
