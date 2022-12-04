#!/usr/lib/python3

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *

def parseCalorieList(calorieList):
    highestNumberOfCalories = 0
    counter = 0
    for meal in calorieList:
        if meal == "\n":
            counter = 0
        else:
            counter = int(counter) + int(meal.strip())
            if counter > highestNumberOfCalories:
                highestNumberOfCalories = counter
    return highestNumberOfCalories            

def printResult(input):
    calorieList = loadfile(input)
    result = parseCalorieList(calorieList)
    print("The elf with the highest load is carrying " + str(result) + " calories")
    return 0

printResult("input.txt")