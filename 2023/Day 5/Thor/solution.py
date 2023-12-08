#!/usr/local/bin/python3
# https://adventofcode.com/2023/day/2

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_vector2 import *
from advent_libs_matrix import *

sys.setrecursionlimit(1500)

print("")
print_color("Day 5: If You Give A Seed A Fertilizer", bcolors.OKGREEN)
print("")

class Map:
    map : list
    def __init__(self) -> None:
        self.map = list()

    def Add(self,mat:list):
        self.map.append(mat)

    def Get(self,x:int,y:int) -> int:
        return self.map[y][x]

    def GetList(self):
        return self.map
    
    def Print(self):
        for mat in self.map:
            print(mat)


def convertData(name, seeds,map:Map):


    # Seed : 79 14 55 13
    # Soil : 50<-98 2
    # Soil : 52 50 48

    newData = list()

    if len(map) == 0:
        return seeds

#    print("---")
#    print(map)

    for seed in seeds:
        if seed == "":
            continue

        seed = int(seed)
        num = seed
        for mat in map:
            m = mat.split(" ")
            d = int(m[0])
            s = int(m[1])
            r = int(m[2])
            if seed >= s and seed < s + r:
                num = (seed - s) + d 

        newData.append(num)
        #print("Seed number ", seed, " corresponds to ",name," number", num)

    return newData
       

def solvePuzzle1(filename:str):
    lines = loadfile(filename)

    sum = 0
    seeds = list()

    mat = list()
    name = ""

    for line in lines:
        line = line.strip("\n")

        if len(line) == 0:
            continue

        if line.startswith("seeds:"):
            d = line.split(":")
            seeds = d[1].split(" ")

        elif line.find(":") >-1:
            seeds = convertData(name,seeds,mat)
            mat.clear()
            name = line

        elif line[0].isnumeric():
            mat.append(line)

    seeds = convertData(name,seeds,mat)

    low = -1
    for seed in seeds:
        if seed < low or low == -1:
            low = seed

    return low

def solvePuzzle2(filename:str):
    lines = loadfile(filename)
    sum = 0
    return sum

unittest(solvePuzzle1, 35, "unittest1.txt")
unittest(solvePuzzle1, 318728750, "input.txt")     

unittest(solvePuzzle2, 46, "unittest1.txt")
unittest(solvePuzzle2, 37384986, "input.txt")     
