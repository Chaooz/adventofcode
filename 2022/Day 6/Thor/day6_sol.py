#
# 2022 Day 6: Tuning Trouble
#

#!/usr/lib/python3

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *

# start of packet marker ( 4 characters that are all different )

def decodeMessage(message, numCharacters):    

    code = message[0]
    for index in range(1,len(message)):

        # Get next character
        character = message[index]

        # Does this new character exist in previous message
        # Skip x forward
        for mIndex in range( 0, len(code) ):
            if character == code[mIndex]:
                code = code[mIndex+1:]
                break
        
        code += character

        # If our code is big enough return it
        if len(code) == numCharacters:
            return index + 1

    return 0

def decodeSmallMessage(message):
    return decodeMessage(message,4)

def decodeLargeMessage(message):
    return decodeMessage(message,14)

def solvePuzzle1(filename):
    file = open(filename)
    message = file.read()
    return decodeSmallMessage(message)

def solvePuzzle2(filename):
    file = open(filename)
    message = file.read()
    return decodeLargeMessage(message)


print("")
print_color("Day 6: Tuning Trouble", bcolors.OKGREEN)
print("")

unittest(decodeSmallMessage, 7, "mjqjpqmgbljsphdztnvjfqwrcgsmlb")
unittest(decodeSmallMessage, 5, "bvwbjplbgvbhsrlpgdmjqwftvncz")
unittest(decodeSmallMessage, 6, "nppdvjthqldpwncqszvftbrmjlhg")
unittest(decodeSmallMessage, 10, "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg")
unittest(decodeSmallMessage, 11, "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw")

unittest(decodeLargeMessage, 19, "mjqjpqmgbljsphdztnvjfqwrcgsmlb")
unittest(decodeLargeMessage, 23, "bvwbjplbgvbhsrlpgdmjqwftvncz")
unittest(decodeLargeMessage, 23, "nppdvjthqldpwncqszvftbrmjlhg")
unittest(decodeLargeMessage, 29, "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg")
unittest(decodeLargeMessage, 26, "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw")

unittest(solvePuzzle1, 1794, "puzzleinput.txt")
unittest(solvePuzzle2, 2851, "puzzleinput.txt")