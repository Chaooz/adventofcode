#!/usr/local/bin/python3
# https://adventofcode.com/2023/day/2

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_vector2 import *
from advent_libs_matrix import *
from enum import Enum

sys.setrecursionlimit(1500)

print("")
print_color("Day 7: Camel Cards", bcolors.OKGREEN)
print("")

CARD_MAP = { "T":"A", "J":".", "Q":"C", "K":"D", "A":"E" }
            
JOKER_CARD = "1"

class RESULT(Enum):
    NONE = 0
    ONE_PAIR = 1
    TWO_PAIRS = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6

def score(hand):
    counts = [hand.count(card) for card in hand]
    # FIVE_OF_A_KIND
    if 5 in counts:
        return 6            
    # FOUR_OF_A_KIND
    elif 4 in counts:       
        return 5
    # THREE_OF_A_KIND
    elif 3 in counts:
        # ONE_PAIR
        if 2 in counts:
            # FULL_HOUSE
            return 4
        return 3
    # TWO_PAIRS
    elif counts.count(2) == 4:
        return 2
    # ONE_PAIR
    elif 2 in counts:
        return 1
    return 0

# Classify
def bestHand(hand):
    return max(map(score,replacements(hand)))

def strength(hand):
    return (bestHand(hand), [CARD_MAP.get(card,card) for card in hand])

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

    cardList.sort( key=lambda play: strength(play[0]))

#    print(cardList)

    total = 0
    for rank, (hand,s,bid) in enumerate(cardList, 1):
        total += rank * bid
    return total

unittest(solvePuzzle2, 5905, "unittest1.txt")
unittest(solvePuzzle2, 251481660, "input.txt")
