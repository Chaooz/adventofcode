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
    programAsReturn:bool
    idx:int

    def __init__(self, programAsReturn:bool):
        self.registerA = 0
        self.registerB = 0
        self.registerC = 0
        self.registerPointer = 0
        self.output = []
        self.programAsReturn = programAsReturn
        self.idx = 0
    
    def CreateFromFile(filename:str, programAsReturn:bool):
        lines = loadfile(filename)
        cpu = Cpu(programAsReturn)

        for line in lines:
            if line.startswith("Register A:"):
                b, c = line.split(": ")
                cpu.registerA = int(c)
            if line.startswith("Program:"):
                b, c = line.split(": ")
                cpu.program = [int(x) for x in c.split(",") ]

        return cpu


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
            if self.programAsReturn:
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

    # 
    # Run the program once with the current values in the register
    #
    def RunOnePermutation(self, registerA):
        self.registerA = registerA
        self.registerB = 0
        self.registerC = 0
        self.registerPointer = 0
        self.idx = 0
        self.output = []

        while 0 <= self.registerPointer < len(self.program):
            opcode, instruction = self.program[self.registerPointer], self.program[self.registerPointer+1]
            if not self.runOpCode(opcode, instruction):
                return None
        return self.output

def solvePuzzle1(filename):
    cpu = Cpu.CreateFromFile(filename, False)
    intList = cpu.RunOnePermutation(cpu.registerA)    
    return ','.join(str(x) for x in intList)

def RunThreadPermutation(q,Lock,startRange, numRange, program):

    cpu = Cpu(True)
    cpu.program = program
    endRange = startRange + numRange

    for a in range(startRange, endRange):
        cpuOutput = cpu.RunOnePermutation( a )
        if cpuOutput == cpu.program:
            print_debug("A: " + str(a) + " Output: " + str(cpuOutput), " program:", cpu.program)
            with Lock:
                q.put(a)
                break

#
# The brute varian is to start multiple cores and let each
# core compute a set of start values for registerA
#
def solvePuzzle2Brute(filename):
    cpu = Cpu.CreateFromFile(filename, False)
 
    threads = 6        # Number of threads/cores
    numbers = 500000   # Number of values for registerA to try out pr thread

    runner:JobRunner = JobRunner(threads)
    for r in range(0,threads):
        s = r * numbers
        runner.AddToQueue( RunThreadPermutation, [s, numbers, cpu.program] )
    runner.RunQueue()

    ret = None
    allValues = runner.GetValues()
    for value in allValues:
        if ret == None or ret > value:
            ret = value

    n = (threads * numbers) / 1000000
    print_debug("Jobs done", ret, " tried: ", n, " million calculations with ", threads, " cores running ", numbers, " startvalues each")
    return ret


def solvePuzzle2(filename):
    cpu = Cpu.CreateFromFile(filename, False)

    j = 1
    istart = 0
    regA = 0
    while j <= len(cpu.program) and j >= 0:
        regA <<= 3
        for i in range(istart, 8):
            if cpu.program[-j:] == cpu.RunOnePermutation( regA + i ):
                break
        else:
            j -= 1
            regA >>= 3
            istart = (regA % 8) + 1
            regA >>= 3
            continue
        j += 1
        regA += i
        istart = 0
    return regA

if __name__ == '__main__':

    setupCode("Day 17: Chronospatial Computer")

#    UNITTEST.DEBUG_ENABLED = True

    unittest(solvePuzzle1, "4,6,3,5,6,3,5,2,1,0", "unittest1.txt")
    unittest(solvePuzzle2, 117440, "unittest2.txt")

#   Enable for fun :)
#    unittest(solvePuzzle2Brute, 117440, "unittest2.txt")
#    runCode(17,solvePuzzle2Brute, 105981155568026, "input.txt")

    runCode(17,solvePuzzle1, "1,5,0,3,7,3,0,3,1", "input.txt")
    runCode(17,solvePuzzle2, 105981155568026, "input.txt")

