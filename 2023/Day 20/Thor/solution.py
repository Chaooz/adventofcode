#!/usr/local/bin/python3
# https://adventofcode.com/2023/day/2

import sys
import math

# Import custom libraries
sys.path.insert(1, '../../../Libs')

#from ...Libs.advent_libs import *
from advent_libs import *

print("")
print_color("Day 20: Pulse Propagation", bcolors.OKGREEN)
print("")

class Module:
    OPERAND_NONE = 0
    OPERAND_FLIPFLOP = 1
    OPERAND_CONJUNCTION = 2
    OPERAND_BROADCASTER = 3

    op:int
    name:str
    dest_modules:list
    pulse:int

    def __init__(self, op:int, name:str, dest:str):
        self.pulse = 0
        self.op = op
        self.name = name
        self.dest_modules = [ x.strip() for x in dest.split(",") ]

    def GetOutput(self):
        return self.dest_modules
    
    def Op(self):
        return self.op

    def GetOpName(op:int):
        if op == Module.OPERAND_BROADCASTER:
            return "OPERAND_BROADCASTER"
        elif op == Module.OPERAND_CONJUNCTION:
            return "OPERAND_CONJUNCTION"
        elif op == Module.OPERAND_FLIPFLOP:
            return "OPERAND_FLIPFLOP"
        return "?" + str(op)

    def GetPulseName(pulse:int):
        if pulse == 0:
            return "low"
        return "high"

    def HandlePulse(self, pulseFrom:str, pulse:int):
        print("Handle pulse", pulseFrom, "-", Module.GetPulseName(self.pulse), "- => ", self.name, " op:", Module.GetOpName(self.op) )

        # The pulse is just passed on
        if self.op == Module.OPERAND_BROADCASTER:
            self.pulse = pulse

        # Flip pulse on/off if we receive a low pulse
        elif self.op == Module.OPERAND_FLIPFLOP:
            if pulse == 0:
                self.pulse = 1 - self.pulse

        elif self.op == Module.OPERAND_CONJUNCTION:
            if pulse == 0:
                self.pulse = 0

        # Unknown operation
        else:
            pass

def readInput(filename):
    lines = loadfile(filename)
    module_list = dict()
    for line in lines:
        char = line[0]
        values = line.split(" -> ")
        key = values[0].strip()

        op = Module.OPERAND_NONE
        if char == '%':
            op = Module.OPERAND_FLIPFLOP
            key = key[1:]
        elif char == "&":
            op = Module.OPERAND_CONJUNCTION
            key = key[1:]
        elif char == "b":
            op = Module.OPERAND_BROADCASTER

#        print("line:", line, "op:", op, " key:",key," values:", values[1])

#        if len(module_list) == 0:
#            module_list["START"] = Module(Module.OPERAND_BROADCASTER, "START", key)

        module_list[key] = Module(op, key, values[1])
    return module_list

def runIteration(module_list:int, max_iter:int):
    i = 0

    # Get the first key
    key = next(iter(module_list))
    while True:
        i = i + 1
        if i > max_iter:
            print("Max iterations : ", i)
            exit(0)

        module = module_list[key]

        # Exit criteria, if flipflop has a highpulse it exits
        if module.op == Module.OPERAND_FLIPFLOP and module.pulse == 1:
            return

        receivers = module.GetOutput()
        for receiverKey in receivers:
            receiverModule = module_list[receiverKey]
            receiverModule.HandlePulse(module.name, module.pulse)


def solvePuzzle1(filename):
    module_list = readInput(filename)

    runIteration(module_list, 10)

    low_pulses = 0
    high_pulses = 0
    for key in module_list:
        module = module_list[key]
        if module.pulse == 0:
            low_pulses += 1
        else:
            high_pulses += 1

    sum = low_pulses * high_pulses
    print("Sum:", low_pulses, " x ", high_pulses , " => ", sum )
    return sum

def solvePuzzle2(filename):
    return -1

unittest(solvePuzzle1, 32000000, "unittest1.txt")     
#unittest(solvePuzzle1, 0, "input.txt")     

#unittest(solvePuzzle2, 0, "unittest2.txt")
#unittest(solvePuzzle2, 0, "input.txt")     

