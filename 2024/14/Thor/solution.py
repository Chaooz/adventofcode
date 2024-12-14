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
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel

    def move(self):
        self.pos = self.pos + self.vel

    def moveBack(self):
        self.pos = self.pos - self.vel

    def print(self):
        print("Pos: " + self.pos.print() + " Vel: " + self.vel.print())


def solvePuzzle1(filename):
    lines = loadfile(filename)

    map = Matrix("debug", 10, 7, ".")
    robots = list()

    for line in lines:
        pv = line.split(line, " ")
        sPos = pv[0].split(",")
        sVel = pv[1].split(",")

        pos = Vector2(int(sPos[0]), int(sPos[1]))
        vel = Vector2(int(sVel[0]), int(sVel[1]))

        robot = Robot(pos, vel)
        robots.append(robot)
        robot.print()

    return 0

def solvePuzzle2(filename):
    return 0

unittest(solvePuzzle1, -1, "unittest1.txt")
#unittest(solvePuzzle2, -1, "unittest1.txt")

#runCode(14,solvePuzzle1, -1, "input.txt")
#runCode(14,solvePuzzle2, -1, "input.txt")