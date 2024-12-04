
#
# 2022 Day 5: Supply Stacks
#

#!/usr/lib/python3
# https://adventofcode.com/2022/day/5

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *

setupCode("Day 5: Supply Stacks")

def debugPrintPile(pile):

    if UNITTEST.DEBUG_ENABLED == False:
        return

    # Get max height
    maxHeight = 0
    for index in range(0,len(pile)):
        stack = pile[index]
        if len(stack) > maxHeight:
            maxHeight = len(stack)

    # print it
    for lineNumber in range(1,maxHeight+1):
        line = ""
        for index in range(0,len(pile)):
            stack = pile[index]

            found = False
            for pIndex in range(0,len(stack)):
                v = stack[pIndex]
                if v != None and v[1] == lineNumber:
                    line += "[" + str(v[0]) + "] "
                    found = True
            if not found:
                line += "    "
        print(line)

def parseFile(lines):

    cratePile = []
    for index in range(0,10):
        cratePile.append([])

    lineNumber = 0

    isHeader = True
    for line in lines:
        emptyLine = line.strip()
        if emptyLine == "":
            isHeader = False
            continue

        # CratePile ?
        # Rename box to crates

        if isHeader:
            lineNumber += 1

            # [Z] [M] [P]
            boxNumber = 0
            for index in range(0,len(line)):
                character = line[index]
                #print("c:" + str(character))
                if character == "]":
                    boxNumber = int(index / 4)
                    box = line[index-1]
                    stack = cratePile[boxNumber]
                    stack.append(( box, lineNumber ) )
        else:
            # move 1 from 2 to 1
            (txt1, moveNumber, txt2, moveFrom, txt3, moveTo ) = line.split(" ")
#            print("Move " + str(moveNumber) + " boxes: " + str(moveFrom + " => " + moveTo))

    return cratePile

def solvePuzzle1(filename):
    lines = loadfile(filename)
    pile = parseFile(lines)
    debugPrintPile(pile)
    return 0

unittest(solvePuzzle1, "CMZ", "unittest1.txt")

runCode(5,solvePuzzle1, "VQZNJMWTR", "puzzleinput.txt")
runCode(5,solvePuzzle1, "NLCDCLVMQ", "puzzleinput.txt")
