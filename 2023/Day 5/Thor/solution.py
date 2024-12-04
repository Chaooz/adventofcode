#!/usr/local/bin/python3
# https://adventofcode.com/2023/day/2

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_vector2 import *
from advent_libs_matrix import *

setupCode("Day 5: If You Give A Seed A Fertilizer")

class ConversionRuleSet:

    rules : list

    def __init__(self):
        self.rules = list()

    def addRule(self, line:str):
        dest,source,range = line.split(" ")
        self.rules.append((int(dest),int(source),int(range)))

    def convertOne(self,material_list) -> list:
        new_material_list = list()
        for material in material_list:
            new_material = material
            for dest,source,range in self.rules:
                # If the material is within the range of the conversion rule, convert it
                if material >= source and material < source + range:
                    new_material = (material - source) + dest             
            new_material_list.append(new_material)
        return new_material_list
    
    def convertRange(self, material_range) -> list:

        converted_material_range = []

        # Go through all rules in this group
        for dest,source_start,range in self.rules:
            source_end = source_start + range
            new_material_range = []

#            print(material_range, " rule : ", str(source_start) + "-" + str(source_end), " -> ", str(dest) + "-" + str(dest+range))

            for material_start, material_end in material_range:

                # Outside range -> lower (try it on next rule)
                before_rule = (material_start,min(material_end,source_start))
                if before_rule[1] > before_rule[0]:
                    new_material_range.append(before_rule)

                # Inside range -> convert (skip remaining rules to only convert data once)
                match_rule = (max(material_start, source_start), min(source_end, material_end))
                if match_rule[1] > match_rule[0]:
                    diff = dest - source_start
                    converted_material = ((match_rule[0]+diff, match_rule[1]+diff))
                    converted_material_range.append(converted_material)

                # Outside range -> higher (try it on next rule)
                after_rule = (max(source_end, material_start), material_end)
                if after_rule[1] > after_rule[0]:
                    new_material_range.append(after_rule)

            # Set the material range to the outside range materials
            material_range = new_material_range

        # Add remailing outside ranges
        return converted_material_range + material_range
                   
#
# Read all data
#
def readData(filename:str) -> list:
    lines = loadfile(filename)

    material_list = list()
    conversion_list = list()
    conversion_rule = ConversionRuleSet()

    for line in lines:
        line = line.strip("\n")

        # Skip empty lines
        if len(line) == 0:
            continue

        # Read line with seeds
        if line.startswith("seeds:"):
            d = line.split(":")
            material_list: list = [int(x) for x in d[1].split()]

        # If the line contains numbers, these are material A -> B conversion
        # Just add them to the conversion list
        elif line[0].isnumeric():
            conversion_rule.addRule(line)

        # If the line does NOT contain numbers, it is a header.
        # When we start a new header, go through the converson_list we have made
        # and put the materials through to get the new material number
        elif len(conversion_rule.rules) > 0:
            conversion_list.append(conversion_rule)
            conversion_rule = ConversionRuleSet()

    conversion_list.append(conversion_rule)
    return material_list,conversion_list


def solvePuzzle1(filename:str):

    material_list, conversion_list = readData(filename)

    # Convert data
    for conversion_rule in conversion_list:
        material_list = conversion_rule.convertOne(material_list)

    # Get the material with the lowest number
    material = min(material_list)
    return material

def solvePuzzle2(filename:str):
    material_list, conversion_list = readData(filename)

    # Convert material list to a key/value pair with start and end
    material_range = []
    for index in range(0,int(len(material_list) / 2)):
        mat_start = material_list[index*2]
        mat_range = material_list[index*2+1]
        material_range.append((mat_start,mat_start+mat_range))

    # Convert data
    for conversion_rule in conversion_list:
        material_range = conversion_rule.convertRange(material_range)

    # Get the material with the lowest number
    sum = min([x for x,y in material_range])
    return sum

unittest(solvePuzzle1, 35, "unittest1.txt")
unittest(solvePuzzle1, 318728750, "input.txt")     

runCode(5,solvePuzzle2, 46, "unittest1.txt")
runCode(5,solvePuzzle2, 37384986, "input.txt")     
