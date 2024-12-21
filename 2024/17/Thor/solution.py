#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/17

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *

setupCode("Day 17: Chronospatial Computer")

iteration = 0

class Cpu:
    registerA:int
    registerB:int
    registerC:int
    registerPointer:int
    output:list
    useOutput:bool
    idx:int

    def __init__(self):
        self.registerA = 0
        self.registerB = 0
        self.registerC = 0
        self.registerPointer = 0
        self.output = []
        self.useOutput = True
        self.idx = 0
    
    def print(self):
        print("A: " + str(self.registerA) + " B: " + str(self.registerB) + " C: " + str(self.registerC) + " Pointer: " + str(self.registerPointer))

    def ToString(self):
        return "A: " + str(self.registerA) + " B: " + str(self.registerB) + " C: " + str(self.registerC) + " Pointer: " + str(self.registerPointer)

    def getInstruction(self, instruction):
        if 0 <= instruction <= 3:
            return instruction
        elif instruction == 4:
            return self.registerA
        elif instruction == 5:
            return self.registerB
        elif instruction == 6:
            return self.registerC
        else:
            print_assert(False, "Invalid opCode: " + str(instruction))
            return 0


def runOpCode(opCode, instruction, cpu):
    global iteration
#    print("runOpCode: " + str(opCode) + " " + str(instruction))
    # adv
    if opCode == 0:
        s = cpu.getInstruction(instruction)
        cpu.registerA = cpu.registerA // (2 ** s)
#        print("[" + str(iteration) + "] OP-0: ", cpu.registerA, instruction, " REG:", cpu.ToString())
    # bxl
    elif opCode == 1:
        cpu.registerB = cpu.registerB ^ instruction
#        print("[" + str(iteration) + "] OP-1: ", cpu.registerB, instruction, " REG:", cpu.ToString())
    # bst
    elif opCode == 2:
        s = cpu.getInstruction(instruction) % 8
        cpu.registerB = s
#        print("[" + str(iteration) + "] OP-2b: ", cpu.registerB, instruction, " REG:", cpu.ToString())
    # jnz
    elif opCode == 3:
        if cpu.registerA != 0:
            cpu.registerPointer = instruction - 2
#            print("[" + str(iteration) + "] OP-3: ", cpu.registerPointer, instruction, " REG:", cpu.ToString())
    # bxc
    elif opCode == 4:
        cpu.registerB = cpu.registerB ^ cpu.registerC
#        print("[" + str(iteration) + "] OP-4: ", cpu.registerB, instruction, " REG:", cpu.ToString())
    # out
    elif opCode == 5:
        w = cpu.getInstruction(instruction) % 8
        if not cpu.useOutput:
#            print("CPU Program:", cpu.program, len(cpu.program), cpu.idx, w)

            if cpu.idx >= len(cpu.program):
#                print("FAIL 2: ", cpu.idx, w, len(cpu.program))
                return False

            if cpu.program[cpu.idx] != w:
#                print("FAIL 1: ", cpu.idx, w, cpu.program[cpu.idx])
                return False

            cpu.idx += 1
        cpu.output.append( w )

#        cpu.output.append( w )
#        print(instruction,w,x, cpu.registerA, cpu.registerB, cpu.registerC, cpu.registerPointer)
#        print("[" + str(iteration) + "] OP-5: ", x, instruction, " REG:", cpu.ToString())

    # bdv
    elif opCode == 6:
        s = cpu.getInstruction(instruction)
        cpu.registerB = cpu.registerA // (2 ** s)
#        print("[" + str(iteration) + "] OP-6: ", cpu.registerB, instruction, " REG:", cpu.ToString())
    # cdv
    elif opCode == 7:
        s = cpu.getInstruction(instruction)
        cpu.registerC = cpu.registerA // (2 ** s)
#        print("[" + str(iteration) + "] OP-7: ", cpu.registerC, instruction, " REG:", cpu.ToString())
    else:
        print_assert(False, "Invalid opCode: " + str(opCode))

    cpu.registerPointer += 2
#    print(cpu.registerPointer)
    return True


def solvePuzzle1(filename):
    global iteration
    lines = loadfile(filename)
    cpu = Cpu()
    program = []
    for line in lines:
        if line.rstrip() == "":
            continue
        elif line.startswith("Register A:"):
            b, c = line.split(": ")
            cpu.registerA = int(c)
        elif line.startswith("Register B:"):
            b, c = line.split(": ")
            cpu.registerB = int(c)
        elif line.startswith("Register C:"):
            b, c = line.split(": ")
            cpu.registerC = int(c)
        elif line.startswith("Program:"):
            b, c = line.split(": ")
            program = [int(x) for x in c.split(",") ]
    
    cpu.print()
    print(program)

    iteration = 0
    while 0 <= cpu.registerPointer < len(program):
        iteration += 1
        opcode, instruction = program[cpu.registerPointer], program[cpu.registerPointer+1]
        runOpCode(opcode, instruction, cpu)

    return ','.join(str(x) for x in cpu.output)

def solvePuzzle2(filename):
    global iteration
    lines = loadfile(filename)
    cpu = Cpu()
    program = []
    for line in lines:
        if line.rstrip() == "":
            continue
        elif line.startswith("Register A:"):
            b, c = line.split(": ")
            cpu.registerA = int(c)
        elif line.startswith("Register B:"):
            b, c = line.split(": ")
            cpu.registerB = int(c)
        elif line.startswith("Register C:"):
            b, c = line.split(": ")
            cpu.registerC = int(c)
        elif line.startswith("Program:"):
            b, c = line.split(": ")
            program = [int(x) for x in c.split(",") ]
    
    cpu.print()
    print("PR:", program)
    p = ','.join(str(x) for x in program)
#    p = "1" + p
#    print("P:", p)

    cpu.useOutput = False
    cpu.program = program

    for a in range(0, 10000000):
        cpu.registerA = a
        cpu.registerB = 0
        cpu.registerC = 0
        cpu.registerPointer = 0
        cpu.idx = 0
        cpu.output = []

        if a % 10000 == 0:
            print("A: " + str(a))        

        iteration = 0
        while 0 <= cpu.registerPointer < len(program):
            iteration += 1
            opcode, instruction = program[cpu.registerPointer], program[cpu.registerPointer+1]
            if not runOpCode(opcode, instruction, cpu):
                break

        pOut = ','.join(str(x) for x in cpu.output)
        #if a % 10000 == 0:
#        print("A: " + str(a) + " Output: " + pOut, " program:", cpu.program)

        if pOut == p:
            return a
        
    return -1


unittest(solvePuzzle1, "4,6,3,5,6,3,5,2,1,0", "unittest1.txt")
unittest(solvePuzzle2, 117440, "unittest2.txt")

#runCode(17,solvePuzzle1, "1,5,0,3,7,3,0,3,1", "input.txt")
runCode(17,solvePuzzle2, -1, "input.txt")