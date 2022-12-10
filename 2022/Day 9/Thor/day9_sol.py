#
# 2022 Day 9: Rope Bridge
#

#!/usr/lib/python3
import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_matrix import *
from advent_libs_list import *

# Rules
# Tail is trying to follow Head
# Bridge is 5 . wide
# If head is in 90 degree angle away from tail. Tail moves directly up/down/left/right
# if the head is outside row/column the tail moves diagonally
# R 4  -> Move head 4 step to the right
# After each step move tail

bridgeWidth = 6
bridgeLength = 1000

def moveOneStep( matrix, position, direction, character ):
    posX = position[0]
    posY = position[1]

#    oldPos = (posX,posY)
    posX += direction[0]
    posY += direction[1]

    if posX >= bridgeWidth:
        posX = 0
        posY += 1
    elif posX < 0:
        posX = bridgeWidth - 1
        posY -= 1

#    print("move:" + str(oldPos[0]) + "x" + str(oldPos[1]) + " => " + str(posX) + "x" + str(posY))

    if posX >= 0 and posX < bridgeWidth and posY >= 0 and posY < bridgeLength:
        if character == "":
            matrix[posX][posY] += 1
    else:
        print_warning("outside:" + str(posX) + "x" + str(posY))

    return (posX,posY)

# Follow Position
def followPosition(matrix, startPos, endPos, character):

    posX = startPos[0]
    posY = startPos[1]

    # If we have to go diagonally
    if posX != endPos[0] and posY != endPos[1] and 2==1:
        # Go diagonally
        print_warning("Dialognal!!")
        pass
    else:
        dirX = endPos[0] - posX
        dirY = endPos[1] - posY

        if dirX < 0:
            posX -= 1
        elif dirX > 0:
            posX += 1
       
        if dirY < 0 :
            posY -=1
        elif dirY > 0:
            posY += 1

        # Cannot go into head
        if posX == endPos[0] and posY == endPos[1]:
            return startPos

#        print("move" + str(startPos[0]) + "x" + str(startPos[1]) + " => " + str(endPos[0]) + "x" + str(endPos[1]) + " end:" + str(posX) + "x" + str(posY))

    if character != "":
        SetMatrixPoint(matrix,posX,posY,character)

    return (posX,posY)
       
def SetMatrixPoint(matrix, x, y, character ):
    if x >= 0 and x < bridgeWidth and y >= 0 and y < bridgeLength:
        matrix[x][y] = character
    else:
        print_warning("SetMatrixPoint : " + str(x) + "x" + str(y) + " is outsde of matrix")

# Move both Head and Tail x steps with the move command
def moveSquare( matrix, debug, head, tail, direction, steps, character ):
    if debug:
        matrix[tail[0]][tail[1]] =  " T "
        matrix[head[0]][head[1]] =  " H "
        print_matrix_color("moveSquare:Start", matrix, 0, bcolors.DARK_GREY, "   ", " " )

    for step in range(0,steps):
        if debug:
            matrix[head[0]][head[1]] =  " . "
            matrix[tail[0]][tail[1]] =  " . "

        head = moveOneStep(matrix, head, direction, character)
        tail = followPosition(matrix, tail, head, character)

        if debug:
            matrix[tail[0]][tail[1]] =  " T "
            matrix[head[0]][head[1]] =  " H "
            print_matrix_color("moveSquare:" + str(step), matrix, 0, bcolors.DARK_GREY, "   ", " " )

    return (head,tail)

# Execute a move order
def moveOrder( matrix, debug, order, head, tail, steps, character ):
    if order == "R":
        head,tail = moveSquare(matrix, debug, head, tail, (1,0), steps, character)
    elif order == "L":
        head,tail = moveSquare(matrix, debug, head, tail, (-1,0), steps, character)
    elif order == "D":
        head,tail = moveSquare(matrix, debug, head, tail, (0,1), steps, character)
    elif order == "U":
        head,tail = moveSquare(matrix, debug, head, tail, (0,-1), steps, character)
    return head, tail

#
# calcVisitedSteps
# @Matrix matrix - The matrix to find number of steps in
#
def calcVisitedSteps(matrix):
    numVisits = 1
    for x in range(0, bridgeWidth):
        for y in range(0,bridgeLength):
            if ( matrix[x][y] == "#" ):
                numVisits += 1
    return numVisits

#
#
#
def testMove(order, input):
    global bridgeWidth
    global bridgeLength

    start, head, tail, debug = input.split(",")
    start = ( int(start[0]), int(start[2]))
    head = ( int(head[0]), int(head[2]))
    tail = ( int(tail[0]), int(tail[2]))
    debug = debug == "True"

    matrix = create_empty_matrix( bridgeWidth, 10, " . ")
    parts = order.split(" ")
    steps = int(parts[1])
    head,tail = moveOrder(matrix, debug, parts[0], head, tail, steps, " # ")

    # Mark these positions
    matrix[start[0]][start[1]] = " s "
    matrix[tail[0]][tail[1]] = " T "
    matrix[head[0]][head[1]] = " H "
    if debug:
        print_matrix_color("Order:" + order + " - ", matrix, 0, bcolors.DARK_GREY, "   ", " " )
    return 0

def solvePuzzle1(filename):
    global bridgeWidth
    global bridgeLength

    matrix = create_empty_matrix( bridgeWidth, bridgeLength, "  .")
    lines = loadfile(filename)
    y = int(bridgeLength/2)
    startPos = (0,y)
    start = startPos
    tail = startPos
    head = startPos

    for move in lines:
        parts = move.split(" ")
        steps = int(parts[1])
        head,tail = moveOrder(matrix, False, parts[0], head, tail, steps, "#")

    matrix[start[0]][start[1]] = "s"

    #print_matrix_color("Bridge", matrix, " . ", bcolors.DARK_GREY, "   ", " " )
    return calcVisitedSteps(matrix)

def solvePuzzle2(filename):
    return 0

print("")
print_color("Day 9: Rope Bridge", bcolors.OKGREEN)
print("")

debug = "False"
#unittest_input(testMove, "0 5,0 5,0 5," + debug, (4,5), "R 4")
#unittest_input(testMove, "0 5,4 5,3 5," + debug, 0, "U 4")
#unittest_input(testMove, "0 5,4 0,4 1," + debug, 0, "L 3")
#unittest_input(testMove, "0 5,1 0,2 0," + debug, 0, "D 1")
#unittest_input(testMove, "0 5,1 1,2 0," + debug, 0, "R 4")
#unittest_input(testMove, "0 5,5 1,4 1," + debug, 0, "D 1")
#unittest_input(testMove, "0 5,5 2,4 1," + debug, 0, "L 5")
#unittest_input(testMove, "0 5,0 2,1 2," + debug, 0, "R 2")

unittest(solvePuzzle1, 13, "unittest.txt")
#unittest(solvePuzzle2, 1, "unittest.txt")
unittest(solvePuzzle1, 13, "puzzleinput_work.txt")
#unittest(solvePuzzle2, 1, "puzzleinput_work.txt")
