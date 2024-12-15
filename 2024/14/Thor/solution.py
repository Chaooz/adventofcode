#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/0

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *
from advent_libs_matrix import *

setupCode("Day 14: Restroom Redoubt")

class Robot:
    def __init__(self, pos, vel, maxX, maxY):
        self.pos = pos
        self.vel = vel
        self.maxX = maxX
        self.maxY = maxY
                                                                                                                          
    def move(self):
        self.pos = self.pos + self.vel
        x = self.pos.x % self.maxX
        y = self.pos.y % self.maxY
        self.pos = Vector2(x,y)

    def print(self):
        print("Pos: " + self.pos.ToString() + " Vel: " + self.vel.ToString())

def printDebug(robots, maxX, maxY):
    # Overengineering 101
    colorList = list()
    colorList.append(("1", bcolors.YELLOW))
    colorList.append(("2", bcolors.WHITE))

    map = Matrix("debug", maxX, maxY, ".")
    for robot in robots:
        data = map.GetPoint(robot.pos)
        if data == ".":
            map.SetPoint(robot.pos, 1)
        else:
            map.SetPoint(robot.pos, data+1)
    map.PrintWithColor(colorList, bcolors.DARK_GREY, "", "")

#
# Create a list of robots
#
def createRobots(lines, maxX, maxY):
    robots = list()
    for line in lines:
        lineList = line.split(" ")

        sPosLine = lineList[0].split("=")
        sPos = sPosLine[1].split(",")

        sVelLine = lineList[1].split("=")
        sVel = sVelLine[1].split(",")

        pos = Vector2(int(sPos[0]), int(sPos[1]))
        vel = Vector2(int(sVel[0]), int(sVel[1]))

        robot = Robot(pos, vel, maxX, maxY)
        robots.append(robot)
    return robots

def solveLines(lines, maxX, maxY, numQuadrants, showDebug):
    robots = createRobots(lines, maxX, maxY)

    # Run for 100 seconds
    for rounds in range(0,100):
        for robot in robots:
            robot.move()

    x = int(maxX / 2)
    y = int(maxY / 2)

    q = dict()
    for n in range(numQuadrants):
        q[n] = 0

    for robot in robots:
        if robot.pos.x < x and robot.pos.y < y:
            q[0] += 1
        elif robot.pos.x < x and robot.pos.y > y:
            q[1] += 1
        elif robot.pos.x > x and robot.pos.y < y:
            q[2] += 1
        elif robot.pos.x > x and robot.pos.y > y:
            q[3] += 1

    sum = 1
    for n in range(numQuadrants):
        sum = sum * q[n]

    if showDebug:
        printDebug(robots, maxX, maxY)

    return sum

def solvePuzzle1Unittest(filename):
    lines = loadfile(filename)
    return solveLines(lines,11, 7, 4, UNITTEST.VISUAL_GRAPH_ENABLED)

def solvePuzzle1(filename):
    lines = loadfile(filename)
    return solveLines(lines,101, 103, 4, False)

# 
# Just see if we have many numbers next to each other
#
def robotsFormATree(robots, maxX, maxY, cache, groupNumber):
    # IF the tree starts at the top with 1
    # We check at least from the line with groupNumber / 2
    startY = int(groupNumber / 2)
    for y in range( startY, maxY):
        mxRobots = 0
        if cache[y] < groupNumber:
            continue

        robotsOnLine = [ robot for robot in robots if robot.pos.y == y]

        # Number of robots next to each other
        robotsOnLine.sort(key=lambda x: x.pos.x)

        for index in range(1, len(robotsOnLine)):
            robotA = robotsOnLine[index-1]
            robotB = robotsOnLine[index]

            if robotA.pos.x + 1 == robotB.pos.x:    
                mxRobots += 1
            else:
                mxRobots = 1

            if mxRobots >= groupNumber:
                return True

    return False


def solvePuzzle2(filename):

    lines = loadfile(filename)
    maxX = 101
    maxY = 103

    robots = createRobots(lines, maxX, maxY)

    # Run for 100 seconds
    round = 0
    # Make sure we don't run forever
    cache = dict()

    for y in range(0, maxY):
        cache[y] = 0

    # Add to cache
    for robot in robots:
        cache[robot.pos.y] += 1

    while round < 10000:
        round += 1
        for robot in robots:
            cache[robot.pos.y] -= 1
            robot.move()
            cache[robot.pos.y] += 1

        if robotsFormATree(robots, maxX, maxY, cache, 10):
#            print("Found at round: " + str(round))
            if UNITTEST.VISUAL_GRAPH_ENABLED:
                printDebug(robots, maxX, maxY)
            return round

    return -1

unittest(solvePuzzle1Unittest, 12, "unittest1.txt")
unittest(solvePuzzle2, -1, "unittest1.txt")

runCode(14,solvePuzzle1, 208437768, "input.txt")
runCode(14,solvePuzzle2, 7492, "input.txt")