#!/usr/local/bin/python3
# https://adventofcode.com/2023/day/2

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_vector2 import *
from advent_libs_matrix import *
from colorama import Fore

EXPECTED_RESULT_TEST_1 = 35
EXPECTED_RESULT_TEST_2 = 46

class Map:
    map : list
    def __init__(self) -> None:
        self.map = []

    def Add(self,material:list):
        self.map.append(material)

    def Get(self,x:int,y:int) -> int:
        return self.map[y][x]
    
    def GetList(self):
        return self.map
    
    def Print(self):
        for material in self.map:
            print(material)

def convert_data(name, seeds, conversion_rule:list):
    converted_data = []

    if len(conversion_rule) == 0:
        return seeds

#    print(conversion_rule)

    for seed in seeds:

        if seed == "":
            continue
            
        seed = int(seed)
        num = seed

        destination = int(conversion_rule[0])
        source = int(conversion_rule[1])
        range = int(conversion_rule[2])
        if seed >= source and seed < source + range:
            num = (seed - source) + destination
        
        converted_data.append(num)

    print("Converted : ", seeds, " to ", converted_data)

    return converted_data

def convert_data_range(name, seeds, map:list):
    converted_data = []

    if len(map) == 0:
        return seeds

    for seed in seeds[0]:

        if seed == "":
            continue
            
        seed = int(seed)
        num = seed
        for material in map:
            material = material.split(" ")
            destination = int(material[0])
            source = int(material[1])
            range = int(material[2])
            if seed >= source and seed < source + range:
                num = (seed - source) + destination
        
        converted_data.append(num)
            
    return converted_data

def process_seeds(input_file):
    lines = loadfile(input_file)

    seeds = []
    name = ""

    for line in lines:
        line = line.strip("\n")

        if len(line) == 0:
            continue

        if line.startswith("seeds:"):
            seed = line.split(":")
            seeds = seed[1].split(" ")
            
        elif line[0].isnumeric():
            conversion_rule = line.split(" ")
            seeds = convert_data(name, seeds, conversion_rule)

    low_seed = min(seeds)
    return low_seed


def process_seeds_range(input_file):
    lines = loadfile(input_file)

    seeds = []
    name = ""

    for line in lines:
        line = line.strip("\n")

        if len(line) == 0:
            continue

        if line.startswith("seeds:"):
            seeds = expand_seed_list(line)
            
        elif line[0].isnumeric():
            conversion_rule = line.split(" ")
            seeds = convert_data_range(name, seeds, conversion_rule)

    low_seed = min(seeds)
    return low_seed

def expand_seed_list(line):

    line = line.split(":")
    number_list = line[1].strip().split(" ")

    number_pairs = []
    for index in range(0,len(number_list)):
        number = int(number_list[index])
        if index % 2 == 0:
            number_pair = [number, 0]
        else:
            number_pair[1] = number
            number_pairs.append(number_pair)
        
    return number_pairs

def main():
    print("Day 5 - Simon")
    if process_seeds("test.txt") == EXPECTED_RESULT_TEST_1:
        print("Part 1 test: " + Fore.GREEN + "PASSED" + Fore.RESET)
        print("Part 1 result: " + Fore.YELLOW + str(process_seeds("input.txt")) + Fore.RESET)
    else:
        print("Part 1 test: " + Fore.RED + "FAILED" + Fore.RESET)
        print("Expected: " + str(EXPECTED_RESULT_TEST_1) + " Got: " + str(process_seeds("test.txt")))

    if process_seeds_range("test.txt") == EXPECTED_RESULT_TEST_2:
        print("Part 2 test: " + Fore.GREEN + "PASSED" + Fore.RESET)
        print("Part 2 result: " + Fore.YELLOW + str(process_seeds_range("input.txt")) + Fore.RESET) 
    else:
        print("Part 2 test: " + Fore.RED + "FAILED" + Fore.RESET)

main()
