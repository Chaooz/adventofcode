#!/usr/local/bin/python3

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_list import *

stacks = []
moves = []

def organizeInput(inputfile):
    input = loadfile(inputfile)

    # Create padding
    for pIndex in range(0,100):
        stacks.append( "........." )

    for line in input:
        if line[0] == "m":
            # move 20 from 5 to 8
            (txt1,numberOfBoxes, txt2, moveFrom, txt3, moveTo ) = line.split(" ")
            moves.append( [ int(numberOfBoxes), int(moveFrom), int(moveTo) ] )

        elif line.strip() != "" and not line.startswith(" 1"):    
            row = "........."

            for index in range(0,len(line)):
                character = line[index]
                if character == "]":
                    boxLetter = line[index-1]
                    x = int(index / 4)
                    row = row[:x] + boxLetter + row[x + 1:]
            stacks.append(row)

    debugPrintStacks()
    #moveBoxes()
    moveMultiBoxes()
    debugPrintStacks()

    ll = ""
    for r in range(0,9):
        l = getLineNumberFromStack(r)
        box = replaceBox(r,l,".")
        ll += box
    print(ll)

# Hente index for når første bokstav starter


#     x0  x1  x2  x3 x4  x5  x6   x7  x8
# y0  x   x   x   x  [B]  x  [L]  x  [S]
# y1  x   x  [Q] [J] [C]  x  [W]  x  [F]

# move 1 from 2 to 3

def debugPrintStacks():
    startPrint = False
    for y in range(0,len(stacks)):
        row = stacks[y]
        if row != ".........":
            startPrint = True
        if startPrint:
            line = ""
            for index in range(len(row)):
                c = row[index]
                if ( c != "."):
                    line += "[" + c + "] "
                else:
                    line += "    "
            print(line)
    print("            ")

# move top 1 from x2 to x3
def getLineNumberFromStack(x):
    for y in range(0,len(stacks)):
        row = stacks[y]
        character = row[x]
        if character != ".":
            return y
    return len(stacks)

def replaceBox( x, y, newBox ):
    # Hente hele raden med bokser
    row = stacks[y]
    # Hente box som ligger på en spesifikk plass (x)
    oldBox = row[x]
#    row[x] = newBox
    #
    row = row[:x] + newBox + row[x + 1:]
    stacks[y] = row
    return oldBox

def moveBoxes():
    for move in moves:

        # Readability variables
        numberOfBoxes = move[0]
        moveFrom = move[1] - 1
        moveTo = move[2] - 1

        for number in range(0,numberOfBoxes):
            # Finne ut hvor stacks starter med bokstaver
            lineFrom = getLineNumberFromStack( moveFrom)
            lineTo = getLineNumberFromStack( moveTo) - 1
            # Hent box
            box = replaceBox(moveFrom, lineFrom, ".")
            check = replaceBox(moveTo, lineTo, box)

        print(" move " + str(numberOfBoxes) + " times " + str(moveFrom+1) + " => " + str(moveTo+1))
        #debugPrintStacks()

def moveMultiBoxes():
    for move in moves:

        # Readability variables
        numberOfBoxes = move[0]
        moveFrom = move[1] - 1
        moveTo = move[2] - 1

        # Finne ut hvor stacks starter med bokstaver
        lineFrom = getLineNumberFromStack( moveFrom)
        lineTo = getLineNumberFromStack( moveTo) - 1

        #  .   .   .
        # [D]  .   .    
        # [N] [C]  .
        # [Z] [M] [P]

        for number in range(0,numberOfBoxes):
            # Hent box
            box = replaceBox(moveFrom, lineFrom + (numberOfBoxes-1) - number, ".")
            check = replaceBox(moveTo, lineTo - number, box)
#            print(" move " + str(numberOfBoxes) + " times " + str(moveFrom+1) + " => " + str(moveTo+1) + " Box:" + box + " check:" + check)
#        debugPrintStacks()

organizeInput("puzzleinput.txt")
