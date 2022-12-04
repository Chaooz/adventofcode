#!/usr/lib/python3

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *

def parseCalorieList(calorieList):
    counter = 0
    ranking = []
    for meal in calorieList:
        if meal == "\n":
            ranking.append(counter)
            counter = 0
        else:
            counter = int(counter) + int(meal.strip())
    return ranking

def printResult(input):
    calorieList = loadfile(input)
    ranking = parseCalorieList(calorieList)
    ranking.sort(reverse = True)
    result = ranking[0] + ranking[1] + ranking[2]
    print("The elfs with the 3 highest loads are carrying " + str(result) + " calories in total")
    return 0

printResult("input.txt")