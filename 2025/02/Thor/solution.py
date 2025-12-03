#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/24

from email.mime import text
import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *

def solvePuzzle1(filename):
    line = loadfile_as_string(filename)
    lines = line.split(',')
    total = 0
    for line in lines:
        idRange = line.split('-')
        start = idRange[0].strip()
        end = idRange[1].strip()
        # Process each range here
        for n in range(int(start), int(end)+1):
            # Split the number in half
            s = str(n)
            half = len(s) // 2
            a = s[:half]
            b = s[half:]
            # Check if the sums are equal
            if a == b:
                #print("invalid digit [" + line + "]: " + str(n))
                total += n
            pass
    return total

def solvePuzzle2(filename):
    line = loadfile_as_string(filename)
    lines = line.split(',')
    total = 0
    for line in lines:
        idRange = line.split('-')
        start = idRange[0]
        end = idRange[1]
        # Process each range here
        for n in range(int(start), int(end)+1):
            # Split the number in half
            s = str(n)
            strLen = len(s)
            halfLen = strLen // 2

            if strLen % 2 == 0:
                first,second = s[:halfLen], s[halfLen:]
                if first == second:
                    total += n
                    continue

            for letter in range(1, halfLen + 1):
                if strLen % letter != 0:
                    continue
                    
                aa = s[:letter]
                bb = re.sub(f'({aa})+', '', s)
                if bb == '':
                    total += n
                    #print_debug("2 Invalid even digit: " + s)
                    break

    return total

setupCode("Day 2: Gift Shop")

#UNITTEST.DEBUG_ENABLED = True

unittest(solvePuzzle1, 1227775554, "unittest1.txt")
unittest(solvePuzzle2, 4174379265, "unittest1.txt")
    
runCode(2,solvePuzzle1, 13108371860, "input.txt")
runCode(2,solvePuzzle2, 22471660255, "input.txt")