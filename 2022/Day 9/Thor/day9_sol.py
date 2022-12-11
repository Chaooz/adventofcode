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
from advent_libs_vector2 import *

# Rules
# Tail is trying to follow Head
# Bridge is 5 . wide
# If head is in 90 degree angle away from tail. Tail moves directly up/down/left/right
# if the head is outside row/column the tail moves diagonally
# R 4  -> Move head 4 step to the right
# After each step move tail

bridgeWidth = 6
bridgeLength = 1000

#
# getDirection
# @str dir - The direction in RLDU letters
# return Vector with direction
#
def getDirection(dir:str):
    if dir == "R": return Vector2(1,0)
    elif dir == "L": return Vector2(-1,0)
    elif dir == "D": return Vector2(0,1)
    elif dir == "U": return Vector2(0,-1)
    return Vector2(0,0)

def isNeighbour(pos1,pos2):
    return abs(pos2.x - pos1.x) < 2 and abs(pos2.y - pos1.y) < 2

def moveHead( list:Vector2List, position: Vector2, direction: Vector2, steps:int, maxWidth:int) -> Vector2List:
    for index in range(0,steps):
        position += direction
#        if position.x > maxWidth:
#            position.y += int( position.x / maxWidth )
#        elif position.x < 0:
#            position.y -= 1
#            position.x += maxWidth
#            if position.x < 0:
#                print_warning("moveHead: broken!")
#        position.x %= maxWidth
        list.append(position)
    return position

def solveInternalPuzzle(name, moveList, debug, head, tail):
    headList = Vector2List("head")
    headList.append(head)

    tailList = Vector2List("tail")
    tailList.append(tail)

    # Move head
    position = head
    for index in range(0, len(moveList)):
        move = moveList[index]
        direction = getDirection(move[0])
        position = moveHead( headList, position, direction, int(move[1]), 6 )

    # Make tail follow head
    tailPos = tail
    for index in range(0, headList.len()):
        headPos = headList.Get(index)
        if isNeighbour(headPos,tailPos):
            continue
        tailPos = headList.Get(index-1)
        if tailList.GetWithPos(tailPos) == None:
            tailList.append(tailPos)

    # Debug print matrix with head movements
    if debug:
        matrixHead = Matrix(name + ":Head", bridgeWidth, 10, ".")
        matrixHead.InsertFromVector2List(headList,"#")
        matrixHead.Print("#", bcolors.WHITE)

        # Debug print matrix with movements
        matrixTail = Matrix(name + ":Tail",bridgeWidth, 10, 0)
        matrixTail.InsertFromVector2List(tailList, "")
        matrixTail.Print("0", bcolors.DARK_GREY)

        headList.Print()

    return tailList.len()

#
#
#
def testMove(order, input):
    head, tail, debug = input.split(",")
    head = Vector2( int(head[0]), int(head[2]))
    tail = Vector2( int(tail[0]), int(tail[2]))
    debug = debug == "True"

    moveList = list()
    moveList.append( order.split(" "))

    return solveInternalPuzzle(order, moveList, debug, head, tail)

def solvePuzzle1(filename):
    moveList = listFromFile(filename, " ")

#    newList = list()
#    for index in range(0,5):
#        move = moveList[index]
#        newList.append(move)

    return solveInternalPuzzle("solvePuzzle1", moveList, False, Vector2(0,250), Vector2(0,250))

def solvePuzzle2(filename):
    return 0

print("")
print_color("Day 9: Rope Bridge", bcolors.OKGREEN)
print("")

debug = "False"
unittest_input(testMove, "0 5,0 5," + debug, 4, "R 4")
unittest_input(testMove, "4 5,3 5," + debug, 4, "U 4")
unittest_input(testMove, "4 0,4 1," + debug, 0, "L 3")
unittest_input(testMove, "1 0,2 0," + debug, 0, "D 1")
unittest_input(testMove, "1 1,2 0," + debug, 0, "R 4")
unittest_input(testMove, "5 1,4 1," + debug, 0, "D 1")
unittest_input(testMove, "5 2,4 1," + debug, 0, "L 5")
unittest_input(testMove, "0 2,1 2," + debug, 0, "R 2")

unittest(solvePuzzle1, 13, "unittest.txt")
unittest(solvePuzzle1, 5, "unittest2.txt")
#unittest(solvePuzzle2, 1, "unittest.txt")
unittest(solvePuzzle1, 3488, "puzzleinput.txt") # 3488 = TooLow
unittest(solvePuzzle1, 3488, "puzzleinput_work.txt") # 3488 = TooLow
#unittest(solvePuzzle2, 1, "puzzleinput_work.txt")
