#!/usr/local/bin/python3
# https://adventofcode.com/2023/day/2

import sys
import math

# Import custom libraries
sys.path.insert(1, '../../../Libs')

from advent_libs import *
from advent_libs_vector2 import *
from advent_libs_matrix import *

setupCode("Day 19: Aplenty")

class Rule:
    char:str
    number:int
    op:str
    next_flow:str    

    def __init__(self, part:str) -> None:
        rule, self.next_flow = part.split(":")
        if rule.find("<") != -1:
            self.char, self.number = rule.split("<")
            self.op = "<"
            self.number = int(self.number)
        else:
            self.char, self.number = rule.split(">")
            self.op = ">"
            self.number = int(self.number)

    def ToString(self):
        return self.char + self.op + str(self.number) + " => " + self.next_flow

class Part:
    name:str
    materials:dict

    def __init__(self, packets:str):
        self.name = packets
        self.materials = dict()

        materials = packets[1:-1].split(",")
        for material in materials:
            material_name, material_number = material.split("=")
            self.materials[material_name] = int(material_number)
    
    def ToString(self):
        s = "Part:" + self.name + " workflow:"
        a = ""
        for workflow in self.workflows:
            if a != "":
                a += " -> "
            a += workflow
        return s + a
    
    def GetRating(self):
        rating = 0
        for key,value in self.materials.items():
            rating += value
        return rating

class Workflow:
    name:str
    defaultRule:str
    rules:list

    def __init__(self, line:str) -> None:
        self.name,block = line[:-1].split("{")
        self.rules = list()
        parts = block.split(",")
        for part in parts:
            if part.find(":") == -1:
                self.defaultRule = part
            else:
                self.rules.append(Rule(part))

    def CheckRule(self,part:Part):
        for rule in self.rules:
            material_number = part.materials[rule.char]
            if rule.op == "<" and material_number < rule.number:
#                print(self.name,"match rule less:", rule.char, rule.op, rule.number, " material:", material_name, material_number, " next workflow:", rule.next_flow)
                return rule.next_flow
            elif rule.op == ">" and material_number > rule.number:
#                print(self.name, "match rule more", rule.char, rule.op, rule.number, " material:", material_name, material_number, "next workflow:", rule.next_flow)
                return rule.next_flow

        return self.defaultRule
        
    def ToString(self):
        s = self.name + " ["
        for rule in self.rules:
            s += rule.char + rule.op + str(rule.number) + " => " + rule.next_flow + ", "
        s += self.defaultRule
        s += "]"
        return s

#
# Parse the input file
#
def readInput(filename):
    block = False
    workflow_list = dict()
    parts = list()

    lines = loadfile(filename)
    for line in lines:
        if line == "":
            block = True
            continue

        if block == False:
            workflow = Workflow(line)
            workflow_list[workflow.name] = workflow
        else:
            parts.append(Part(line))

    return workflow_list, parts

def solvePuzzle1(filename):
    sum = 0
    workflow_list, parts = readInput(filename)

    for part in parts:
        workflow = workflow_list["in"]
        while workflow != None:
            next_flow = workflow.CheckRule(part)
            if next_flow == "A":
                sum += part.GetRating()
                workflow = None
                continue
            elif next_flow == "R":
                workflow = None
                continue
            else:
                workflow = workflow_list[next_flow]
    return sum

def solvePuzzle2(filename):
    workflow_list, parts = readInput(filename)
    accepted_ranges_list = []

    ranges = {
        "x": (1, 4000),
        "m": (1, 4000),
        "a": (1, 4000),
        "s": (1, 4000),
    }

    stack = list()
    stack.append((ranges, "in"))

    while stack:
        ranges, workflow_id = stack.pop()

        # If the default rule is A or R
        if workflow_id == "A": 
            accepted_ranges_list.append(ranges)
            continue
        elif workflow_id == "R":
            continue

        # Get workflow
        workflow = workflow_list[workflow_id]

        # Split ranges based on rules
        for rule in workflow.rules:
            true_range, false_range = ranges.copy(), ranges.copy()
            if rule.op == "<":
                true_range[rule.char] = (true_range[rule.char][0], int(rule.number) - 1)
                false_range[rule.char] = (int(rule.number), false_range[rule.char][1])
            elif rule.op == ">":
                true_range[rule.char] = (int(rule.number) + 1, true_range[rule.char][1])
                false_range[rule.char] = (false_range[rule.char][0], int(rule.number))

            stack.append((true_range, rule.next_flow)) # Add true range to stack to explore new_workflow_id
            ranges = false_range # Update ranges for next iteration in rules loop

        # Defaultrule has the remaining range
        stack.append((ranges, workflow.defaultRule))


    # now we have a list of accepted ranges, we can calculate the number of combinations possible
    sum = 0
    for ranges in accepted_ranges_list:
#        print("ranges: a:", ranges["a"], "m:", ranges["m"], "x:", ranges["x"], "s:", ranges["s"])
        sum += (
            (ranges["x"][1] - ranges["x"][0] + 1)
            * (ranges["m"][1] - ranges["m"][0] + 1)
            * (ranges["a"][1] - ranges["a"][0] + 1)
            * (ranges["s"][1] - ranges["s"][0] + 1)
        )
    return sum

unittest(solvePuzzle1, 19114, "unittest1.txt")     
unittest(solvePuzzle2, 167409079868000, "unittest1.txt")

runCode(19,solvePuzzle1, 421983, "input.txt")     
runCode(19,solvePuzzle2, 129249871135292, "input.txt")     
