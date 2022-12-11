#!/usr/local/bin/python3

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *

# Global variables
strengthMeasurements = []
intervals = [20,60,100,140,180,220]

def calculateSignalStrengthAtIntervals(inputList):
    signalStrength = 1
    cycle = 0
    for command in inputList:
        command = command.split(" ")
        if command[0] == "addx":
            cycle += 1
            cycleCheck(cycle, signalStrength)
            cycle += 1
            cycleCheck(cycle, signalStrength)
            # print("Cycle: " + str(cycle) + " addx " + command[1])
            signalStrength += int(command[1])
            # print("Signal Strength: " + str(signalStrength))
            # print("----------------")
        else:
            cycle += 1
            cycleCheck(cycle, signalStrength)

def cycleCheck(cycleNumber, signalStrength):
    global strengthMeasurements
    if cycleNumber in intervals:
        # print("Cycle: " + str(cycleNumber))
        # print("Signal Strength: " + str(signalStrength))
        measuredSignalStrength = cycleNumber * signalStrength
        strengthMeasurements.append(measuredSignalStrength)
        # print("Measurements: " + str(strengthMeasurements))
        # print("----------------")

inputList = loadfile("input.txt")
calculateSignalStrengthAtIntervals(inputList)
# calculations = calculateSignalStrengthAtIntervals(inputList, 20)
solution = 0
for measurement in strengthMeasurements:
    solution += measurement
print(solution)