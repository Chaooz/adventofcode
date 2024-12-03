#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/3

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '/Users/thorh/Develop/DarkFactor/adventofcode/Libs')

from advent_libs import *

print("")
print_color("Day 3: Mull It Over", bcolors.OKGREEN)
print("")

#
# Generate a proper list of numbers
#
def solvePuzzleLine(textString):
    sum = 0

    # mul      - to get the starting mul
    # \(       - a ( char
    # ([^()]*) - Capturing group 1: a negated character class matching any 0 or more chars other than ( and )
    # \)       - a ) char.

    mulLines = re.findall(r'mul\(([^()]*)\)', textString)

    for pair in mulLines:
        if pair.count(",") != 1:
            continue

        a,b = pair.split(",")
        a = int(a)
        b = int(b)
        sum += a * b
    return sum

def solvePuzzle1(filename):
    sum = 0
    lines = loadfile_as_string(filename)
    return solvePuzzleLine(lines)

# Puzzle 2 will enable multiplier with do and disable it with don't
def solvePuzzleLine2(textString):
    sum = 0

    # Replace the do and dont with start and end
    # This is to not get messup with the DO and DONT in the mul instructions
    textString = textString.replace("don\'t", "end")
    textString = textString.replace("do", "start")

    # Wrap text with start and end to make sure rexex works
    textString = "start" + textString + "end"

    # (?<=start) - The text before the group must be start
    # ([^()]*)   - Capturing group 1: a negated character class matching any 0 or more chars other than ( and )
    # (?=end)    - The text after the group must be end
    mulLines = re.findall(r'(?<=start)(.*?)(?=end)', textString)

    for line in mulLines:
        sum += solvePuzzleLine(line)
    return sum

def solvePuzzle2(filename):
    sum = 0
    line = loadfile_as_string(filename)
    return solvePuzzleLine2(line)

# Only the four highlighted sections are real mul instructions. 
# Adding up the result of each instruction produces 161 (2*4 + 5*5 + 11*8 + 8*5)
unittest(solvePuzzleLine, 2024, "mul(44,46)")
unittest(solvePuzzleLine, 0, "mul(4*")
unittest(solvePuzzleLine, 161, "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))")     

# 48 (2*4 + 8*5)
unittest(solvePuzzleLine2, 48, "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))")

unittest(solvePuzzle1, 157621318, "input.txt")
unittest(solvePuzzle2, 79845780, "input.txt")

