#!/usr/local/bin/python3
# https://adventofcode.com/2023/day/2

import sys
import math

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_vector2 import *
from advent_libs_matrix import *

print("")
print_color("Day 12: Hot Springs", bcolors.OKGREEN)
print("")

SYMBOL_LIST = ".#?"

def match_numbers(decoded:str, codes):
    code_block = codes.split(",")
    blocks = decoded.split(".")
    i = 0

    nonemty_blocks = []
    for block in blocks:
        if block != "":
            nonemty_blocks.append(block)

    if len(nonemty_blocks) != len(code_block):
        return False

    for b in nonemty_blocks:
        if b == "":
            continue

        if i >= len(code_block):
            return False

        if len(b) != int(code_block[i]):
            return False

        i = i + 1

    return i == len(code_block)

#
# Get all permutations
#
def get_permutations(encoded:str) -> dict:

    if encoded == "":
        return [""]

    return [
        x + y
        for x in (".#" 
                  if encoded[0] == "?" 
                  else encoded[0])
        for y in get_permutations(encoded[1:])
    ]

#
# Only get the permutations that are possible
#
def get_possible_permutations(cache, encoded:str, encode_index:int, codes:str, code_index:int, current_code_length:int) -> int:

    key = (encode_index, code_index, current_code_length)
    if key in cache:
        return cache[key]

    # End of line ?
    if encode_index == len(encoded):

        # Found all codes ?
        if code_index == len(codes):
            #print("EOD: found all codes -> 1")
            return 1
        
        # Is on the last code
        elif code_index == len(codes) - 1 and codes[code_index] == current_code_length:
            #print("EOD: found last code -> 1")
            return 1
        
        #print("EOD: found nothing", code_index, encode_index, current_code_length)
        return 0


    # Get the character
    encoded_char = encoded[encode_index]

    decoded = 0

    for char in [".","#"]:

        # We have a match
        if encoded_char == char or encoded_char == "?":
            #print("Encoded char:", encoded_char, " variant:", char, " codeIndex", code_index, "l1:", codes[code_index], " l2:", current_code_length)

            # If we start the block with a . and we have no number
            # Just increase index for the encoded string and try next character
            if char == "." and current_code_length == 0:
                #print("1:Just increase index and move on. Char:", char, "Encoded:",encoded_char)
                decoded += get_possible_permutations(cache, encoded, encode_index + 1, codes, code_index, 0)

            # If we start the block with a . and we have a code it means the end of the current code
            # Check that the length of the code matches
            # We cannot start a new code if we are out of codes
            elif char == "." and current_code_length > 0 and code_index < len(codes) and codes[code_index] == current_code_length:
                #print("2: End current code block Char:", char, "Encoded:",encoded_char)
                decoded += get_possible_permutations(cache, encoded, encode_index + 1, codes, code_index + 1, 0)

            # Increase length of code if its not long enough
            elif char == "#" and code_index < len(codes) and current_code_length < codes[code_index]:
                #print("3: Increase code length. Char:", char, "Encoded:",encoded_char)
                decoded += get_possible_permutations(cache, encoded, encode_index + 1, codes, code_index, current_code_length + 1)

    cache[key] = decoded
    return decoded
 
def solveLine(line:str):

    encoded,codes = line.split(" ")

    codes = [ int(x) for x in codes.split(",") ]
    cache = {}
    sum = get_possible_permutations(cache,encoded,0, codes, 0, 0)

    return sum

def solveLine2(line:str):

    encoded,codes = line.split(" ")

    factor = 5

    # Increase line with a factor of X
    new_encoded = ""
    new_codes = ""
    for i in range(0,factor):
        if new_encoded != "":
            new_encoded += "?"
        new_encoded += encoded

        if new_codes != "":
            new_codes += ","
        new_codes += codes

    codes = [ int(x) for x in new_codes.split(",") ]
    cache = {}
    sum = get_possible_permutations(cache,new_encoded,0, codes, 0, 0)
    return sum

def solvePuzzle1(filename):
    sum = 0
    lines = loadfile(filename)
    for line in lines:
        sum += solveLine(line)
    return sum

def solvePuzzle2(filename):
    sum = 0
    lines = loadfile(filename)
    for line in lines:
        sum += solveLine2(line)
    return sum

unittest(solveLine, 1 , "#.#.### 1,1,3")
unittest(solveLine, 1 , "???.### 1,1,3")
unittest(solveLine, 10 , "?###???????? 3,2,1")
unittest(solveLine, 4 , ".??..??...?##. 1,1,3")
unittest(solveLine, 1 , "?#?#?#?#?#?#?#? 1,3,1,6")
unittest(solveLine, 1 , "????.#...#... 4,1,1")
unittest(solveLine, 4 , "????.######..#####. 1,6,5")
unittest(solveLine, 10 , "?###???????? 3,2,1")
unittest(solveLine, 1 , ".#?.# 1,1")

unittest(solveLine2, 1 , ".# 1")
unittest(solveLine2, 1 , "???.### 1,1,3")
unittest(solveLine2, 16384 , ".??..??...?##. 1,1,3")
unittest(solveLine2, 506250 , "?###???????? 3,2,1")

unittest(solvePuzzle1, 7307, "input.txt")     

unittest(solvePuzzle2, 525152, "unittest2.txt")
unittest(solvePuzzle2, 3415570893842, "input.txt")     

