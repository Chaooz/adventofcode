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

#
# LineOfSight
# Returns the number of trees in a line of sight
# @Matrix matrix    - 2D array filled with trees
# @Tuple  position  - start position
# @Tuple  direction - The direction to search for LOS
# @String character - The character to place next to the high trees
#
def LineOfSight(matrix, position, direction, character ):

    showDebug = True

    posX = position[0]
    posY = position[1]

    size = get_matrix_size(matrix)
    highestTree = matrix[posX][posY]

    if highestTree[0] == "U" or highestTree[0] == "D" or highestTree[0] == "L" or highestTree[0] == "R":
        return 0

    numTree = 1
    matrix[posX][posY] = character + highestTree

    while(True):
        posX += direction[0]
        posY += direction[1]

        # Outside of Matrix ?
        if posX < 0 or posX > size[0]-1 or posY < 0 or posY > size[1]-1:
#            if numTree > 0:
#                print("[OK] Outside matrix : " + str(posX) + "x" + str(posY) + " high:" + str(highestTree) + "  num:" + str(numTree) + " char:" + character)
            return numTree

        thisTree = matrix[posX][posY]

        # Visible from the other side
        if thisTree[0] == "U" or thisTree[0] == "D" or thisTree[0] == "L" or thisTree[0] == "R":
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

#
# GetMaxLineOfSight
# Return the distance you can see before hitting trees
# @Matrix matrix    - 2D array filled with trees
# @Tuple  position  - start position
# @Tuple  direction - The direction to search for LOS
# @String character - The character to place next to the high trees
#
def GetMaxLineOfSight(matrix, position, direction, character ):

    posX = position[0]
    posY = position[1]

    size = get_matrix_size(matrix)
    highestTree = matrix[posX][posY]
    numTree = 0

    while(True):
        posX += direction[0]
        posY += direction[1]

        # Outside of Matrix ?
        if posX < 0 or posX > size[0]-1 or posY < 0 or posY > size[1]-1:
            return numTree

        thisTree = matrix[posX][posY]
        numTree += 1

        if highestTree <= thisTree:
            return numTree

        if len(character) > 0:
            matrix[posX][posY] = character + matrix[posX][posY]

def findBestTreeHousePlace(matrix):
    size = get_matrix_size(matrix)

    maxScore = 0
    position = (0,0)
    for x in range(0,size[0]):
        for y in range(0,size[1]):
            up = GetMaxLineOfSight(matrix, (x,y), (0, -1),"")
            down = GetMaxLineOfSight(matrix, (x,y), (0, 1),"")
            left = GetMaxLineOfSight(matrix, (x,y), (-1, 0),"")
            right = GetMaxLineOfSight(matrix, (x,y), (1, 0),"")

            score = up * down * left * right
            if score > maxScore:
                maxScore = score
                position = (x,y)

    return position, maxScore

def countVisibleTrees(matrix):
    trees = 0

    size = get_matrix_size(matrix)
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

def solvePuzzle1(filename, showDebug):
    matrix = create_matrix_from_file(filename)
    numTrees = countVisibleTrees(matrix)

    if showDebug:
        highlight_values = ["D", "U", "L", "R", "X"]
        print_matrix_colorlist("solvePuzzle1",matrix, highlight_values, bcolors.WHITE, bcolors.DARK_GREY, "   ", "")

    return numTrees

def debugMarkPath(matrix, pos, character):
    GetMaxLineOfSight(matrix, pos, (0, -1), character)
    GetMaxLineOfSight(matrix, pos, (0, 1), character)
    GetMaxLineOfSight(matrix, pos, (-1, 0), character)
    GetMaxLineOfSight(matrix, pos, (1, 0), character)

def solvePuzzle2(filename, showDebug):
    matrix = create_matrix_from_file(filename)
    pos, maxScore = findBestTreeHousePlace(matrix)

    # Create a path in the matrix to visually see i
    if showDebug:
        debugMarkPath(matrix, pos, "*")
        matrix[pos[0]][pos[1]] = "X" + matrix[pos[0]][pos[1]]
        highlight_values = ["X", "*"]
        print_matrix_colorlist("solvePuzzle2",matrix, highlight_values, bcolors.YELLOW, bcolors.DARK_GREY, " 00", "")

    return maxScore

################################################################

showDebug = False

print("")
print_color("Day 8: Treetop Tree House", bcolors.OKGREEN)
print("")

unittest_input(solvePuzzle1, showDebug,21, "unittest.txt")
unittest_input(solvePuzzle2, showDebug, 8, "unittest.txt")
unittest_input(solvePuzzle1, showDebug, 1546, "puzzleinput_work.txt")
unittest_input(solvePuzzle2, showDebug, 519064, "puzzleinput_work.txt")
unittest_input(solvePuzzle1, showDebug, 1546, "puzzleinput.txt")
unittest_input(solvePuzzle2, showDebug, 519064, "puzzleinput.txt")
