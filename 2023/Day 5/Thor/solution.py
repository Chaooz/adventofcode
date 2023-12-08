#!/usr/local/bin/python3
# https://adventofcode.com/2023/day/2

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_vector2 import *
from advent_libs_matrix import *

print("")
print_color("Day 5: If You Give A Seed A Fertilizer", bcolors.OKGREEN)
print("")

#
# Convert the material numbers according to the map
#
def convertData(name, source_material_list:list,conversion_list:list):

    destination_material_list = list()

    # If the map is empty, just return the seeds
    if len(conversion_list) == 0:
        return source_material_list

    # Convert all materials
    for material in source_material_list:
        if material == "":
            continue

        material = int(material)
        num = material

        # Go through the conversion list and see if we can convert the material
        for conversion_rule in conversion_list:
            m = conversion_rule.split(" ")
            d = int(m[0])
            s = int(m[1])
            r = int(m[2])

            # If the material is within the range of the conversion rule, convert it
            if material >= s and material < s + r:
                num = (material - s) + d 

        # Add the converted material to the list
        destination_material_list.append(num)

        #print("Seed number ", seed, " corresponds to ",name," number", num)

    return destination_material_list
       

def solvePuzzle1(filename:str):
    lines = loadfile(filename)

    # List of all materials that needs to be converted
    material_list = list()
    # Table on how to convert materials
    conversion_list = list()
    # Debug, name of the material we are currently reading
    name = ""

    for line in lines:
        line = line.strip("\n")

        # Skip empty lines
        if len(line) == 0:
            continue

        # Read line with seeds
        if line.startswith("seeds:"):
            d = line.split(":")
            material_list = d[1].split(" ")

        # If the line contains numbers, these are material A -> B conversion
        # Just add them to the conversion list
        elif line[0].isnumeric():
            conversion_list.append(line)
        # If the line does NOT contain numbers, it is a header.
        # When we start a new header, go through the converson_list we have made
        # and put the materials through to get the new material number
        else:
            material_list = convertData(name,material_list,conversion_list)
            conversion_list.clear()
            name = line

    # Make sure to read the last line
    material_list = convertData(name,material_list,conversion_list)

    # Get the maeerial with the lowest number
    material = min(material_list)

    return material

def solvePuzzle2(filename:str):
    lines = loadfile(filename)
    sum = 0
    return sum

unittest(solvePuzzle1, 35, "unittest1.txt")
unittest(solvePuzzle1, 318728750, "input.txt")     

unittest(solvePuzzle2, 46, "unittest1.txt")
unittest(solvePuzzle2, 37384986, "input.txt")     
