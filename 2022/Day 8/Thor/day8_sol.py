#
# 2022 Day 8: Treetop Tree House
#

# Rules
# Must delete files
# 70000000 is max space
# Need at least 70000000

#!/usr/lib/python3
import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_matrix import *

print("")
print_color("Day 8: Treetop Tree House", bcolors.OKGREEN)
print("")

def LineOfSight(matrix, position, direction, character ):

    posX = position[0]
    posY = position[1]

    size = get_matrix_size(matrix)
    highestTree = matrix[posX][posY]

    if highestTree == "U" or highestTree == "D" or highestTree == "L" or highestTree == "R":
#        print("[!] Startbug: " + str(posX) + "x" + str(posY) + " high:" + str(highestTree) + " : " + character)
        return 0

    numTree = 1
    matrix[posX][posY] = character + highestTree

    while(True):
        posX += direction[0]
        posY += direction[1]

        # Outside of Matrix ?
        if posX < 0 or posX > size[0]-1 or posY < 0 or posY > size[1]-1:
#            print("[  ] End of line : " + str(posX) + "x" + str(posY) + " highest:" + str(highestTree) + " => " + str(numTree) + " (" + character + ")")
            #matrix[posX][posY] = numTree
            return numTree

        thisTree = matrix[posX][posY]

        # Visible from the other side
        if thisTree[0] == "U" or thisTree[0] == "D" or thisTree[0] == "L" or thisTree[0] == "R":
#            print("[OK] Visible from other side : " + str(posX) + "x" + str(posY) + " high:" + str(highestTree) + " new:" + str(thisTree) + " => " + str(numTree))
#            return numTree
            thisTree = thisTree[1]
            if highestTree < thisTree:
                highestTree = thisTree
            continue

        if highestTree < thisTree:
#            print("[OK] Tree is higher : " + str(posX) + "x" + str(posY) + " high:" + str(highestTree) + " new:" + str(thisTree)+ " => " + str(numTree))
            matrix[posX][posY] = character + thisTree
            highestTree = thisTree
            numTree += 1
            continue

def countVisibleTrees(matrix):
    trees = 0

    size = get_matrix_size(matrix)
    print(size)
    matrix[0][0] = "X"
    matrix[0][size[1]-1] = "X"
    matrix[size[0]-1][0] = "X"
    matrix[size[0]-1][size[1]-1] = "X"

    for x in range(1,size[0]-1):
        trees += LineOfSight( matrix, (x,0), (0, 1), "D" ) 
        trees += LineOfSight( matrix, (x,size[1]-1), (0, -1), "U" ) 
    for y in range(1, size[1]-1):
        trees += LineOfSight( matrix, (0,y), (1, 0),"R" ) 
        trees += LineOfSight( matrix, (size[0]-1,y), (-1, 0),"L" ) 
    return trees + 4

def debugClearForest(matrix):
    size = get_matrix_size(matrix)
    for x in range(0,size[0]):
        for y in range(0,size[1]):
            if matrix[x][y] != "X":
                matrix[x][y] = 0

def solvePuzzle1(filename):
    matrix2 = create_matrix_from_file(filename)
    size = get_matrix_size(matrix2)
    matrix = matrix2
    #matrix = matrix_cut(matrix2, 0, 0, 50,size[1])
    print_matrix_color("Trees1",matrix, 0, bcolors.DARK_GREY, "", "")
    numTrees = countVisibleTrees(matrix)
    #debugClearForest(matrix)

    values = list()
    values.append("D")
    values.append("U")
    values.append("L")
    values.append("R")
    values.append("X")
    print_matrix_colorlist("Trees2",matrix, values, bcolors.WHITE, bcolors.DARK_GREY, "   ", "")
    return numTrees

def solvePuzzle2(filename):
    lines = loadfile(filename)  
    return 0

#unittest(solvePuzzle1, 21, "unittest.txt")
#unittest(solvePuzzle2, 1, "unittest1.txt")

unittest(solvePuzzle1, 21, "puzzleinput_work.txt")
