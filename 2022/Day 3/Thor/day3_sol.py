#
# 2022 Day 3: Rucksack Reorganization
#

#!/usr/lib/python3

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *

#
# Split a packet in half and check each half for equal characters
#
def getSimilarPacket(packet):
    mid = int(len(packet) / 2)
    item1 = packet[0:mid]
    item2 = packet[mid:len(packet)]
    for letter in item2:
        a = item1.find(letter)
        if a >= 0:
            return letter

    return ""

#
# Return the score for all a-z and A-Z characters
#
def getCharacterScore(character):
    if character.upper() == character:
        return ord(character) - ord("A") + 27
    else:
        return ord(character) - ord("a") + 1

#
# Group all packets in group of 3
#
def groupPackets(packetList):
    index = 0
    groups = []
    for packet in packetList:
        packet = packet.strip()

        if index == 0:
            group = []
        group.append(packet)
        index = index + 1
        if index == 3:
            groups.append(group)
            index = 0
    return groups

#
# Find the same character in all 3 groups
#
def getGroupCharacter(group):
    for character in group[0]:
        a = group[1].find(character)
        b = group[2].find(character)
        if a > -1 and b > -1:
            return character

def solvePuzzle1(filename):
    lines = loadfile(filename)
    score = 0
    for line in lines:
        line = line.strip()
        letter = getSimilarPacket(line)
        score += getCharacterScore(letter)
    return score

def solvePuzzle2(filename):
    lines = loadfile(filename)
    groups = groupPackets(lines)
    score = 0
    for group in groups:   
        character = getGroupCharacter(group)
        score += getCharacterScore(character)
    return score
    
print("")
print_color("Day 3: Rucksack Reorganization", bcolors.OKGREEN)
print("")

unittest(getSimilarPacket, "p", "vJrwpWtwJgWrhcsFMMfFFhFp")
unittest(getSimilarPacket, "L","jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL")
unittest(getSimilarPacket, "P", "PmmdzqPrVvPwwTWBwg")
unittest(getSimilarPacket, "v", "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn")
unittest(getSimilarPacket, "t", "ttgJtRGJQctTZtZT")
unittest(getSimilarPacket, "s", "CrZsJsPPZsGzwwsLwLmpwMDw")

unittest(getCharacterScore,16,"p")
unittest(getCharacterScore,38,"L")
unittest(getCharacterScore,42,"P")
unittest(getCharacterScore,22,"v")
unittest(getCharacterScore,20,"t")
unittest(getCharacterScore,19,"s")

unittest(solvePuzzle1, 157, "unittest1.txt")
unittest(solvePuzzle2, 70, "unittest2.txt")

unittest(solvePuzzle1, 7428, "puzzleinput.txt")
unittest(solvePuzzle2, 2650, "puzzleinput.txt")
unittest(solvePuzzle1, 8240, "puzzleinput_work.txt")
unittest(solvePuzzle2, 2587, "puzzleinput_work.txt")
