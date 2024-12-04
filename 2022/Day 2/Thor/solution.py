#!/usr/lib/python3
# https://adventofcode.com/2022/day/2

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *

setupCode("Day 2: Rock Paper Scissors")

_Rock = "A"
_Paper = "B"
_Scissor = "C"

_MustLoose = "X"
_MustDraw = "Y"
_MustWin = "Z"

#
# Translate the choice from XYZ to ABC
#
def translateOpponent(opponent):
    if opponent == "X":
        return _Rock
    elif opponent == "Y":
        return _Paper
    elif opponent == "Z":
        return _Scissor
    else:
        return ""

#
# Returns the score of the players choice of weapon
# 
def calculateChoiceScore(you):
    you_translated = translateOpponent(you)
    return calculateChoiceScoreTranslated(you_translated)

#
# Returns the score of the players choice of weapon
# Here your choice is translated ( from XYZ to ABC )
# 
def calculateChoiceScoreTranslated(you_translated):
    if you_translated == _Rock:
        return 1
    elif you_translated == _Paper:
        return 2
    elif you_translated == _Scissor:
        return 3
    else:
        return 0


#
# Calculate the score of Rock/Paper/Scissor
#
def calculateMatchPoints(opponent, you):
    you_translated = translateOpponent(you)
    return calculateMatchPointsTranslated(opponent, you_translated)

#
# Calculate the score of Rock/Paper/Scissor
# Here your choice is translated ( from XYZ to ABC )
#
def calculateMatchPointsTranslated(opponent, you_translated):

    # Draw
    if you_translated == opponent:
        return 3

    # Calculate wins
    if you_translated == _Rock and opponent == _Scissor:
        return 6
    elif you_translated == _Paper and opponent == _Rock:
        return 6
    elif you_translated == _Scissor and opponent == _Paper:
        return 6

    # Lost
    return 0

#
# Return the score of the choice + win/loose/draw score 
#
def calculateFullScore(opponent, you):
    win = calculateMatchPoints(opponent,you)
    choice = calculateChoiceScore(you)
    return win + choice

#
# Return points based on the win/loose/draw result
#
def getRuleScore(rule):
    if rule == _MustLoose:
        return 0
    elif rule == _MustWin:
        return 6
    else:
        return 3

#
# Figure out the points for each match (choice + draw/win/loose)
# Sum all matches and return
#
def useStrategyGuide(guide):
    score = 0
    for line in guide:
        line = line.replace("\n", "")
        players = line.split(" ")
        score += calculateFullScore(players[0], players[1])
    return score

#
# Return the choice the player has to make to win/loose/draw based on the opponents choice
#
def getMatchChoice(opponent, rule):

    if rule == _MustWin:
        if opponent == _Rock:
            return _Paper
        elif opponent == _Paper:
            return _Scissor
        elif opponent == _Scissor:
            return _Rock
    elif rule == _MustLoose:
        if opponent == _Rock:
            return _Scissor
        elif opponent == _Paper:
            return _Rock
        elif opponent == _Scissor:
            return _Paper

    # Draw, just return opponent
    return opponent

#
# Debug function to return a proper name for the choice 
#
def debugGetProperChoiceName(choice):
    if choice == _Rock:
        return "Rock"
    elif choice == _Paper:
        return "Paper"
    elif choice == _Scissor:
        return "Scissor"
    return "?"

#
# Debug function to return a proper name for the forced choice we have to make
#
def debugGetChoiceName(choice):
    if choice ==_MustWin:
        return "MustWin"
    elif choice == _MustDraw:
        return "MustDraw"
    elif choice == _MustLoose:
        return "MustLoose"
    return "?"

#
# Anyway, the second column says how the round needs to end: X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win
# The total score is still calculated in the same way, but now you need to figure out what shape to choose so the round ends as indicated
#
def useRulesFromGuide(guide):
    score = 0
    for line in guide:
        line = line.replace("\n", "")
        players = line.split(" ")

        # Return the choice based on opponents choice and if we have to win/loose/draw
        choice = getMatchChoice(players[0], players[1])
        choice_score = calculateChoiceScoreTranslated(choice)
        match_score = calculateMatchPointsTranslated(players[0], choice)

        # Debug ouput
        #weaponA = debugGetProperChoiceName(players[0])
        #weaponB = debugGetProperChoiceName(choice)
        #choiceName = debugGetChoiceName(players[1])
        #print_ok("useRulesFromGuide:" + weaponA + " vs " + weaponB + " (" + choiceName + ") : " + str(choice_score) + " + " + str(match_score) + " = " + str(match_score+choice_score) )

        score += match_score + choice_score
    return score

def solvePuzzle1(filename):
    lines = loadfile(filename)
    return useStrategyGuide(lines)

def solvePuzzle2(filename):
    lines = loadfile(filename)
    return useRulesFromGuide(lines)

unittest(calculateChoiceScore, 1, "X")
unittest(calculateChoiceScore, 2, "Y")
unittest(calculateChoiceScore, 3, "Z")
unittest(calculateChoiceScore, 0, "D")

unittest_input(calculateMatchPoints, "Y", 6, "A" )
unittest_input(calculateMatchPoints, "X", 0, "B" )
unittest_input(calculateMatchPoints, "Z", 3, "C" )
unittest_input(calculateFullScore, "Y", 8, "A" )

unittest( useStrategyGuide, 15, ["A Y","B X", "C Z"])
unittest( useRulesFromGuide, 12, ["A Y","B X", "C Z"])

runCode( 2, solvePuzzle1, 11906, "puzzleinput.txt")
runCode( 2, solvePuzzle2, 11186, "puzzleinput.txt")
