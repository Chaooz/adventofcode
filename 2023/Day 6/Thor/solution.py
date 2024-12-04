#!/usr/local/bin/python3
# https://adventofcode.com/2023/day/2

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_vector2 import *
from advent_libs_matrix import *

sys.setrecursionlimit(1500)

setupCode("Day 6: Wait For It")

def runRace(raceTime:int, distance:int):
    numWays = 0
    for i in range(0,raceTime):
        r = raceTime - i
        d = (i * r)
        if d > distance:
            numWays += 1
    return numWays

def solvePuzzle1(filename:str):
    lines = loadfile(filename)

    raceTime = list()
    distance = list()

    for line in lines:
        line = line.replace("\n", "")

        if line.startswith("Time:"):
            rTime = line.split(":")[1].split(" ")
            for r in rTime:
                if r == "":
                    continue
                raceTime.append(int(r))

        if line.startswith("Distance:"):
            rDist = line.split(":")[1].split(" ")
            for r in rDist:
                if r == "":
                    continue
                distance.append(int(r))

    sum = 1
    for i in range(0, len(raceTime)):
        rTime = raceTime[i]
        rDist = distance[i]
        sum *= runRace(rTime,rDist)

    return sum

def solvePuzzle2(filename:str):
    lines = loadfile(filename)
    sum = 0

    raceTime = ""
    distance = ""

    for line in lines:
        line = line.replace("\n", "")

        if line.startswith("Time:"):
            rTime = line.split(":")[1].split(" ")
            for r in rTime:
                if r == "":
                    continue
                raceTime += r

        if line.startswith("Distance:"):
            rDist = line.split(":")[1].split(" ")
            for r in rDist:
                if r == "":
                    continue
                distance += r

    sum = runRace(int(raceTime),int(distance))
    return sum

unittest(solvePuzzle1, 288, "unittest1.txt")
unittest(solvePuzzle2, 71503, "unittest1.txt")

runCode(6,solvePuzzle1, 170000, "input.txt")     
runCode(6,solvePuzzle2, 20537782, "input.txt")
