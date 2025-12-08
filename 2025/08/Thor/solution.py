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
    blockList:list[Vector3]

    def __init__(self):
        self.blockList = list()

    def AddBlock(self, block):
        self.blockList.append(block)

    def HasBlock(self, block):
        return self.blockList.__contains__(block)
    
    def AddList(self, otherList:'BlockList'):
#        for block in otherList.blockList:
#            self.AddBlock(block)
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



def findClosestPoint(startVec:Vector3, vectorList:list[Vector3]) -> Vector3:
    foundVec = None
    foundDist = None
    for vec in vectorList:
        if vec == startVec:
            continue

        dist = vec.Distance(startVec)

        if foundVec is None:
            foundVec = vec
            foundDist = dist
        elif dist < foundDist:
            foundVec = vec
            foundDist = dist

    return foundVec

def createConnectionList(filename, maxConnected=1000):
    connected = list()
    lines = loadfile(filename)

    vectorList = list()
    checkList = list()

    for line in lines:
        line = line.strip()
        (x,y,z) = map(int, line.split(","))
        point = Vector3(x,y,z)
        vectorList.append(point)
        checkList.append(point)

    # Create a list of connected points sorted by distance
    for x in range(0, len(vectorList) - 1):
        thisPoint = vectorList[x]
        checkList.remove(thisPoint)

        for nextPoint in checkList:
            dist = thisPoint.Distance(nextPoint)            
            connected.append( (dist, thisPoint, nextPoint) )

#        shortestPoint = findClosestPoint(thisPoint, checkList)
#        dist = thisPoint.Distance(shortestPoint)
#        print(f"Distance from {thisPoint.ToString()} to {shortestPoint.ToString()} is {dist}")
#        connected.append( (dist, thisPoint, shortestPoint) )

    connected.sort(key=lambda item: item[0])

    # Connect the first N closest points
    connectionList = list()
    mx = min(maxConnected, len(connected))
    lastPoint = None
    for x in range(0, mx):
        (dist, pointA, pointB) = connected[x]

        blockListA:BlockList = None
        blockListB:BlockList = None
        for n in range(0, len(connectionList)):
            blockList:BlockList = connectionList[n]
            if blockList.HasBlock(pointA):
                blockListA = blockList
            if blockList.HasBlock(pointB):
                blockListB = blockList
            if blockListA is not None and blockListB is not None:
                break

        if blockListA is not None and blockListB is not None:
            if blockListA != blockListB:
                lastPoint = (pointA, pointB)
                blockListA.AddList(blockListB)
                connectionList.remove(blockListB)
        elif blockListA is not None:
            lastPoint = (pointA, pointB)
            blockListA.AddBlock(pointB)
        elif blockListB is not None:
            lastPoint = (pointA, pointB)
            blockListB.AddBlock(pointA)
        else:
            lastPoint = (pointA, pointB)
            blockList = BlockList()
            blockList.AddBlock(pointA)
            blockList.AddBlock(pointB)
            connectionList.append(blockList)
    return connectionList, lastPoint

def solvePuzzle1(filename, maxConnected=1000):    
    connectionList, lastPoint = createConnectionList(filename, maxConnected)

#    print("Total BlockLists:" + str(len(connectionList)))
    countedLists = list()
    for blockList in connectionList:
        blockLength = blockList.len()
        countedLists.append(( blockLength, blockList))
    countedLists.sort(key=lambda item: item[0], reverse=True)

    linkedcount = 1
#    print("Total CountedList:" + str(len(countedLists)))
    for index in range(0, min(3, len(countedLists))):
        blockList = countedLists[index][1]
#        print("Larger Blocklist # " +str(blockList.len()))
        linkedcount *= blockList.len()
#        print("Largest BlockList #" + str(index+1) + ":" + blockList.ToString() + " Size:" + str(blockList.len()))

#    print("Linked Nodes:" + str(linkedcount) + " of " + str(len(vectorList)))

    return linkedcount

def solvePuzzle2(filename, maxConnected=200000):
    connectionList, lastPoint = createConnectionList(filename, maxConnected)
    pointA, pointB = lastPoint

    print("Total CountedList:" + str(len(connectionList)))
#    print("Point A:" + pointA.ToString())
#    print("Point B:" + pointB.ToString())

    return pointA.x * pointB.x

setupCode("Day 8: Playground")

unittest_input(solvePuzzle1, 10, 40, "unittest1.txt")
unittest_input(solvePuzzle2, 10000, 25272, "unittest1.txt")

runCode(8,solvePuzzle1, 330786, "input.txt")
runCode(8,solvePuzzle2, 3276581616, "input.txt")