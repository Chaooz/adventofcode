#!/usr/local/bin/python3
#
# 2022 Day 7: No Space Left On Device
#

# Rules
# Must delete files
# 70000000 is max space
# Need at least 70000000

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *


print("")
print_color("Day 7: No Space Left On Device", bcolors.OKGREEN)
print("")

class FileFolder:
    name = ""
    size = 0
    isFolder = False
    children = []

    def __init__(self, name, size, isFolder):
        self.children = list()
        self.name = name
        self.size = size
        self.isFolder = isFolder

    def AddFile(self,filename, size):
        self.children.append( FileFolder(filename, int(size), False))
        self.size += int(size)

    def AddFolder(self,folderName):
        self.children.append( FileFolder(folderName, 0, True))

    def GetFolder(self,folderName):
        for child in self.children:
            if child.isFolder and child.name == folderName:
                return child
        print_warning("did not find foldername : " + folderName + " : " + str(len(self.subfolder)))
        return None

#
# parseInputCommands
#
# @String input       - The data to parse
# @String folderName  - Name of the folder to parse
# @Int    parentIndex - The index in the inputstring 
#
def parseInputCommands(input, folder, parentIndex):

    skipto = 0
    for index in range(parentIndex,len(input)):
        line = input[index]
        line = line.strip()
        parts = line.split(" ")

        if skipto > 0 and index < skipto:
            continue

        if line[0] == "$":
            # CD commands
            if parts[1] == "cd":
                if parts[2] == "/":
                    pass
                elif parts[2] == "..":
                    return index + 1
                else:
                    subFolder = folder.GetFolder(parts[2])
                    skipto = parseInputCommands(input, subFolder, index + 1)
                    folder.size += subFolder.size
        # Folders
        elif parts[0] == "dir":
            folder.AddFolder(parts[1])
        # Files
        else:
            folder.AddFile(parts[1], parts[0] )

    return len(input)

#
# Go through all folders with max size
#
def getFoldersWithMax(folder, maxSum ):
    folders = list()
    for child in folder.children:
        if child.isFolder:
            if child.size < maxSum:
                folders.append(child)
            subFolders = getFoldersWithMax(child, maxSum)
            for sub in subFolders:
                folders.append(sub)
    return folders

# 
# Go through all folders with at least minSum size
#
def getFoldersWithMin(folder, minSum ):
    folders = list()
    for child in folder.children:
        if child.isFolder:
            if child.size >= minSum:
                folders.append(child)
            subFolders = getFoldersWithMin(child, minSum)
            for sub in subFolders:
                folders.append(sub)
    return folders

#
# Print all folders and files
#
def debugPrintTree(folder, space):
    print(space + "- " + folder.name + " (dir)")
    for child in folder.children:
        if child.isFolder:
            debugPrintTree(child, space + " ")
        else:
            print(space + " " + "- " + child.name + " (file, size=" + str(child.size) +")")

def solvePuzzle1(filename):
    lines = loadfile(filename)  

    topFolder = FileFolder("/", 0, True )
    parseInputCommands(lines, topFolder, 0 )
    #debugPrintTree(topFolder, "")
    sum = 0
    folders = getFoldersWithMax(topFolder, 100000 )
    for folder in folders:
        sum += folder.size
    return sum

def solvePuzzle2(filename):
    lines = loadfile(filename)  
    topFolder = FileFolder("/", 0, True )
    parseInputCommands(lines, topFolder, 0 )
    #debugPrintTree(topFolder, "")

    deviceSpace = 70000000
    neededSpace = 30000000
    freeSpace = deviceSpace - topFolder.size
    mustFree = neededSpace - freeSpace

    min = 70000000
    folders = getFoldersWithMin(topFolder, mustFree )
    for folder in folders:
        if folder.size < min:
            min = folder.size
    return min

unittest(solvePuzzle1, 95437 , "testinput.txt")
unittest(solvePuzzle2, 24933642 , "testinput.txt")

unittest(solvePuzzle1, 1141028 , "input.txt")
unittest(solvePuzzle2, 8278005 , "input.txt")

