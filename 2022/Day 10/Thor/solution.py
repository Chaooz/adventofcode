#!/usr/local/bin/python3

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_matrix import *
from advent_libs_list import *
from advent_libs_vector2 import *


print("")
print_color("Day 9: Rope Bridge", bcolors.OKGREEN)
print("")

def checkCycle(cycle:int, checkPointList:list, signalStrength:int):
    if cycle in checkPointList:
#        print("checkCycle: cycle: " + str(cycle) + " signal:" + str(signalStrength) + " = " + str(cycle * signalStrength))
        return cycle * signalStrength
    return 0

def solvePuzzle1(filename):
    commandList = loadfile(filename)

    checkPointList = [20,60,100,140,180,220]

    cycle = 0
    signalStrength = 1
    sum = 0
    for command in commandList:
        command = command.strip().split(" ")

        cycle += 1
        sum += checkCycle(cycle, checkPointList, signalStrength)

        if command[0] == "addx":
            cycle += 1
            sum += checkCycle(cycle, checkPointList, signalStrength)

            signal = int(command[1])
            signalStrength += signal

    return sum

#
# Part two
#
def runCycle(matrix:Matrix,cycle:int, cursorPosition:Vector2, spritePosition:int, fre:int):

    cycle += 1

    if cursorPosition.x > spritePosition - 2 and cursorPosition.x < spritePosition + 2:
        matrix.Set(cursorPosition.x, cursorPosition.y, "X")
    else:
        matrix.Set(cursorPosition.x, cursorPosition.y, ".")

    cursorPosition.x +=1
    if cycle % 40 == 0:
        cursorPosition.y += 1
        cursorPosition.x = 0

    return cycle,cursorPosition

def solvePuzzle2(filename):
    commandList = loadfile(filename)

    cycle = 0
    spritePosition = 1
    sum = 0

    matrix = Matrix("CRT Screen", 40,6," ")

    cursorPosition = Vector2(0,0)
    for command in commandList:
        command = command.strip().split(" ")

        cycle, cursorPosition = runCycle(matrix,cycle, cursorPosition, spritePosition, 0)

        if command[0] == "addx":
            signal = int(command[1])
            cycle, cursorPosition = runCycle(matrix,cycle,cursorPosition, spritePosition, signal)
            spritePosition += signal

    matrix.Print(".", bcolors.DARK_GREY, "", "")
    return sum



unittest(solvePuzzle1, 13140, "unittest.txt")
unittest(solvePuzzle1, 15020, "puzzleinput.txt")

#unittest(solvePuzzle2, 15020, "unittest.txt")
unittest(solvePuzzle2, 15020, "puzzleinput.txt")
