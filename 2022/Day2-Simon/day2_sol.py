#!/usr/local/bin/python3

import sys

# Import custom libraries
sys.path.insert(1, '../../Libs')
from advent_libs import *

# This function takes a list of tuples, each containing two strings as it´s 
# #input. It will enumerate the list adding 1, 2, or 3 points based on the 
# second string value of the tuple. It returns the total number of points 
# from the list as an integer.
def getPointsForSelection(selections):
    points = 0
    for selection in selections:
        selection = selection[1]
        if selection == "X":
            points += 1
        elif selection == "Y":
            points += 2
        elif selection == "Z":
            points += 3
        else:
            ValueError("The selection contained an unexpected value")
    return points

def getPointsForResult(gameList):
    points = 0
    for game in gameList:
        them = game[0]
        you = game[1]

        match them:
            case "A":
                if you == "X":
                    points += 3
                elif you == "Y":
                    points += 6
            case "B":
                if you == "Y":
                    points += 3
                elif you == "Z":
                    points += 6
            case "C":
                if you == "X":
                    points += 6
                elif you == "Z":
                    points += 3
    return points

def getTotalScore(inputFile):
    totalPoints = 0
    gameList = listFromFile(inputFile, " ")
    totalPoints += getPointsForSelection(gameList)
    totalPoints += getPointsForResult(gameList)
    print("The total number of points gained is " + str(totalPoints))

getTotalScore("input.txt")