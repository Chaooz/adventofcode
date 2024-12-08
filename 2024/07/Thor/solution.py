#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/0

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *

setupCode("Day 0: Template")

modList1 = ["+", "*"]
modList2 = ["+", "*", "||"]

def sumNumbers(index:int, numbers:list, sum:int, testValue:int, line:str, modList:list):

    # End of list and sum is correct
    if sum == testValue and index == len(numbers):
        return True

    # Out of bounds or sum is too high
    if index >= len(numbers) or sum > testValue:
        return False    

    thisNumber = numbers[index]

    for m in modList:
        if m == "+":
            if sumNumbers(index+1, numbers, sum + thisNumber, testValue, line + " + " + str(thisNumber), modList):
                return True
        elif m == "*":
            if sumNumbers(index+1, numbers, sum * thisNumber, testValue, line + " * " + str(thisNumber), modList):
                return True
        elif m == "||":
            sum = int(str(sum) + str(thisNumber))
            if sumNumbers(index+1, numbers, sum, testValue, line + " || " + str(thisNumber), modList):
                return True
    return False

def readNumberList(line:str):
    testValue, strNumbers = line.split(":")
    testValue = int(testValue)
    numbers = strNumbers.split(" ")
    numberList = []
    for number in numbers:
        if number.rstrip().lstrip() != "":
            numberList.append(int(number.rstrip().lstrip()))
    return testValue, numberList

def calculateSumLine1(line:str):
    testValue, numberList = readNumberList(line)
    sum = numberList[0]
    if sumNumbers(1, numberList, sum, testValue, str(sum), modList1) == True:
        return testValue
    return 0

def calculateSumLine2(line:str):
    testValue, numberList = readNumberList(line)
    sum = numberList[0]
    if sumNumbers(1, numberList, sum, testValue, str(sum), modList2) == True:
        return testValue
    return 0

def solvePuzzle1(filename):
    lines = loadfile(filename)
    sum = 0
    for line in lines:
        sum += calculateSumLine1(line)
    return sum

def solvePuzzle2(filename):
    lines = loadfile(filename)
    sum = 0
    for line in lines:
        sum += calculateSumLine2(line)
    return sum

unittest(calculateSumLine1, 190, "190: 10 19")
unittest(calculateSumLine1, 3267, "3267: 81 40 27")
unittest(calculateSumLine2, 156, "156: 15 6")

unittest(solvePuzzle1, 3749, "unittest1.txt")
unittest(solvePuzzle2, 11387, "unittest1.txt")

runCode(7,solvePuzzle1, 2654749936343, "input.txt")
runCode(7,solvePuzzle2, 124060392153684, "input.txt")