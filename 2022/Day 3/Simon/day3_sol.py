#!/usr/local/bin/python3

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *

def devideCompartments(contentList):
    rucksackList = []
    for rucksack in contentList:
        rucksack = rucksack.strip()
        compartment1 = rucksack[:int(len(rucksack)/2)]
        compartment2 = rucksack[int(len(rucksack)/2):]
        rucksackList.append( (compartment1,compartment2) )
    return rucksackList

def findDuplicateItems(rucksackList):
    duplicates = []
    for rucksack in rucksackList:
        duplicates.append(findFirstDupe(rucksack))            
    return duplicates

def findFirstDupe(rucksack):
    for item in rucksack[0]:
            for otherItem in rucksack[1]:
                if item == otherItem:
                    return otherItem

def getPriorities(dupeList):
    priorityScore = 0
    for character in dupeList:
        if character.upper() == character:
            priorityScore += ord(character) - ord("A") + 27
        else:
            priorityScore += ord(character) - ord("a") + 1 
    return priorityScore

def getGroups(contentList):
    groups = []
    counter = 0
    currentGroup = []
    for rucksack in contentList:
        rucksack = rucksack.strip()
        if counter == 3:
            groups.append(currentGroup)
            counter = 0
            currentGroup = []
        currentGroup.append(rucksack)
        counter += 1
    
    groups.append(currentGroup)

    return groups

def findGroupDupes(groupList):
    duplicates = []
    for group in groupList:
        duplicates.append(findFirstGroupDupe(group))
    return duplicates

def findFirstGroupDupe(group):
    for item in group[0]:
        if group[1].find(item) != -1 and group[2].find(item) != -1:
            return item

contentList = loadfile("input.txt")
print("Part 1:")
rucksackList = devideCompartments(contentList)
print(getPriorities(findDuplicateItems(rucksackList)))
print("----------")

print("Part 2:")
groups = getGroups(contentList)
duplicates = findGroupDupes(groups)
#print(duplicates)
print(getPriorities(duplicates))
