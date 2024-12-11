#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/09

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *
from advent_libs_linkedlist import *

setupCode("Day 9: Disk Fragmenter")

MAX_INTERATIONS = 100000000

class BlockType:
    DATA = 0
    FREE = 1

    def GetName(blockType:int):
        if blockType == BlockType.DATA:
            return "DATA"
        return "FREE"

class Block(LinkedElement):
    GlobalID:int = 0
    id: int
    length:int
    blockType: BlockType

    def __init__(self, length:int, blockType:BlockType):
        LinkedElement.__init__(self)
        self.length = length
        self.blockType = blockType
        self.id = -1
        if blockType == BlockType.DATA:
            self.id = Block.GlobalID
            Block.GlobalID = Block.GlobalID + 1

    def SetData(self, length):
        self.length = length

    def FreeData(self, length):
        self.length = self.length - length
           
    def ToString(self):
        extra = ""
        if self.prev is not None:
            extra = extra + " Prev:" + str(self.prev.elementId)
        if self.next is not None:
            extra = extra + " Next:" + str(self.next.elementId)
        blockName = BlockType.GetName(self.blockType)
        return "[ID:" + str(self.elementId) + extra + " Data:" + str(self.id) + "/" + str(self.length) + "/" + blockName + "]"


class Disk(LinkedList):

    def GetFreeBlock(self, allocateBlock:LinkedElement, useSize:bool):
        element = self.firstElement
        while element is not None:
            if element.blockType == BlockType.FREE and ( useSize == False or element.length >= allocateBlock.length):
                return element

            if element == allocateBlock:
                return None

            element = element.next
        return None
    
    def CalculateChecksum(self):
        sum = 0
        index = 0
        element = self.firstElement
        maxIterations = 0
        while element is not None:
            maxIterations = maxIterations + 1
            if maxIterations > MAX_INTERATIONS:
                print_assert(False,"CalcChecksum: ERROR: Too many iterations")
                return -1
            
            if element.blockType == BlockType.FREE:
                return sum
            for j in range(0,element.length):
                sum = sum + ( index * element.id)
                index = index + 1

            element = element.next
        return sum
    
#
#
#
#

def createDiskFromString(input) -> Disk:
    disk:Disk = Disk()
    for index in range(0,len(input)):
        char = input[index]
        dataLength = int(char)
        if index % 2 == 0:
            block = Block(dataLength, BlockType.DATA)
        else:
            block = Block(dataLength, BlockType.FREE)

        disk.AddBlock(block)

    return disk

def fragmentDisk1(disk:Disk) -> Disk:

    dataBlock = disk.lastElement
    skippedBlocks = 0

    runIterations = 0

#    disk.PrintDebug("Run: " + str(runIterations))

    while True:

        # Cannot fragment anymore
        if dataBlock is None:
            return disk

        runIterations = runIterations + 1
        if runIterations > MAX_INTERATIONS:
            print_assert(False, "ERROR: Too many iterations: " + str(runIterations) + " #" + str(disk.numElements) + " skipped: " + str(skippedBlocks))
           
            return disk

        # Skip free blocks
        if dataBlock.blockType == BlockType.FREE:
#            print("skip free ...", dataBlock.ToString())
            dataBlock = dataBlock.prev
            skippedBlocks = skippedBlocks + 1
            if skippedBlocks > MAX_INTERATIONS:
                print_assert(False,"ERROR: Too many skipped blocks")
                disk.PrintDebug("Too many skipped blocks")
                return disk
            
#            if dataBlock is not None:
#                disk.DeleteElement(dataBlock.next)
            
            continue

        freeBlock = disk.GetFreeBlock(dataBlock, False)

        # No free blocks -> return disk
        if freeBlock is None:
            return disk
        skippedBlocks = 0

        # If the free block is right after the datablock we are done
        if (dataBlock.next == freeBlock and freeBlock.prev == dataBlock):
#            print("### DONE ###", dataBlock.ToString(), freeBlock.ToString())
            return disk

        # If the free block is the same size as the data block
        elif freeBlock.length == dataBlock.length:
#            print("")
#            print("### SWAP ###", dataBlock.ToString(), freeBlock.ToString())
#            print("")
            disk.Swap(dataBlock, freeBlock)
            dataBlock = freeBlock

        # If the free block is larger than the data block
        elif freeBlock.length > dataBlock.length:
#            print("")
#            print("### FREE > DATA ###", dataBlock.ToString(), freeBlock.ToString())
#            print("")

            # Split the free block into two blocks
            newFreeBlock = Block(freeBlock.length - dataBlock.length, BlockType.FREE)
            freeBlock.FreeData(dataBlock.length)
            disk.InsertAfterBlock(freeBlock, newFreeBlock)

            disk.Swap(dataBlock, freeBlock)
            dataBlock = freeBlock

        # If the free block is smaller than the data block
        elif freeBlock.length < dataBlock.length:
#            print("")
#            print("### FREE < DATA ###", dataBlock.ToString(), freeBlock.ToString())
#            print("")

            # Split the datablock into two blocks
            newDataBlock = Block(dataBlock.length - freeBlock.length, BlockType.DATA)
            newDataBlock.id = dataBlock.id
            dataBlock.SetData(freeBlock.length)
            disk.InsertAfterBlock(dataBlock, newDataBlock)

            # Swap the free block and the first data black
            disk.Swap(dataBlock, freeBlock)
            dataBlock = freeBlock


    return disk

def fragmentDisk2(disk:Disk) -> Disk:

    dataBlock = disk.lastElement
    skippedBlocks = 0
    runIterations = 0

    while True:

        # Cannot fragment anymore
        if dataBlock is None:
            return disk

        runIterations = runIterations + 1
        if runIterations > MAX_INTERATIONS:
            print_assert(False, "ERROR: Too many iterations: " + str(runIterations) + " #" + str(disk.numElements) + " skipped: " + str(skippedBlocks))
           
            return disk

        # Skip free blocks
        if dataBlock.blockType == BlockType.FREE:
#            print("skip free ...", dataBlock.ToString())
            dataBlock = dataBlock.prev
            skippedBlocks = skippedBlocks + 1
            if skippedBlocks > MAX_INTERATIONS:
                print_assert(False,"ERROR: Too many skipped blocks")
                disk.PrintDebug("Too many skipped blocks")
                return disk
            
            continue

        freeBlock = disk.GetFreeBlock(dataBlock, True)

        # No free blocks -> return disk
        if freeBlock is None:
            print("ERROR: No free blocks: Should move to next datablock")
            continue
        skippedBlocks = 0

        # If the free block is right after the datablock we are done
        if (dataBlock.next == freeBlock and freeBlock.prev == dataBlock):
#            print("### DONE ###", dataBlock.ToString(), freeBlock.ToString())
            return disk

        # If the free block is the same size as the data block
        elif freeBlock.length == dataBlock.length:
#            print("")
#            print("### SWAP ###", dataBlock.ToString(), freeBlock.ToString())
#            print("")
            disk.Swap(dataBlock, freeBlock)
            dataBlock = freeBlock

        # If the free block is larger than the data block
        elif freeBlock.length > dataBlock.length:
#            print("")
#            print("### FREE > DATA ###", dataBlock.ToString(), freeBlock.ToString())
#            print("")

            # Split the free block into two blocks
            newFreeBlock = Block(freeBlock.length - dataBlock.length, BlockType.FREE)
            freeBlock.FreeData(dataBlock.length)
            disk.InsertAfterBlock(freeBlock, newFreeBlock)

            disk.Swap(dataBlock, freeBlock)
            dataBlock = freeBlock

        # If the free block is smaller than the data block
        elif freeBlock.length < dataBlock.length:
#            print("")
#            print("### FREE < DATA ###", dataBlock.ToString(), freeBlock.ToString())
#            print("")

            # Split the datablock into two blocks
            newDataBlock = Block(dataBlock.length - freeBlock.length, BlockType.DATA)
            newDataBlock.id = dataBlock.id
            dataBlock.SetData(freeBlock.length)
            disk.InsertAfterBlock(dataBlock, newDataBlock)

            # Swap the free block and the first data black
            disk.Swap(dataBlock, freeBlock)
            dataBlock = newDataBlock

    return disk

def GetDiskHash(disk:Disk):
    element = disk.firstElement
    c = ""
    while element is not None:
        for j in range(0,element.length):
            d = "."
            if element.blockType == BlockType.DATA:
                d = str(element.id)
            c = c + d
        element = element.next
    return c

def solvePuzzle1(filename):
    line = loadfile_as_string(filename)

    disk = createDiskFromString(line)
#    lineHash = GetDiskHash(disk)
#    print("create disk", lineHash)

    disk = fragmentDisk1(disk)
#    lineHash = GetDiskHash(disk)
#    print("fragmented:", lineHash)

    disk.PrintDebug("Fragmented disk", 100)
#    disk.PrintReversedDebug("Fragmented disk", 10)

    return disk.CalculateChecksum()

def solvePuzzle2(filename):
    line = loadfile_as_string(filename)

    disk = createDiskFromString(line)
#    lineHash = GetDiskHash(disk)
#    print("create disk", lineHash)

    disk = fragmentDisk2(disk)
#    lineHash = GetDiskHash(disk)
#    print("fragmented:", lineHash)

    disk.PrintDebug("Fragmented disk", 10)
    disk.PrintReversedDebug("Fragmented disk", 10)

    return disk.CalculateChecksum()

#unittest(resolveFragementedDisk, "00...111...2...333.44.5555.6666.777.888899", "2333133121414131402")
#unittest(calculateChecksum, 1928, "0099811188827773336446555566..............")

unittest(solvePuzzle1, 1928, "unittest1.txt")
#unittest(solvePuzzle2, -1, "unittest1.txt")

#runCode(9,solvePuzzle1, 6378826667552, "input.txt") # Too low
#runCode(9,solvePuzzle2, 6413328569890, "input.txt")