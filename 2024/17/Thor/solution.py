#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/17

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *
from advent_libs_multithreading import *



class Cpu:
    foundRegA = 0

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


    def runOpCode(self,opCode, instruction):
        if opCode == 0:
            s = self.getInstruction(instruction)
            self.registerA = self.registerA // (2 ** s)
        # bxl
        elif opCode == 1:
            self.registerB = self.registerB ^ instruction
        # bst
        elif opCode == 2:
            s = self.getInstruction(instruction) % 8
            self.registerB = s
        # jnz
        elif opCode == 3:
            if self.registerA != 0:
                self.registerPointer = instruction - 2
        # bxc
        elif opCode == 4:
            self.registerB = self.registerB ^ self.registerC
        # out
        elif opCode == 5:
            w = self.getInstruction(instruction) % 8
            if not self.useOutput:
                if self.idx >= len(self.program):
                    return False
                if self.program[self.idx] != w:
                    return False
                self.idx += 1
            
            self.output.append( w )

        # bdv
        elif opCode == 6:
            s = self.getInstruction(instruction)
            self.registerB = self.registerA // (2 ** s)
        # cdv
        elif opCode == 7:
            s = self.getInstruction(instruction)
            self.registerC = self.registerA // (2 ** s)

        self.registerPointer += 2
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
        cpu.runOpCode(opcode, instruction)

    return ','.join(str(x) for x in cpu.output)

def RunPermutation(q,Lock,startRange, numRange, program):

    cpu = Cpu()
    cpu.useOutput = False
    cpu.program = program
    cpu.foundRegA = 0

    endRange = startRange + numRange
    result = ','.join(str(x) for x in cpu.program)

#    print("RunPermitations:", startRange, endRange, program)

    for a in range(startRange, endRange):
        cpu.registerA = a
        cpu.registerB = 0
        cpu.registerC = 0
        cpu.registerPointer = 0
        cpu.idx = 0
        cpu.output = []

        iteration = 0
        while 0 <= cpu.registerPointer < len(cpu.program):
            iteration += 1
            opcode, instruction = cpu.program[cpu.registerPointer], cpu.program[cpu.registerPointer+1]
            if not cpu.runOpCode(opcode, instruction):
                break

        pOut = ','.join(str(x) for x in cpu.output)
        if pOut == result:
            print("A: " + str(a) + " Output: " + pOut, " program:", cpu.program)
            cpu.foundRegA = a
            with Lock:
                if q.empty():
#                    print("PutA")
                    q.put(a)
                else:
                    oldA = q.get()
#                    print("b:",oldA,a)
                    if oldA > a:
                        q.put(a)
                    else:
                        q.put(oldA)
        if cpu.foundRegA != 0:
            break

def solvePuzzle2(filename):
    global iteration
    lines = loadfile(filename)
    program = []
    for line in lines:
        if line.rstrip() == "":
            continue
        elif line.startswith("Program:"):
            b, c = line.split(": ")
            program = [int(x) for x in c.split(",") ]
    
    threads = 2
    numbers = 10000000
    runner:JobRunner = JobRunner(threads)
    for r in range(0,threads):
        s = r * numbers
        runner.AddToQueue( RunPermutation, [s, numbers, program] )
    runner.RunQueue()

    ret = runner.GetValue()
    if ret is not None:
        n = (threads * numbers) / 1000000
        print("Jobs done", ret, " tried: ", n, " millions")
        return ret
    return 0

if __name__ == '__main__':

    setupCode("Day 17: Chronospatial Computer")

    #unittest(solvePuzzle1, "4,6,3,5,6,3,5,2,1,0", "unittest1.txt")
    unittest(solvePuzzle2, 117440, "unittest2.txt")

    #runCode(17,solvePuzzle1, "1,5,0,3,7,3,0,3,1", "input.txt")
    runCode(17,solvePuzzle2, -1, "input.txt")
