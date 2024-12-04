#!/usr/local/bin/python3
# https://adventofcode.com/2023/day/2

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_vector2 import *
from advent_libs_matrix import *

sys.setrecursionlimit(1500)

setupCode("Day 4: Scratchcards")

class Card:
    id:int
    winningNumbers : list
    yourNumbers: list
    numCards : int

    def __init__(self, id:str, winningNumbers:list, yourNumbers:list) -> None:
        self.id = id
        self.winningNumbers = winningNumbers
        self.yourNumbers = yourNumbers
        self.numCards = 1
    
    def checkScore(self):
        score = 0
        for wNumber in self.winningNumbers:
            if wNumber == "":
                continue

            for yNumber in self.yourNumbers:
                if wNumber == yNumber:
                    if score == 0:
                        score = 1
                    else:
                        score += score

        return score

    def NumWins(self):
        score = 0
        for wNumber in self.winningNumbers:
            if wNumber == "":
                continue
            for yNumber in self.yourNumbers:
                if wNumber == yNumber:
                    score += 1
        return score
        
        
class CardList:
    cardList : list
    def __init__(self) -> None:
        self.cardList = list()

    def Add(self,card:Card):
        self.cardList.append(card)

    def Get(self,id:int) -> Card:
        for card in self.cardList:
            if card.id == id:
                return card
        return None
    
    def GetList(self):
        return self.cardList


def checkCardScore(input:str):
    card = createCard(input)
    return card.checkScore()

def createCard(input:str):

    input = input.strip("\n")

    a = input.split(":")
    ids = a[0].split(" ")
    id = ids[len(ids)-1]

    numberGroup = a[1].split("|")
    winningNumbers = numberGroup[0].split(" ")
    yourMumbers = numberGroup[1].split(" ")

#    print("Card [" + str(id) + "] " + str(winningNumbers) + " => " + str(yourMumbers))

    return Card(int(id),winningNumbers, yourMumbers)

def solvePuzzle1(filename:str):
    lines = loadfile(filename)

    sum = 0
    for line in lines:
        card = createCard(line)
        sum += card.checkScore()
    return sum

def solvePuzzle2(filename:str):
    lines = loadfile(filename)
    sum = 0

    cardList = CardList()
    for line in lines:
        card = createCard(line)
        cardList.Add(card)

    for card in cardList.GetList():
        numWins = card.NumWins()
        sum += card.numCards

        for i in range(card.id + 1, card.id + numWins + 1):
            wCard = cardList.Get(i)
            wCard.numCards += card.numCards

    return sum

unittest(checkCardScore, 8, "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53")
unittest(checkCardScore, 2, "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19")
unittest(checkCardScore, 2, "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1")
unittest(checkCardScore, 1, "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83")
unittest(checkCardScore, 0, "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36")
unittest(checkCardScore, 0, "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11")

unittest(solvePuzzle1, 13, "unittest1.txt")
unittest(solvePuzzle2, 30, "unittest1.txt")

runCode(4,solvePuzzle1, 23028, "input.txt")     
runCode(4,solvePuzzle2, 9236992, "input.txt")
