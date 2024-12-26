#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/08

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *
from advent_libs_matrix import *

setupCode("Day 8: Resonant Collinearity")

class RadioTower:

    t = 0
    name:str
    positions:list

    def __init__(self, name:str, position):
        self.positions = []
        self.name = name
        self.positions.append(position)          
        self.t = self.t + 1

    def AddPosition(self,position):
        self.positions.append(position)          

    def ToString(self):
        return self.name + " " + str(self.positions)

def addRadioTower(radios,name,position):
    # nodes[grid[i][j]] = nodes.get(grid[i][j], []) + [(i,j)]
    radioTower = getRadioTower(radios,name)
    if radioTower is not None:
        radioTower.AddPosition(position)
        return
#    print("Adding radio tower", name, position)
    radios.append(RadioTower(name,position))

def getRadioTower(radios, name:str) -> RadioTower:
    for radio in radios:
        if radio.name == name:
            return radio
    return None

def solveAllAntinodes(filename, maxAntinodes):
    matrix = Matrix.CreateFromFile(filename)

    # Build a list of radio towers (unqiue names)
    # with a list of positions
    radioTowerList = []
    for x in range(0,matrix.height):
        for y in range(0,matrix.width):
            character = matrix.Get(x,y)
            if character != ".":
                addRadioTower(radioTowerList,str(character),Vector2(x,y))

    # A set will have a unique key, meaning two antinodes will not be counted twice
    aninodeList = set()

    # Check all radio tower types
    for radio in radioTowerList:
        radioLength = len(radio.positions)
        for index1 in range(0,radioLength):
            for index2 in range(0, index1):
                pos1 = radio.positions[index1]
                pos2 = radio.positions[index2]

                diff = pos2 - pos1

                antinode1 = pos1 - diff
                antinode2 = pos2 + diff

                # Assignment 2, also have to add the tower
                if maxAntinodes > 1:
                    aninodeList.add((pos1.x,pos1.y))
                    aninodeList.add((pos2.x,pos2.y))

                # Calculate the antinode positions in a line between the two radio towers
                numIterations1 = 0
                while numIterations1 < maxAntinodes and matrix.IsPointInside(antinode1):
                    aninodeList.add((antinode1.x,antinode1.y))
                    antinode1 = antinode1 - diff
                    numIterations1 = numIterations1 + 1

                # Calculate the antinode positions in a line between the two radio towers
                numIterations2 = 0
                while numIterations2 < maxAntinodes and matrix.IsPointInside(antinode2):
                    aninodeList.add((antinode2.x,antinode2.y))
                    antinode2 = antinode2 + diff
                    numIterations2 = numIterations2 + 1

    return len(aninodeList)

def solvePuzzle1(filename):
    return solveAllAntinodes(filename, 1)

def solvePuzzle2(filename):
    return solveAllAntinodes(filename, 1000000)

unittest(solvePuzzle1, 14, "unittest1.txt")
unittest(solvePuzzle2, 34, "unittest1.txt")

runCode(8,solvePuzzle1, 426, "input.txt") # 410 too low
runCode(8,solvePuzzle2, 1359, "input.txt")