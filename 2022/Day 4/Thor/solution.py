#
# 2022 Day 4: Camp Cleanup
#

#!/usr/lib/python3
# https://adventofcode.com/2022/day/4

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *

setupCode("Day 4: Camp Cleanup")

def createGroup(group):
    areas = []
    sections = group.split(",")
    for section in sections:
        area = section.split("-")
        areas.append( ( int(area[0]), int(area[1]) ) )
    return areas

def isAreaCovered( group ):
    elf1 = group[0]
    elf2 = group[1]
    elf1 = range(int(elf1[0]),int(elf1[1]))
    elf2 = range(int(elf2[0]),int(elf2[1]))
    elf1temp = range(elf1.start, elf1.stop+1)
    elf2temp = range(elf2.start, elf2.stop+1)

    if elf2.start in elf1temp and elf2.stop in elf1temp: 
        return 1
    elif elf1.start in elf2temp and elf1.stop in elf2temp:
        return 1
    return 0

def isAreaPartlyCovered(group):
    elf1 = group[0]
    elf2 = group[1]
    elf1 = range(int(elf1[0]),int(elf1[1]))
    elf2 = range(int(elf2[0]),int(elf2[1]))
    elf1temp = range(elf1.start, elf1.stop+1)
    elf2temp = range(elf2.start, elf2.stop+1)

    if elf2.start in elf1temp or elf2.stop in elf1temp: 
        return 1
    elif elf1.start in elf2temp or elf1.stop in elf2temp:
        return 1
    return 0

def solvePuzzle1(filename):
    lines = loadfile(filename)  
    number = 0  
    for group in lines:
        group = group.strip()
        areas = createGroup(group)
        number += isAreaCovered(areas)
    return number

def solvePuzzle2(filename):
    lines = loadfile(filename)  
    number = 0  
    for group in lines:
        group = group.strip()
        areas = createGroup(group)
        number += isAreaPartlyCovered(areas)
    return number

unittest(isAreaCovered, 0, [(2,4),(6,8)])
unittest(isAreaCovered, 0, [(2,3),(4,5)])
unittest(isAreaCovered, 0, [(5,7),(7,9)])
unittest(isAreaCovered, 1, [(2,8),(3,7)])
unittest(isAreaCovered, 1, [(6,6),(4,6)])
unittest(isAreaCovered, 0, [(2,6),(4,8)])

unittest(isAreaPartlyCovered, 0, [(2,4),(6,8)])
unittest(isAreaPartlyCovered, 0, [(2,3),(4,5)])
unittest(isAreaPartlyCovered, 1, [(5,7),(7,9)])
unittest(isAreaPartlyCovered, 1, [(2,8),(3,7)])
unittest(isAreaPartlyCovered, 1, [(6,6),(4,6)])
unittest(isAreaPartlyCovered, 1, [(2,6),(4,8)])

unittest(solvePuzzle1, 2, "unittest1.txt")

runCode(4,solvePuzzle1, 524, "puzzleinput.txt")
runCode(4,solvePuzzle2, 798, "puzzleinput.txt")
runCode(4,solvePuzzle1, 518, "puzzleinput_work.txt")
runCode(4,solvePuzzle2, 909, "puzzleinput_work.txt")
