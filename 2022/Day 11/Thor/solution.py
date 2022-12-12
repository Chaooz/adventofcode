#!/usr/local/bin/python3

import sys
import yaml
from benedict import benedict

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_matrix import *
from advent_libs_list import *
from advent_libs_vector2 import *

monkeyList = []
class Monkey:
    number:int
    items:list
    operation:str
    test:str
    monkeyTrue:int
    monkeyFalse:int
    iteration:int

    def __init__(self, number):
        self.number = int(number)
        self.iteration = 0

    def ToString(self):
        return "Monkey " + str(self.number) + " inspected items " + str(self.iteration) + " times."

    def Operation(self, old):
        return eval(self.operation)

    def Test(self, item):
        return item % int(self.test) == 0

    def ExamineItems(self, supermod):
        tempList = self.items.copy()
        for oldItem in tempList:
            self.iteration += 1
            newItem = self.Operation(oldItem)
            if supermod == 0:
                newItem = int(newItem / 3)
            else:
                newItem = newItem % supermod
            self.items.remove(oldItem)
            if self.Test(newItem):
                monkeyList[self.monkeyTrue].items.append(newItem)
            else:
                monkeyList[self.monkeyFalse].items.append(newItem)
       
def solvePuzzle(filename, iterations, puzzleNumber):
    data = benedict.from_yaml(filename)
    for key in data:
        monkey = Monkey(key.split()[1])
        monkey.items = str(data[key]["Starting items"]).split(",")
        monkey.items = [int(item) for item in monkey.items]
        monkey.operation = data[key]["Operation"].split(" = ")[1]
        monkey.test = int(data[key]["Test"].split(" ")[2])
        monkey.monkeyTrue = int(data[key]["If true"].split(" ")[3])
        monkey.monkeyFalse = int(data[key]["If false"].split(" ")[3])

        monkeyList.append(monkey)

    supermod = 1
    if puzzleNumber == 2:
        for monkey in monkeyList:
            supermod *= monkey.test

    for i in range(0,iterations):
        for monkey in monkeyList:
            monkey.ExamineItems(supermod)

    for monkey in monkeyList:
        print(monkey.ToString())

    active = list()
    for monkey in monkeyList:
        active.append( monkey.iteration )
    active.sort(reverse=True)
    return active[0] * active[1]

def solvePuzzle1(filename):
    return solvePuzzle(filename, 20, 1)

def solvePuzzle2(filename):
    return solvePuzzle(filename, 10000, 2)

print("")
print_color("Day 11: Monkey in the Middle", bcolors.OKGREEN)
print("")

unittest(solvePuzzle1, 10605, "unittest.yaml")
unittest(solvePuzzle1, 66124, "puzzleinput.yaml")
unittest(solvePuzzle2, 2713310158, "unittest.yaml")
unittest(solvePuzzle2, 19309892877, "puzzleinput.yaml")
