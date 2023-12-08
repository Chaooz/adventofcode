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

CARD_LIST = "123456789ABCDE"
JOKER_CARD = "1"

class RESULT(Enum):
    NONE = 0
    ONE_PAIR = 1
    ONE_PAIR_JOKER = 2
    TWO_PAIRS = 3
    TWO_PAIRS_JOKER = 4
    THREE_OF_A_KIND = 5
    THREE_OF_A_KIND_JOKER = 6
    FULL_HOUSE = 7
    FULL_HOUSE_JOKER = 8
    FOUR_OF_A_KIND = 9
    FOUR_OF_A_KIND_JOKER = 10
    FIVE_OF_A_KIND = 11
    FIVE_OF_A_KIND_JOKER = 12


def upgradeHand(current:RESULT, new:RESULT, newJoker):
#    print("check upgrade:", current, " vs ", new)

    if current == RESULT.NONE:
        ret = new
        if newJoker:
            ret = RESULT(new.value + 1)
        return ret

    oldJoker = current.value % 2 == 0

    # If both are jokers, use highest
    if ( newJoker and oldJoker ):
        if current.value > new.value:
            return current
        else:
            return new

    # Mask off jokers
    if current.value % 2 == 0:
        current = RESULT( current.value - 1)

    if ( current == RESULT.ONE_PAIR ):
        if new == RESULT.ONE_PAIR:
#            print("upgradeHand:", current, " vs ", new, " =>", RESULT.TWO_PAIRS)
            return RESULT.TWO_PAIRS
        elif new == RESULT.THREE_OF_A_KIND:
#            print("upgradeHand:", current, " vs ", new, " =>", RESULT.FULL_HOUSE)
            return RESULT.FULL_HOUSE
    elif ( current == RESULT.THREE_OF_A_KIND):
        if new == RESULT.ONE_PAIR:
#            print("upgradeHand:", current, " vs ", new, " =>", RESULT.FULL_HOUSE)
            return RESULT.FULL_HOUSE
    elif current != RESULT.NONE and new == RESULT.NONE:
#        print("upgradeHand:", current, " vs ", new, " =>", current)
        return current    
    elif current.value > new.value:
#        print("upgradeHand:", current, " vs ", new, " =>", current)
        return current

 #   print("Use new : current", current, " new:", new)
        
    return new

def getCardRule(cards:str):
    return getCardRuleWithJoker(cards, "X")

def getCardRuleWithJoker(cards:str, joker:str):
    result = RESULT.NONE

    numJokers = cards.count(joker)
    hasJoker = numJokers > 0

#    print("cards:", cards, " jukers:", numJokers, " joker:", joker)

    for c in CARD_LIST:
        n = cards.count(c)

        if ( c == joker ):
            continue

        n += numJokers

        if n == 2:
            result = upgradeHand(result,RESULT.ONE_PAIR, hasJoker)
        elif n == 3:
            result = upgradeHand(result,RESULT.THREE_OF_A_KIND, hasJoker)
        elif n == 4:
            result = upgradeHand(result,RESULT.FOUR_OF_A_KIND, hasJoker)            
        elif n == 5:
            result = upgradeHand(result,RESULT.FIVE_OF_A_KIND, hasJoker)            

    # Strip joker
    if result.value > 0 and result.value % 2 == 0:
        result = RESULT(result.value - 1)

    return result

def insertRanked(sortedCardList:list, cards:str, cardRule:RESULT, strength:int, joker:str):
    if len(sortedCardList) == 0:
        sortedCardList.append((cards,cardRule,strength))
        return sortedCardList

    cards_check = cards.replace(joker, "0")

    for i in range(0,len(sortedCardList)):
        (c,r,s) = sortedCardList[i]

        if cardRule.value > r.value:
            sortedCardList.insert(i,(cards,cardRule,strength))
            return sortedCardList
        elif cardRule.value == r.value:
            d = c.replace(joker, "0")
            if cards_check > c:
                sortedCardList.insert(i,(cards,cardRule,strength))
                return sortedCardList

    sortedCardList.append((cards,cardRule,strength))
    return sortedCardList

def replaceValue(cards:str, joker:str ):
    cards = cards.replace("A", "E")
    cards = cards.replace("K", "D")
    cards = cards.replace("Q", "C")
    cards = cards.replace("J", joker)
    cards = cards.replace("T", "A")
    return cards

def solvePuzzle1(filename:str):
    lines = loadfile(filename)

    sortedCardList = list()

    for line in lines:
        line = line.replace("\n", "")
        (cards,strength) = line.split(" ")

        cards = replaceValue(cards, "B")
        cardRule = getCardRule(cards)
        sortedCardList = insertRanked(sortedCardList, cards, cardRule, int(strength), "X" )

    sum = 0
    power = len(sortedCardList)
    for card in sortedCardList:
        (cards,cardRule,strength) = card
        sum += power * strength
        power -= 1

    return sum

def solvePuzzle2(filename:str):
    lines = loadfile(filename)

    sortedCardList = list()

    for line in lines:
        line = line.replace("\n", "")
        (cards,strength) = line.split(" ")

        cards = replaceValue(cards, JOKER_CARD)
        cardRule = getCardRuleWithJoker(cards, JOKER_CARD)
        sortedCardList = insertRanked(sortedCardList, cards, cardRule, int(strength), JOKER_CARD )

    sum = 0
    power = len(sortedCardList)
    for card in sortedCardList:
        (cards,cardRule,strength) = card
        sum += power * strength
        if cardRule != RESULT.NONE:  
            if cards.count(JOKER_CARD) > 0 and cardRule == RESULT.ONE_PAIR:
                print("Card:", cards, "Rule:", cardRule, "Strength:", strength, "Power:", power, "Sum:", sum, " J:")
#            else:
#                print("Card:", cards, "Rule:", cardRule, "Strength:", strength, "Power:", power, "Sum:", sum)
        power -= 1

    return sum

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
    elif 2 in counts:
        return RESULT.ONE_PAIR
    return RESULT.NONE




unittest(getCardRule, RESULT.ONE_PAIR, "22345")
unittest(getCardRule, RESULT.TWO_PAIRS, "22433")
unittest(getCardRule, RESULT.THREE_OF_A_KIND, "22243")
unittest(getCardRule, RESULT.FULL_HOUSE, "22233")
unittest(getCardRule, RESULT.FOUR_OF_A_KIND, "22232")
unittest(getCardRule, RESULT.FIVE_OF_A_KIND, "22222")

unittest(solvePuzzle1, 6440, "unittest1.txt")
unittest(solvePuzzle1, 250951660, "input.txt")     

unittest_input(getCardRuleWithJoker, JOKER_CARD, RESULT.THREE_OF_A_KIND, "22"+JOKER_CARD+"45")

unittest(solvePuzzle2, 5905, "unittest1.txt")
unittest(solvePuzzle2, 251432266, "input.txt")

# LOW : 251361338
# NO  : 251388895
#       251432266
#       251361338
#       251516664
#       251282208
# HIGH: 251795473
  

