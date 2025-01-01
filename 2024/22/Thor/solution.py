#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/22

import sys
import re
import math
from collections import defaultdict

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *

def calcSecret(secret):
    number = int(secret)
    number = ((number * 64) ^ number) % 16777216
    number = ((number // 32) ^ number) % 16777216
    number = ((number * 2048) ^ number) % 16777216
    return number

def solvePuzzle1(filename):
    lines = loadfile(filename)
    sum = 0
    for line in lines:
        secret = int(line)
        for n in range(2000):
            secret = calcSecret(secret)
        sum += secret
    return sum

def solvePuzzle2(filename):
    lines = loadfile(filename)
    sum = 0

    # Generate price list
    priceList = []
    for line in lines:
        secret = int(line)
        priceList.append( [secret % 10] )
        for _ in range(2000):
            secret = calcSecret(secret)
            priceList[-1].append(secret % 10)

    diff_table = defaultdict(int)
    for p in priceList:
        d = set()
        for i in range(4, len(p)):
            diff = (p[i-3] - p[i-4], p[i-2] - p[i-3], p[i-1] - p[i-2], p[i] - p[i-1])
            if diff in d:
                continue
            diff_table[diff] += p[i]
            d.add(diff)
    sum = (max(diff_table.values()))
    return sum

setupCode("Day 22: Monkey Market")

unittest(calcSecret, 15887950, "123")
unittest(calcSecret, 16495136, "15887950")

unittest(solvePuzzle1, 37327623, "unittest1.txt")
unittest(solvePuzzle2, 23, "unittest2.txt")

runCode(22,solvePuzzle1, 17163502021, "input.txt")
runCode(22,solvePuzzle2, 1938, "input.txt")