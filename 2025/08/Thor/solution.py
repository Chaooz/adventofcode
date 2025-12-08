#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/24

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *
from advent_libs_vector3 import *

class BlockList:
    blockList:list[int]

    def __init__(self):
        self.blockList = list()

    def AddBlock(self, block):
        self.blockList.append(block)

    def HasBlock(self, block):
        return self.blockList.__contains__(block)
    
    def AddList(self, otherList:'BlockList'):
        self.blockList.extend(otherList.blockList)

    def ToString(self):
        ret = ""
        for block in self.blockList:
            if ret != "":
                ret += " - "
            ret += block.ToString()

        return ret
    def len(self):
        return len(self.blockList)


def createVectorList(filename) -> list[Vector3]:
    vectorList = []
    lines = loadfile(filename)

    for line in lines:
        line = line.strip()
        (x,y,z) = map(int, line.split(","))
        vectorList.append(Vector3(x,y,z))

    return vectorList

def createConnectionList(vectorList:list[Vector3], maxConnected=1000):
    connected = []

    # Create a list of connected points sorted by distance
    for i, thisPoint in enumerate(vectorList):
        for j, nextPoint in enumerate(vectorList):
            if i>j:
                dist = thisPoint.Distance(nextPoint)            
                connected.append( (dist, i, j) )

    # Sort list by distance
    connected.sort(key=lambda item: item[0])

    # Connect the first N closest points
    connectionList = []
    mx = min(maxConnected, len(connected))
    lastPoint = None
    for x in range(0, mx):
        (dist, indexA, indexB) = connected[x]

        blockListA:BlockList = None
        blockListB:BlockList = None

        # Find if either point is already in a block list
        for n in range(0, len(connectionList)):
            blockList:BlockList = connectionList[n]
            if blockList.HasBlock(indexA):
                blockListA = blockList
            if blockList.HasBlock(indexB):
                blockListB = blockList
            if blockListA is not None and blockListB is not None:
                break

        # If both are found, merge the lists
        if blockListA is not None and blockListB is not None:
            if blockListA != blockListB:
                lastPoint = (indexA, indexB)
                blockListA.AddList(blockListB)
                connectionList.remove(blockListB)
        elif blockListA is not None:
            lastPoint = (indexA, indexB)
            blockListA.AddBlock(indexB)
        elif blockListB is not None:
            lastPoint = (indexA, indexB)
            blockListB.AddBlock(indexA)
        else:
            lastPoint = (indexA, indexB)
            blockList = BlockList()
            blockList.AddBlock(indexA)
            blockList.AddBlock(indexB)
            connectionList.append(blockList)

    return connectionList, lastPoint

def solvePuzzle1(filename, maxConnected=1000):    
    vectorList = createVectorList(filename)
    connectionList, lastPoint = createConnectionList(vectorList, maxConnected)

    # Create a list sorted by size
    countedLists = list()
    for blockList in connectionList:
        blockLength = blockList.len()
        countedLists.append(( blockLength, blockList))
    countedLists.sort(key=lambda item: item[0], reverse=True)

    # Multiply the sizes of the 3 largest connected lists
    linkedcount = 1
    for index in range(0, min(3, len(countedLists))):
        blockList = countedLists[index][1]
        linkedcount *= blockList.len()

    return linkedcount

def solvePuzzle2(filename, maxConnected=200000):
    vectorList = createVectorList(filename)
    connectionList, lastPoint = createConnectionList(vectorList, maxConnected)
    indexA, indexB = lastPoint

    pointA = vectorList[indexA]
    pointB = vectorList[indexB]

    return pointA.x * pointB.x

setupCode("Day 8: Playground")

unittest_input(solvePuzzle1, 10, 40, "unittest1.txt")
unittest_input(solvePuzzle2, 10000, 25272, "unittest1.txt")

runCode(8,solvePuzzle1, 330786, "input.txt")
runCode(8,solvePuzzle2, 3276581616, "input.txt")