#!/usr/local/bin/python3
# https://adventofcode.com/2023/day/2

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_vector2 import *
from advent_libs_matrix import *

setupCode("Day 3: Gear Ratios")

class Gear:
    x:int
    y:int
    val:str
    numberList : list

    def __init__(self,x:int,y:int,val:str) -> None:
        self.x = x
        self.y = y
        self.numberList = list()
        self.val = val

    def AddNumber(self,number:int):
        self.numberList.append(number)

    def GetPower(self) -> int:
        sum = 1
        if len(self.numberList) == 2:
            a = ""
            for number in self.numberList:
                a += str(number) + " "
                sum *= number

            #print("Gear at ", self.x, self.y, " has power ", sum, " with numbers ", a)
        else:
            return 0
        return sum

class GearList:
    gearList : list
    def __init__(self) -> None:
        self.gearList = list()

    def Add(self,gear:Gear):
        self.gearList.append(gear)

    def Get(self,x:int,y:int) -> Gear:
        for gear in self.gearList:
            if gear.x == x and gear.y == y:
                return gear
        return None
    
    def GetList(self):
        return self.gearList
        

#
# If the number has a symbol adjacent to it, then it is valid
#
def adjacentSymbol(matrix:Matrix, number:str, xx:int, yy:int) -> Gear:
    for y in range(yy-1,yy+2):
        if y < 0 or y >= matrix.sizeY:
            continue
        for x in range(xx-len(number)-1, xx+1):
            if x < 0 or x >= matrix.sizeY:
                continue
            val = matrix.Get(x,y)
            if val.isnumeric() or val == ".":
                continue
            return Gear(x,y,val) 
    return None
    
def solvePuzzle1(filename:str):
    matrix  = Matrix.CreateFromFile(filename, ".")

    sum = 0
    for y in range(0,matrix.sizeY):
        number = ""
        for x in range(0,matrix.sizeX):
            val = matrix.Get(x,y)
            calcNumber = False

            if val.isnumeric():
                number += val
                if x == matrix.sizeX - 1:
                    calcNumber = True
            elif len(number) > 0:
                calcNumber = True

            if calcNumber:
                if adjacentSymbol(matrix, number, x, y) != None:                    
                    sum += int(number)
                number = ""
    return sum

def solvePuzzle2(filename:str):
    matrix  = Matrix.CreateFromFile(filename, ".")
    gearList = GearList()

    sum = 0
    for y in range(0,matrix.sizeY):
        number = ""
        for x in range(0,matrix.sizeX):
            val = matrix.Get(x,y)
            calcNumber = False

            if val.isnumeric():
                number += val
                if x == matrix.sizeX - 1:
                    calcNumber = True
            elif len(number) > 0:
                calcNumber = True

            if calcNumber:
                gear = adjacentSymbol(matrix, number, x, y)                   
                if gear == None:
                    number = ""
                    continue

                if gear.val == "*":
                    otherGear = gearList.Get(gear.x,gear.y)
                    if ( otherGear != None ):
                        otherGear.AddNumber(int(number))
                    else:
                        gearList.Add(gear)
                        gear.AddNumber(int(number))

                number = ""

    for gear in gearList.GetList():
        sum += gear.GetPower()

    return sum


unittest(solvePuzzle1, 4361, "unittest1.txt")
unittest(solvePuzzle2, 467835, "unittest2.txt")  

runCode(3,solvePuzzle1, 528799, "input.txt")     
runCode(3,solvePuzzle2, 84907174, "input.txt")
