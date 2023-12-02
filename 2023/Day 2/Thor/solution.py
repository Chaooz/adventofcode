#!/usr/local/bin/python3
# https://adventofcode.com/2023/day/2

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_vector2 import *
from advent_libs_matrix import *

print("")
print_color("Day 2: Cube Conundrum", bcolors.OKGREEN)
print("")

class Game:
    id:int
    rounds:list

    def __init__(self,name = "") -> None:
        self.id = 0
        self.rounds = list()

    def isGameValid(self,red:int,green:int,blue:int):
        for round in self.rounds:
            if red < round.red:
                return False
            if blue < round.blue:
                return False
            if green < round.green:
                return False
        return True
    
    def getMaxRound(self):
        maxRound = Round()
        for round in self.rounds:
            if maxRound.red < round.red:
                maxRound.red = round.red
            if maxRound.blue < round.blue:
                maxRound.blue = round.blue
            if maxRound.green < round.green:
                maxRound.green = round.green
        return maxRound

    def ToString(self):
        a = "" + str(self.id) + " => "
        for round in self.rounds:
            a += round.ToString() + " "
        return a
    
class Round:
    red:int
    green:int
    blue:int

    def __init__(self) -> None:
        self.red = 0
        self.green = 0  
        self.blue = 0

    def GetPower(self):
        return self.red * self.green * self.blue

    def ToString(self):
        return " r:" + str(self.red) + " b:" + str(self.green) + " g:" + str(self.blue)

def createGame(line:list):
    game = Game()

    # Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    gameIdStr = line.split(":")
    game.id = int(gameIdStr[0].split(" ")[1])

    sets = gameIdStr[1].split(";")

    for set in sets:
        round = Round()
        colors = set.split(",")
        for color in colors:
            if color.find("blue") > -1:
                round.blue = int(color.split(" ")[1])
            if color.find("red") > -1:
                round.red = int(color.split(" ")[1])
            if color.find("green") > -1:
                round.green = int(color.split(" ")[1])
        game.rounds.append(round)
    return game


def solvePuzzle1(filename:str):
    lines = loadfile(filename)

    sum = 0
    for line in lines:
        if len(line) > 0:
            game = createGame(line)
            if ( game.isGameValid(12,13,14) ):
                sum += game.id

    return sum

def solvePuzzle2(filename:str):
    lines = loadfile(filename)
    sum = 0
    for line in lines:
        if len(line) > 0:
            game = createGame(line)
            round = game.getMaxRound()
            sum += round.GetPower()

    return sum

unittest(solvePuzzle1, 8, "unittest1.txt")
unittest(solvePuzzle1, 2545, "input.txt")

unittest(solvePuzzle2, 2286, "unittest1.txt")
unittest(solvePuzzle2, 78111, "input.txt")
