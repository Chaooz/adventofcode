#!/usr/local/bin/python3
# https://adventofcode.com/2023/day/2

import sys
import math

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_vector2 import *
from advent_libs_matrix import *

print("")
print_color("Day 16: The Floor Will Be Lava", bcolors.OKGREEN)
print("")

#
# Raytrace from position in direction until we hit a wall
#
def raytrace(matrix:Matrix, position:Vector2, direction:Vector2, openPostion:str):
    while True:
        next_position = position + direction

        if matrix.IsOutOfBounds(next_position):
            #print("Out of bounds", position.ToString(), " => ", next_position.ToString() )
            return position

        if ( matrix.GetPoint(next_position) != openPostion):
            return next_position

        position = next_position

def set_path(matrix:Matrix, start_position:Vector2, end_position:Vector2, character:str, openPostion:str):
    direction = end_position - start_position
    if direction.x == 0 and direction.y == 0:
#        print("SetPath:Zero", start_position.ToString(), end_position.ToString())
        return

    old_character = matrix.GetPoint(start_position)
#    if old_character in [".","/","\\","|","-"]:
    matrix.Set(start_position.x, start_position.y, character)

    direction = direction.Normalize()
 #   print("SetPath", start_position.ToString(), end_position.ToString(), direction.ToString())
    while True:
        start_position = start_position + direction
        if matrix.IsOutOfBounds(start_position):
            return

        old_character = matrix.GetPoint(start_position)
#        if old_character in [".","/","\\","|","-"]:
        matrix.Set(start_position.x, start_position.y, character)
        if start_position == end_position:
            return


def traverse(id:int,matrix:Matrix, light_matrix:Matrix, position:Vector2, direction:Vector2):

    beams = list()
    beams.append((position,direction))

    loop = True
    while loop:
        loop = False

        for i in reversed(range(0,len(beams))):
            if beams[i] == None:
                continue

            loop = True

            position,direction = beams[i]
            mirror = matrix.Get(position.x, position.y)

            # We hit a mirror, change direction
            if mirror.find("/") != -1 and direction.x != 0:
                direction = Vector2(direction.y, -direction.x)
            elif mirror.find("/") != -1 and direction.x == 0:
                direction = Vector2(-direction.y, direction.x)
            elif mirror.find("\\") != -1:
                direction = Vector2(direction.y, direction.x)
            elif mirror.find("|") != -1 and direction.y == 0:
                direction = Vector2(0, -1)
                # Replace split with a I to avoid using this interception again
                matrix.SetPoint(position, "I")
                # Spawn a new ray in the other direction
                beams.append((position,Vector2(0,1)))
            elif mirror.find("-") != -1 and direction.x == 0:
                direction = Vector2(-1, 0)
                # Replace split with a = to avoid using this interception again
                matrix.SetPoint(position, "=")
                # Spawn a new ray in the other direction
                beams.append((position,Vector2(1,0)))
            # Stop at this splitter to avoid using it again (to avoid loop)
            elif mirror.find("=") != -1 and direction.x == 0:
                beams[i] = None
                continue
            # Stop at this splitter to avoid using it again (to avoid loop)
            elif mirror.find("I") != -1 and direction.y == 0:
                beams[i] = None
                continue

            nextPosition = raytrace(matrix, position, direction, ".")
            if nextPosition == position:
                beams[i] = None
                continue

            set_path(light_matrix, position, nextPosition, "#",".")
            position = nextPosition
            beams[i] = (position,direction)

def internal_solve(matrix:Matrix, position:Vector2, direction:Vector2):
    light_matrix  = matrix.Duplicate("LightMatrix")
    traverse(1,matrix,light_matrix,position, direction)

    sum = 0
    for y in range(light_matrix.sizeY):
        for x in range(light_matrix.sizeX):
            char = light_matrix.Get(x,y)
            if char == "#":
                sum += 1
#    print(position.ToString(), direction.ToString(), sum)
    return sum

def solvePuzzle1(filename):
    matrix  = Matrix.CreateFromFile(filename, ".")
    return internal_solve(matrix, Vector2(0,0), Vector2(1,0))

def solvePuzzle2(filename):

    max_sum = 0
    matrix  = Matrix.CreateFromFile(filename, ".")
#    return internal_solve(matrix, Vector2(3,0), Vector2(0,1))

    for y in range(matrix.sizeY):
        matrix_copy = matrix.Duplicate("MatrixCopy")
        sum = internal_solve(matrix_copy, Vector2(0,y), Vector2(1,0))
        max_sum = max(max_sum, sum)
        matrix_copy = matrix.Duplicate("MatrixCopy")
        sum = internal_solve(matrix_copy, Vector2(matrix.sizeX-1,y), Vector2(-1,0))
        max_sum = max(max_sum, sum)

    for x in range(matrix.sizeX):
        matrix_copy = matrix.Duplicate("MatrixCopy")
        sum = internal_solve(matrix_copy, Vector2(x,0), Vector2(0,1))
        max_sum = max(max_sum, sum)
        matrix_copy = matrix.Duplicate("MatrixCopy")
        sum = internal_solve(matrix_copy, Vector2(x,matrix.sizeY-1), Vector2(0,-1))
        max_sum = max(max_sum, sum)

    return max_sum

unittest(solvePuzzle1, 46, "unittest1.txt")     
unittest(solvePuzzle1, 7067, "input.txt")

unittest(solvePuzzle2, 51, "unittest1.txt")
unittest(solvePuzzle2, 7324, "input.txt")     

