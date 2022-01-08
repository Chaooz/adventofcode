
#
# Day 12 Passage Pathing : https://adventofcode.com/2021/day/12
# 

import sys
#from Libs.advent_libs import print_list
sys.path.insert(1, '../Libs')
from advent_libs import *

#
# Code 
#

# Capital letters are BIG caves and can be revisited
def can_revisit(node_list, node_name, max_visits):

    num_visits = 0

    s = str(node_name)
    if s.isupper():
        return True
    else:
        if node_name == "start" or node_name == "end":
            return False

        # Check caves
        for node in node_list:
            if node == node_name:
                num_visits = num_visits + 1
                if num_visits >= max_visits:
                    #print ( "MAX: " + str(num_visits) + str(node_list) + " : " + node_name)
                    #max_visits = 1
                    return False

    return True  

# Get all connected points from a specific point
def get_exits(node_list,from_point):
    lines = list()
    for node in node_list:
        if node[0] == from_point:
            lines.append( node[1] )
    return lines

# Get all connected points TO a specific point
def get_entrance(node_list,from_point):
    lines = list()
    for node in node_list:
        if node[1] == from_point:
            lines.append( node[0] )
    return lines

# Sort key values to make sure start is first and end is last
def sort_values(old_list, start,end):
    new_list = list()
    for entry in old_list:
        if entry[1] == start or entry[0] == end:
            temp = entry[0]
            entry[0] = entry[1]
            entry[1] = temp
        new_list.append(entry)
    return new_list

# Create path until we reach to_point
def create_path(node_list, from_point, to_point, full_path, max_visits):

    num_paths = 0

    full_path.append(from_point)

    # If we have enabled double visit on small caves, check if we visited twice
    if from_point.islower() and max_visits > 1:
        num_visits = 0
        for node in full_path:
            if node == from_point:
                num_visits = num_visits + 1
                if num_visits >= max_visits:
                    #print ( "MAX: " + str(num_visits) + str(node_list) + " : " + node_name)
                    max_visits = 1
                    break

    exits = get_exits( node_list,from_point )
    for exit in exits:
        #print("From [exit] " + str(from_point) + " => " + str(exit))
        if exit != to_point:
            if can_revisit(full_path,exit, max_visits):
                num_paths = num_paths + create_path( node_list, exit, to_point, full_path, max_visits )
        else:
            num_paths = num_paths + 1
            #print ( "Full path" + str(full_path) + " " + to_point )

    entrances = get_entrance(node_list, from_point)
    for entrance in entrances:
        if can_revisit(full_path, entrance, max_visits) and entrance != to_point:
            #print("From [entrance] " + str(from_point) + " => " + str(entrance))
            num_paths = num_paths + create_path( node_list, entrance, to_point, full_path, max_visits )

    full_path.pop()

    return num_paths

def run_pathing(filename):
    node_list = listFromFile(filename, "-")
    node_list = sort_values(node_list, "start", "end")
    full_path = list()
    num_paths = create_path(node_list, "start", "end", full_path, 1)
    return num_paths

def run_pathing_two(filename):
    node_list = listFromFile(filename, "-")
    node_list = sort_values(node_list, "start", "end")
    full_path = list()
    num_paths = create_path(node_list, "start", "end", full_path, 2)
    return num_paths

# Run unittests
unittest(run_pathing,10,"day12_data_unittest1.txt")
unittest(run_pathing,19,"day12_data_unittest2.txt")
unittest(run_pathing,226,"day12_data_unittest3.txt")
unittest(run_pathing_two,36,"day12_data_unittest1.txt")
unittest(run_pathing_two,103,"day12_data_unittest2.txt")
unittest(run_pathing_two,3509,"day12_data_unittest3.txt")

# Actual assignment
unittest(run_pathing,4885,"day12_data_puzzle.txt")
unittest(run_pathing_two,117095,"day12_data_puzzle.txt")
