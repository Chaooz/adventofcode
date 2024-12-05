#!/usr/local/bin/python3
# https://adventofcode.com/2024/day/4

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *
from advent_libs_matrix import *

setupCode("Day 5: Print Queue ")

def pageMatchAnyRule(page, rules):
    for rule in rules:
        if page == rule:
            return True
    return False

#
# Check if all pages in a book matches the ruleset
#
def bookMatchesRule(book,rules):
    for i in range(1, len(book)):
        page1 = str( book[i - 1] )
        page2 = str( book[i])
        pageRule = page1 + "|" + page2
        if pageMatchAnyRule(pageRule, rules) == False:
            return False
    return True

#
# Iterate through the book and order the pages according to the rules
# If two pages are not in the correct order, swap them and check if the new order is correct
#
def orderPages(book, rules):
    sortedBook = book.copy()

    # Keep running this until all the pages matches a rule in the ruleset
    while(True):

        sorted = True

        for i in range(1, len(sortedBook)):
            page1 = str( sortedBook[i - 1] )
            page2 = str( sortedBook[i])

            pageRule = page1 + "|" + page2
            flippedRule = page2 + "|" + page1

            if pageMatchAnyRule(pageRule, rules):
                continue
            
            # If the page matches a flipped rule, swap the pages
            elif pageMatchAnyRule(flippedRule, rules):
                sortedBook[i - 1] = page2
                sortedBook[i] = page1
                sorted = False

        # All pages are sorted, break the loop
        if sorted == True:
            break

    return sortedBook

#
# Read the input file and return the rules and the books
#
def readInput(filename):
    lines = loadfile(filename)
    rules = []
    books = []

    for line in lines:
        if line.rstrip() == "":
            continue
        elif line.find("|") > -1:
            rules.append(line)
        else: 
            pages = line.split(",")
            books.append(pages)

    return rules, books

#
# Sum all the books that matches the rule
#
def solvePuzzle1(filename):
    rules, books = readInput(filename)

    # Sum all the books that matches the rule
    sum = 0
    for book in books:
        if bookMatchesRule(book, rules):
            # Only add the middle page of the book
            i = int(len(book) / 2)
            sum += int(book[i])
    return sum

#
# We want to sum all the pages we need to reorder in the book to make it follow the rules
#
def solvePuzzle2(filename):
    rules, books = readInput(filename)

    sum = 0
    for book in books:
        # If the book does not match the rule, order the pages
        if bookMatchesRule(book, rules) == False:
            sortedBook = orderPages(book, rules)
            i = int(len(sortedBook) / 2)
            m = int(sortedBook[i])
            sum += m
    return sum

unittest(solvePuzzle1, 143, "unittest1.txt")
unittest(solvePuzzle2, 123, "unittest1.txt")

runCode(5,solvePuzzle1, 5374, "input.txt")
runCode(5,solvePuzzle2, 4260, "input.txt")

