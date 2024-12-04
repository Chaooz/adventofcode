#!/usr/local/bin/python3
# https://adventofcode.com/2023/day/18

import sys
import math

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_vector2 import *
from advent_libs_matrix import *
from advent_libs_pathfinding import *

#sys.setrecursionlimit(2500)

setupCode("Day 18: Lavaduct Lagoon")

def matrix_draw(matrix:Matrix, position:Vector2, direction:Vector2, steps:int, character:str):
    for i in range(int(steps)):
        position = position + direction
#        if matrix.IsOutOfBounds(position) == False:
        matrix.SetPoint(position,character)
    return position

def solvePuzzle1(filename, args):
    sum = 0
    lines = loadfile(filename)
    sizeX = int(args[0])
    sizeY = int(args[1])
    posX = int(args[2])
    posY = int(args[3])
    rate = args[4]  
    matrix = Matrix("Lava", sizeX, sizeY, ".")

    startPos = Vector2(posX,posY)
    nextPos = startPos
    for line in lines:
        direction_name, steps, color = line.split(" ")
        if direction_name == "R":
            direction = Vector2(1,0)
        elif direction_name == "D":
            direction = Vector2(0,1)
        elif direction_name == "L":
            direction = Vector2(-1,0)   
        elif direction_name == "U":
            direction = Vector2(0,-1)

        nextPos = matrix_draw(matrix,nextPos, direction, steps, "#")

#    matrix.FillArea(startPos, ".", "#")
#    matrix.FillArea(startPos, ".", "/")

    matrix.FillAreaOuter(Vector2(10,10), "#", "/")

    smallMatrix = matrix
    if rate > 1:
        smallMatrix = matrix.GetScaledMatrix(rate, ".")

    colorList = list()
    colorList.append(("O", bcolors.WHITE))
    colorList.append(("#", bcolors.DARK_GREY))
#    smallMatrix.PrintWithColor(colorList, bcolors.DARK_GREY , " ", "")

    sum = matrix.Count("#")
    sum += matrix.Count(".")
    return sum

def GetAreaSize(point_list:list):
    perimiter = 0
    area = 0
    pLen = len(point_list)

    pOld = Vector2(0,0)
    for i in range(pLen):    
        diff = point_list[i] - pOld
        perimiter += abs(diff.x)
        perimiter += abs(diff.y)
        pOld = point_list[i]

    for i in range(pLen):    
        area -= point_list[i].x * point_list[(i+1) % pLen].y
        area += point_list[i].y * point_list[(i+1) % pLen].x

    perimiter //= 2 # Square Root
    area //= 2

    return area + perimiter + 1

def solvePuzzle1b(filename):
    lines = loadfile(filename)

    pos = Vector2(0,0)
    point_list = list()
    perimiter = 0
    for line in lines:
        direction, length, hex = line.split(" ")
        if direction == "R":
            pos += Vector2(int(length),0)
        elif direction == "D":
            pos += Vector2(0,-int(length))
        elif direction == "L":
            pos += Vector2(-int(length),0)
        elif direction == "U":
            pos += Vector2(0,int(length))
        perimiter += int(length)
        point_list.append(pos)
    perimiter //= 2

    return GetAreaSize(point_list)


def solvePuzzle2(filename):
    lines = loadfile(filename)

    pos = Vector2(0,0)
    point_list = list()
    perimiter = 0
    for line in lines:
        direction, length, hex = line.split(" ")
        direction = {0: 'R', 1: 'D', 2: 'L', 3: 'U'}[int(hex[-2])]
        length = int(hex[2:-2], 16)

        if direction == "R":
            pos += Vector2(int(length),0)
        elif direction == "D":
            pos += Vector2(0,-int(length))
        elif direction == "L":
            pos += Vector2(-int(length),0)
        elif direction == "U":
            pos += Vector2(0,int(length))
        perimiter += int(length)
        point_list.append(pos)
    perimiter //= 2

    return GetAreaSize(point_list)

unittest_input(solvePuzzle1, (20,20,0,0,1), 62, "unittest1.txt")     
unittest_input(solvePuzzle1, (520,350,120,220,5),67891, "input.txt")     # 66513 too low

unittest(solvePuzzle1b, 62, "unittest1.txt")
unittest(solvePuzzle2, 952408144115, "unittest1.txt")

runCode(18,solvePuzzle1b, 67891, "input.txt")
runCode(18,solvePuzzle2, 94116351948493, "input.txt")     

