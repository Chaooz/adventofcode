#
# 2022 Day 3: Rucksack Reorganization
#

# Rules
# * Letters in input is case sensitive

#!/usr/lib/python3

import sys

# Import custom libraries
sys.path.insert(1, '../../Libs')
from advent_libs import *

def getSimilarPacket(packet):
    mid = int(len(packet) / 2)
    item1 = packet[0:mid]
    item2 = packet[mid:len(packet)]
    for letter in item2:
        a = item1.find(letter)
        if a >= 0:
            return letter

    return ""

def solvePuzzle1(filename):
    lines = loadfile(filename)
    for line in lines:
        line = line.replace("\n", "")
        letter = getSimilarPacket(line)
        print(letter)
    return 0

print("")
print_color("Day 3: Rucksack Reorganization", bcolors.OKGREEN)
print("")

unittest(getSimilarPacket, "L","jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL")

#unittest(solvePuzzle1, 1, "unittest1.txt")
#unittest(solvePuzzle1, 1, "puzzleinput.txt"
