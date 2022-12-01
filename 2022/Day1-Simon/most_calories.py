#!/usr/lib/python3

import sys

# Import custom libraries
sys.path.insert(1, '../../Libs')
from advent_libs import *

# Global variables


def parseCalorieList(calorieList):
    highestNumberOfCalories = 0
    counter = 0
    print(calorieList)
    for meal in calorieList:
        if meal == "\n":
            counter = 0
        else:
            mealNum = int(meal.strip())
            counter = int(counter) + int(mealNum)
            print("Counter: " + str(counter))
            if counter > highestNumberOfCalories:
                highestNumberOfCalories = counter
                print("Highest: " + str(highestNumberOfCalories))
    return highestNumberOfCalories            

def printResult(input):
    calorieList = loadfile(input)
    result = parseCalorieList(calorieList)
    print("The elf with the highest load is carrying " + str(result) + " calories")
    return 0

printResult("input.txt")