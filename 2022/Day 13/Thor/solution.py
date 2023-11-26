#!/usr/local/bin/python3

import sys
import ast
import itertools
from functools import cmp_to_key

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *

DRAW = 0
RIGHT_ORDER = -1
WRONG_ORDER = 1

#
# Fix input into proper lists
#
def createPairs(lines):
    pairs = []
    pair = []
    for line in lines:
        if not line.strip():
            pairs.append(pair)
#            print("A:" + str(pair))
            pair = []
        else:            
#            print("B:" + line)
            parsed = ast.literal_eval(line.strip())
            pair.append(parsed)

    return pairs

# Go through all pairs
def comparePair(left,right):

    # Left side is out of items, so inputs are in the right order
    if left is None:
        return RIGHT_ORDER

    # Right side is out of items, so the inputs are in the wrong order
    if right is None:
        return WRONG_ORDER

    if isinstance(left, int) and isinstance(right,int):
        if left < right:
            return RIGHT_ORDER
        elif left > right:
            return WRONG_ORDER
        else:
            return DRAW
    elif isinstance(left, int) and isinstance(right, list):
        return comparePair([left], right)
    elif isinstance(left, list) and isinstance(right, int):
        return comparePair(left, [right])
    else:
      for x, y in itertools.zip_longest(left, right):
            result = comparePair(x, y)
            if result == 0:
                continue
            return result 
    
    return DRAW       


def testPuzzle1(input):
    lines = input.split(" ")
    lines.append("")
    print(lines)
    pairs = createPairs(lines)
    print(pairs)
    return comparePair(pairs[0], pairs[1])

def solvePuzzle1(filename):
    count = []
    lines = loadfile(filename)
    pairs = createPairs(lines)
    for idx, pair in enumerate(pairs):
        result = comparePair(pair[0], pair[1])
        if result == RIGHT_ORDER:
            count.append(idx + 1)
    return sum(count)

def solvePuzzle2(filename):
    lines = loadfile(filename)
    pairs = createPairs(lines)

    # Flatten the list
    allPackets = []
    for pair in pairs:
        allPackets.append(pair[0])
        allPackets.append(pair[1])

    # Add the extra pairs
    extraPairs = [[[2]],[[6]]]
    allPackets += extraPairs

#    for idx, pair in enumerate(allPackets):
#        print("allPackets[" + str(idx) + "]:" + str(pair))
    

    # Sort the pairs
    sorted_pairs = sorted(allPackets, key=cmp_to_key(comparePair))
#    for idx,pair in enumerate(sorted_pairs):
#        print("sorted[" + str(idx) + "]:" + str(pair))
    return (sorted_pairs.index(extraPairs[0]) + 1) * (
        sorted_pairs.index(extraPairs[1]) + 1
    )

print("")
print_color("Day 13: Distress Signal", bcolors.OKGREEN)
print("")

#unittest(testPuzzle1, RIGHT_ORDER, "[1,1,3,1,1] [1,1,5,1,1]")
#unittest(testPuzzle1, RIGHT_ORDER, "[[1],[2,3,4]] [[1],4]")
#unittest(testPuzzle1, WRONG_ORDER, "[9] [[8,7,6]]")
#unittest(testPuzzle1, RIGHT_ORDER, "[[4,4],4,4] [[4,4],4,4,4]")
#unittest(testPuzzle1, WRONG_ORDER, "[7,7,7,7] [7,7,7]")
#unittest(testPuzzle1, RIGHT_ORDER, "[] [3]")
#unittest(testPuzzle1, WRONG_ORDER, "[[[]]] [[]]")
#unittest(testPuzzle1, WRONG_ORDER, "[1,[2,[3,[4,[5,6,7]]]],8,9] [1,[2,[3,[4,[5,6,0]]]],8,9]")

unittest(solvePuzzle1, 13, "unittest.txt")
unittest(solvePuzzle2, 140, "unittest.txt")
unittest(solvePuzzle1, 6484, "puzzleinput.txt")
unittest(solvePuzzle2, 19305, "puzzleinput.txt") # Too low