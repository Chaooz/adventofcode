#!/usr/local/bin/python3
# https://adventofcode.com/2023/day/2

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_vector2 import *
from advent_libs_matrix import *
from enum import Enum

setupCode("Day 7: Camel Cards")

CARD_LIST = "123456789ABCDE"
CARD_MAP = { "T":"A", "J":".", "Q":"C", "K":"D", "A":"E" }
            
class RESULT:
    NONE = 0
    ONE_PAIR = 1
    TWO_PAIRS = 3
    THREE_OF_A_KIND = 5
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 9
    FIVE_OF_A_KIND = 11

def upgradeHand(current:RESULT, new:RESULT):
    if current == RESULT.NONE:
        return new
    elif ( current == RESULT.ONE_PAIR ):
        if new == RESULT.ONE_PAIR:
            return RESULT.TWO_PAIRS
        elif new == RESULT.THREE_OF_A_KIND:
            return RESULT.FULL_HOUSE
    elif ( current == RESULT.THREE_OF_A_KIND):
        if new == RESULT.ONE_PAIR:
            return RESULT.FULL_HOUSE
    elif current != RESULT.NONE and new == RESULT.NONE:
        return current    
    elif current.value > new.value:
        return current

    return new

def getCardRule(cards:str):
    result = RESULT.NONE

    for c in CARD_LIST:
        n = cards.count(c)
        if n == 2:
            result = upgradeHand(result,RESULT.ONE_PAIR)
        elif n == 3:
            result = upgradeHand(result,RESULT.THREE_OF_A_KIND)
        elif n == 4:
            result = upgradeHand(result,RESULT.FOUR_OF_A_KIND)            
        elif n == 5:
            result = upgradeHand(result,RESULT.FIVE_OF_A_KIND)            

    return result

def insertRanked(sortedCardList:list, cards:str, card_rank:RESULT, strength:int):
    if len(sortedCardList) == 0:
        sortedCardList.append((cards,card_rank,strength))
        return sortedCardList

    for i in range(0,len(sortedCardList)):
        (c,rank,s) = sortedCardList[i]

        if card_rank > rank:
            sortedCardList.insert(i,(cards,card_rank,strength))
            return sortedCardList
        elif card_rank == rank:
            if cards > c:
                sortedCardList.insert(i,(cards,card_rank,strength))
                return sortedCardList

    sortedCardList.append((cards,card_rank,strength))
    return sortedCardList

def replaceValue(cards:str ):
    cards = cards.replace("A", "E")
    cards = cards.replace("K", "D")
    cards = cards.replace("Q", "C")
    cards = cards.replace("J", "B")
    cards = cards.replace("T", "A")
    return cards

#
# Return the score of a hand
#
def score(hand):
    counts = [hand.count(card) for card in hand]
    if 5 in counts:
        return RESULT.FIVE_OF_A_KIND
    elif 4 in counts:
        return RESULT.FOUR_OF_A_KIND
    elif 3 in counts:
        if 2 in counts:
            return RESULT.FULL_HOUSE
        return RESULT.THREE_OF_A_KIND
    elif counts.count(2) == 4:
        return RESULT.TWO_PAIRS
    elif 2 in counts:
        return RESULT.ONE_PAIR
    return RESULT.NONE

def solvePuzzle1(filename:str):
    lines = loadfile(filename)

    sortedCardList = list()

    for line in lines:
        line = line.replace("\n", "")
        (cards,strength) = line.split(" ")

        cards = replaceValue(cards)
        cardRule = getCardRule(cards)
        sortedCardList = insertRanked(sortedCardList, cards, cardRule, int(strength) )

    sum = 0
    power = len(sortedCardList)
    for card in sortedCardList:
        (cards,cardRule,strength) = card
        sum += power * strength
        power -= 1

    return sum

#
# Find the best hand out of all possible hands when replacing the Joker with a different card
#
def bestHand(hand):
    return max(map(score,replacements(hand)))

# 
def strength(hand):
    return (bestHand(hand), [CARD_MAP.get(card,card) for card in hand])

# 
# Return all possible hands when replacing the Joker with a different card
#
def replacements(hand):
    if hand == "":
        return [""]
    
    return [
        x + y
        for x in ("23456789TQKA" if hand[0] == "J" else hand[0])
        for y in replacements(hand[1:])
    ]


def solvePuzzle2(filename:str):
    lines = loadfile(filename)
    cardList = []
    for line in lines:
        hand,bid = line.split()
        s = bestHand(hand)
        cardList.append( (hand,s, int(bid)))

    # Sort cardlist with the strength of the hand (play[0] is the hand)
    cardList.sort( key=lambda play: strength(play[0]))

    # Calculate the total score
    total = 0
    for rank, (hand,s,bid) in enumerate(cardList, 1):
        total += rank * bid
    return total


unittest(getCardRule, RESULT.ONE_PAIR, "22345")
unittest(getCardRule, RESULT.TWO_PAIRS, "22433")
unittest(getCardRule, RESULT.THREE_OF_A_KIND, "22243")
unittest(getCardRule, RESULT.FULL_HOUSE, "22233")
unittest(getCardRule, RESULT.FOUR_OF_A_KIND, "22232")
unittest(getCardRule, RESULT.FIVE_OF_A_KIND, "22222")

unittest(solvePuzzle1, 6440, "unittest1.txt")
unittest(solvePuzzle2, 5905, "unittest1.txt")

runCode(7,solvePuzzle1, 250951660, "input.txt")     
runCode(7,solvePuzzle2, 251481660, "input.txt")
