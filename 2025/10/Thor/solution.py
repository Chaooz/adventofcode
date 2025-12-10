#!/usr/local/bin/python3
# https://adventofcode.com/2025/day/09

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *

#
# Solve is bit operations problem
#

#
# Change the true/false flag to be a counter of how many times we want to press this button
# Or something similar
#
 
def getNumberFromBitString(bitString, full=False):
    number = 0
    for pos, bit in enumerate(bitString[::-1]):
        bNumber = 1 << pos
        if full:
            number += bNumber
        elif bit == "#":
            number += bNumber
#            print("Setting bit at pos:", pos, bNumber)
#    print("Bits:", bitString, "Number:", number)
    return number

def getNumberFromBitPosString(bitString):
    number = 0
    for position in bitString:
        p = int(position)
        number |= (1 << p)

#    print("Bits:", bitString, "Number:", number)

    return number

def BitsToString(number, length):
    bitString = ""
    for pos in range(length-1, -1, -1):
        bNumber = 1 << pos
        if (number & bNumber) != 0:
            bitString += "#"
        else:
            bitString += "."
    return bitString

def findMinimumSwitches(index, isLightOn, total, lights, buttonList):

    # Too deep
    if index >= len(buttonList):
        return 0

    # If pressing this button turns off all lights, return total
    if index > -1 and isLightOn: 
        button = buttonList[index]
        lights ^= button
        if lights == 0:
            return total

    # Try both options: press or not press
    on  = findMinimumSwitches(index + 1, True, total + 1, lights, buttonList)
    off = findMinimumSwitches(index + 1, False, total, lights, buttonList)
    if on == 0:
        return off
    if off == 0:
        return on
    return min(on, off)

def findMinimumSwitchesPart2(index, isLightOn, total, lights, buttonList, bitSize, debugString):

    # Too deep
    if index >= len(buttonList):
        return 0

    if index > -1:
        button = buttonList[index]

        if isLightOn:
            debugString += "#"

            lights ^= button
            missingLights = 0 ^ lights

            if missingLights == 0:

                # print ("Done", total, 
                #     "Index:", index,
                #     "Button:", BitsToString(button,bitSize), 
                #     "oldLights:", BitsToString(oldLights,bitSize), 
                #     "Lights:", BitsToString(lights,bitSize), 
                #     "Missing:", BitsToString(missingLights,bitSize),
                #     "Debug:", debugString
                #     )

                return total
        else:
            debugString += "."
            missingLights = 0 ^ lights
    
        # print ("Index:", index, 
        #     "Button:", BitsToString(button,bitSize), 
        #     "oldLights:", BitsToString(oldLights,bitSize), 
        #     "Lights:", BitsToString(lights,bitSize), 
        #     "Missing:", BitsToString(missingLights,bitSize),
        #     "Debug:", debugString
        #     )

    # Try both options: press or not press
    on  = findMinimumSwitchesPart2(index + 1, True, total + 1, lights, buttonList)
    off = findMinimumSwitchesPart2(index + 1, False, total, lights, buttonList)
    if on == 0:
        return off
    if off == 0:
        return on
    return min(on, off)

def solvePuzzle1(filename):    
    total = 0
    lines = loadfile(filename)
    for line in lines:
        blocks = line.strip().split(" ")
        buttonList = []
        for block in blocks:
            if block[0] == '[':
                b = block[1:-1][::-1]
                lights = getNumberFromBitString(b, False)
                lightLength = len(b)
            elif block[0] == '(':
                buttonString = block[1:-1].replace(",","")
                buttonNumber = getNumberFromBitPosString(buttonString)
                buttonList.append( buttonNumber )
#            elif block[0] == '{':
#                print("Block found {}:", block)
#                validCombinations = block[1:-1].split(",")
        total += findMinimumSwitches(-1, False, 0, lights, buttonList)

    return total

def solvePuzzle2(filename):    
    return 0

#UNITTEST.DEBUG_ENABLED = False

setupCode("Day 10: Factory")

unittest(solvePuzzle1, 7, "unittest1.txt")
unittest(solvePuzzle2, 33, "unittest1.txt")

runCode(10,solvePuzzle1, 532, "input.txt")
#runCode(10,solvePuzzle2, 1569262188, "input.txt")