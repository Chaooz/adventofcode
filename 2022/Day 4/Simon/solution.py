#!/usr/local/bin/python3

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_list import *
#import advent_libs_list

def countContainedRanges(elfPairs):
    counter = 0
    for pair in elfPairs:
        elf1 = pair[0].split("-")
        elf1 = range(int(elf1[0]),int(elf1[1]))
        elf2 = pair[1].split("-")
        elf2 = range(int(elf2[0]),int(elf2[1]))
        tempElf1 = range(elf1.start,elf1.stop+1)
        tempElf2 = range(elf2.start,elf2.stop+1)

        if elf2.start in tempElf1 and elf2.stop in tempElf1: 
            counter += 1
        elif elf1.start in tempElf2 and elf1.stop in tempElf2:
            counter += 1
    return counter

def countOverlappingRanges(elfPairs):
    counter = 0
    for pair in elfPairs:
        elf1 = pair[0].split("-")
        elf1 = range(int(elf1[0]),int(elf1[1]))
        elf2 = pair[1].split("-")
        elf2 = range(int(elf2[0]),int(elf2[1]))
        tempElf1 = range(elf1.start,elf1.stop+1)
        tempElf2 = range(elf2.start,elf2.stop+1)

        if elf1.start in tempElf2 or elf1.stop in tempElf2:
            counter += 1
        elif elf2.start in tempElf1 or elf2.stop in tempElf1: 
            counter += 1
    return counter

pairs = listFromFile("input.txt", ",")
print("Part 1: " + str(countContainedRanges(pairs)))
print("Part 2: " + str(countOverlappingRanges(pairs)))
