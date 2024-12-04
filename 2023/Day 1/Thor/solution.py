#!/usr/local/bin/python3

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_vector2 import *
from advent_libs_matrix import *

setupCode("Day 1: Trebuchet?!")

def replaceWords(line:str):
    line2 = ""
    wordlist = [ "one", "two", "three", "four", "five", "six", "seven", "eight", "nine" ]

    # Relace words
    for i in range(0,len(line)):
#        print("i:" + str(i) + " line:")
        for j in range(0,len(wordlist)):
            word = wordlist[j]
            if line.find(word,i,i+len(word)) > -1:
#                print("word match:" + line + " => " + word)
                line = line[:i] + str(j+1) + line[i+1:]
    return line

# Find first and last number in string
def findFirstAndLastNumber(line:str):
    n = ""
    for i in range(0,len(line)):
        if line[i].isnumeric():
            n += line[i]            
    flip = n[0] + n[len(n)-1]
    a = int(flip,10)
    return a

# Solve one line
def solveLine(line:str):

    # Replace words
    line = replaceWords(line)

    # Find first and last number in string
    numbers = findFirstAndLastNumber(line)
    return numbers

def solvePuzzle1(filename:str):
    lines = loadfile(filename)    
    sum = 0
    for line in lines:
        sum += findFirstAndLastNumber(line)
    return sum

def solvePuzzle2(filename:str):
    lines = loadfile(filename)
    sum = 0
    for line in lines:
        sum += solveLine(line)
    return sum


# Test word replace
unittest(replaceWords, "1ne23hree", "one2three")
unittest(replaceWords, "abc1ne23hreexyz", "abcone2threexyz")

# Test line to number
unittest(solveLine, 13, "one2three")
unittest(solveLine, 83, "eightwothree")
unittest(solveLine, 13, "abcone2threexyz")

unittest(replaceWords, "8ight3hree7even2nnkvlzxkvhszfpqzhl37ddqvnxg", "eightthreeseven2nnkvlzxkvhszfpqzhl37ddqvnxg")
unittest(solveLine, 87, "eightthreeseven2nnkvlzxkvhszfpqzhl37ddqvnxg")

# Test input
unittest(solvePuzzle1, 142, "unittest1.txt")
unittest(solvePuzzle2, 281, "unittest2.txt")

# Solution
runCode(1, solvePuzzle1, 55477, "input.txt")
runCode(1, solvePuzzle2, 54431, "input.txt")
