#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/21

import sys
import re
from itertools import permutations
from functools import cache

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *
from advent_libs_matrix import *

# pad stuff
numpad = {'7': Vector2(0, 0), '8': Vector2(1, 0), '9': Vector2(2, 0),
          '4': Vector2(0, 1), '5': Vector2(1, 1), '6': Vector2(2, 1),
          '1': Vector2(0, 2), '2': Vector2(1, 2), '3': Vector2(2, 2),
          '0': Vector2(1, 3), 'A': Vector2(2, 3)}
numpad_inv = {v: k for k,v in numpad.items()}
dirpad = {'^': Vector2(1, 0), 'A': Vector2(2, 0),
          '<': Vector2(0, 1), 'v': Vector2(1, 1), '>': Vector2(2, 1)}
dirpad_inv = {v: k for k,v in dirpad.items()}
dirs = {'^': Vector2(0, -1), 'v': Vector2(0, 1), '<': Vector2(-1, 0), '>': Vector2(1, 0)}
dirs_inv = {v: k for k,v in dirs.items()}

@cache
def runKeypad(level:int, maxLevel:int, keyA:str, keyB:str):
    pad, pad_inv = (numpad, numpad_inv) if level == 0 else (dirpad, dirpad_inv)

    currenPos = pad[keyA]
    nextPos = pad[keyB]
    delta = nextPos - currenPos

    if level == maxLevel - 1:
        return abs(delta.x) + abs(delta.y) + 1

    # loop through the delta and build the pattern
    seq = []
    for _ in range(0, abs(delta.x)):
        seq.append('<' if delta.x < 0 else '>')
    for _ in range(0, abs(delta.y)):
        seq.append('^' if delta.y < 0 else 'v')

    if not seq:
        return 1

    possiblePaths = []

    # Permutations will generate all possible paths based on the sequence
    for perm in set(permutations(seq)):
        pos = currenPos

        # Go through the r path and see if is possible to go this way
        steps = 0
        for i, dir_key in enumerate(perm):
            pos += dirs[dir_key]
            if pos not in pad_inv:
#                print_debug("Invalid Key:" + keyA + "[" + currenPos.ToString() + "] => " + keyB + "[" + nextPos.ToString() + "] Delta:" + delta.ToString() + " perm:" + str(perm), " pos:" + pos.ToString())
                break

            startKey = 'A' if i == 0 else perm[i-1]
            steps += runKeypad(level+1, maxLevel, startKey, dir_key)
        else:
            # path back to A
            steps += runKeypad(level+1, maxLevel, perm[-1], 'A')
            # The path is valid, so we can calculate the steps
#            print_debug( "[" + str(level) + "] OK sum:" + keyA + "[" + currenPos.ToString() + "] => " + keyB + "[" + nextPos.ToString() + "] Delta:" + delta.ToString() + " perm:" + str(perm) + " steps:" + str(steps))

            possiblePaths.append(steps)

    print_debug("[" + str(level) + "] candidates: " + str(possiblePaths), keyA, keyB, seq)
    return min(possiblePaths)

# Numeric keypad
def runNumericKeypad(code, maxLevel, debug):

    # Show debug ?
    UNITTEST.DEBUG_ENABLED = debug

    numericCode =int(code[:-1])

    # Always start at 'A'
    retValue = runKeypad(0, maxLevel, "A", code[0])
#    print_debug("Code:" + code[0] + " Index:0 Value:" + str(retValue))
    for index in range(1,len(code)):        
        r = runKeypad(0, maxLevel, code[index-1], code[index])
        retValue += r
#        print_debug("Code:" + code[index] + " Index:" + str(index) + " Value:" + str(r) + " Total:" + str(retValue))

    print_debug_color(bcolors.LIGHT_GREY, "Code:" + code + " numCode:" + str(numericCode) + " Complexity:" + str(retValue) + " Numeric Code:" + str(numericCode) + " Total Complexity:" + str(retValue * numericCode))

    return retValue * numericCode

def runKeypad1(line):
    return runNumericKeypad(line, 3, False)

def runKeypad2(line):
    return runNumericKeypad(line, 26, False)

def solvePuzzle1(filename):
    lines = loadfile(filename)
    sum = 0
    for line in lines:
        sum += runNumericKeypad(line, 3, False)
    return sum

def solvePuzzle2(filename):
    lines = loadfile(filename)
    sum = 0
    for line in lines:
        sum += runNumericKeypad(line, 26, False)
    return sum

setupCode("Day 0: Template")

unittest(runKeypad1, 68 * 29, "029A")
unittest(runKeypad1, 60 * 980, "980A")
unittest(runKeypad1, 68 * 179, "179A")
unittest(runKeypad1, 64 * 456, "456A")
unittest(runKeypad1, 64 * 379, "379A")

unittest(runKeypad2, 2379451789590, "029A")
unittest(runKeypad2, 70797185862200, "980A")
unittest(runKeypad2, 14543936021812, "179A")
unittest(runKeypad2, 36838581189648, "456A")
unittest(runKeypad2, 29556553253044, "379A")

unittest(solvePuzzle1, 126384, "unittest1.txt")
unittest(solvePuzzle2, 154115708116294, "unittest1.txt")

runCode(21,solvePuzzle1, 206798, "input.txt")
runCode(21,solvePuzzle2, 251508572750680, "input.txt")