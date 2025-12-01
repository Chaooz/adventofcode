#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/0

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *
from collections import defaultdict

def createComputerLink(filename):
    lines = loadfile(filename)
    computerLink = defaultdict(set)
    for line in lines:
        pc1, pc2 = line.split("-")
        computerLink[pc1].add(pc2)
        computerLink[pc2].add(pc1)
    return computerLink

def solvePuzzle1(filename):
    computerLink = createComputerLink(filename)

    # Go through all computers and see if they have 3 computers that are connected to each other
    total = 0
    for network1 in computerLink:
        for network2 in computerLink[network1]:
            for network3 in computerLink[network1]:
                if network2 != network3:
                    if network2 in computerLink[network3]:
                        total += any(node.startswith('t') for node in (network1, network2, network3))        

    return total // 6


def max_group(computerLink, nodes):
    if len(nodes) == 0:
        return set()
    if len(nodes) == 1:
        return nodes

    temp_nodes = nodes.copy()
    node = temp_nodes.pop()

    group_without = max_group(computerLink, temp_nodes)

    # Find all elements in temp_notes that are in the computerLink[node] list
    # This will give us the nodes that are connected to the current node
    # If max_group returns a blank set, then we will return the current node
    group_with = max_group(computerLink, computerLink[node] & temp_nodes) | {node}
#    print("Node: ", len(clique_with), len(clique_without), clique_with, clique_without)

    return group_with if len(group_with) > len(group_without) else group_without

def connectedList(computerLink, key):

    outList = set()
    nodes = computerLink[key]
    for node in nodes:
        if key in computerLink[node]:
            outList.add(node)
    return outList

def solvePuzzle2(filename):
    computerLink = createComputerLink(filename)
    result = None

    nodes = set(computerLink.keys())

#    for key in nodes:
#        outNodes = connectedList(computerLink, key)
#        print(key, outNodes)
#        if result is None or len(outNodes) > len(result):
#            result = outNodes

    result = ','.join(x for x in sorted(max_group(computerLink, nodes)))
#    print(result)
#    b = computerLink["am"] & nodes
#    print(str(b))

    return result

setupCode("Day 23: LAN Party")

unittest(solvePuzzle1, 7, "unittest1.txt")
unittest(solvePuzzle2, "co,de,ka,ta", "unittest1.txt")

runCode(23,solvePuzzle1, 1370, "input.txt")
runCode(23,solvePuzzle2, "am,au,be,cm,fo,ha,hh,im,nt,os,qz,rr,so", "input.txt")