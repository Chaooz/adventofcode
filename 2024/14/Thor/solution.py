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
#        x = self.pos.x % maxX
#        y = self.pos.y % maxY
 #       self.pos = Vector2(x,y)
                                                                                                                          
    def move(self):
        self.pos = self.pos + self.vel
        x = self.pos.x % self.maxX
        y = self.pos.y % self.maxY
        self.pos = Vector2(x,y)

#    def moveBack(self):
#        self.pos = self.pos - self.vel

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
    map.PrintWithColor(colorList, bcolors.DARK_GREY, "  ", "  ")

def solveLines(lines, maxX, maxY, numQuadrants, showDebug):

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

def solvePuzzle2(filename):
    return 0

unittest(solvePuzzle1Unittest, 12, "unittest1.txt")
#unittest(solvePuzzle2, -1, "unittest1.txt")

runCode(14,solvePuzzle1, 208437768, "input.txt") # Too low
#runCode(14,solvePuzzle2, -1, "input.txt")