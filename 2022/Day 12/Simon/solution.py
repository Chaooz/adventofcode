#!/usr/local/bin/python3

import sys
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_matrix import *
from advent_libs_path import *

matrix = Matrix.CreateFromFile(textfile="testinput.txt", defaultValue="@")
elevation = "SabcdefghijklmnopqrstuvwxyzE"

def getPosition(matrix:Matrix,character:str) -> Vector2:
    for y in range(0,matrix.sizeY):
        for x in range(0,matrix.sizeX):
            if matrix.Get(x,y) == character:
                return Vector2(x,y)
    return Vector2(-1,-1)

def getNeighbours(matrix:Matrix,position:Vector2) -> Vector2List:
    neighbours = Vector2List()
    for y in range(position.y-1,position.y+2):
        for x in range(position.x-1,position.x+2):
            if x == position.x and y == position.y:
                continue
            if x >= 0 and x < matrix.sizeX and y >= 0 and y < matrix.sizeY:
                neighbours.Add(Vector2(x,y))
    return neighbours

