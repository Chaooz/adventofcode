#!/usr/local/bin/python3

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
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

def getPointsForStrategy(gameList):
    points = 0
    for game in gameList:
        them = game[0]
        result = game[1]
        match them:
            case "A":
                if result == "X":
                    points += 3
                elif result == "Y":
                    points += 4
                elif result == "Z":
                    points += 8
            case "B":
                if result == "X":
                    points += 1
                elif result == "Y":
                    points += 5
                elif result == "Z":
                    points += 9
            case "C":
                if result == "X":
                    points += 2
                elif result == "Y":
                    points += 6
                elif result == "Z":
                    points += 7
    return points

def getTotalScore(inputFile):
    gameList = listFromFile(inputFile, " ")
    
    totalScore1 = 0
    totalScore1 += getPointsForSelection(gameList)
    totalScore1 += getPointsForResult(gameList)
    print("The total number of points gained for part 1 is " + str(totalScore1))
    print("------------------")

    totalScore2 = 0
    totalScore2 = getPointsForStrategy(gameList)
    print("The total number of points gained for part 2 is " + str(totalScore2))


getTotalScore("input.txt")