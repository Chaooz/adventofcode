#!/usr/lib/python3
"""
    Description: Script to solve the Advent of Code 2024 Day 4 puzzle

    Returns:
        str: The solution to the puzzle
"""
import sys, re
sys.path.insert(1, '../../../Libs')
from advent_libs_matrix import *

expected_result_1 = 143
expected_result_2 = 123
input_2 = []
sample_input_2 = []

def get_input(filename):
    books = []
    rules = []

    raw_data = loadfile(filename)

    for line in raw_data:
        if re.match(r'\d+\|\d+', line):
            line = tuple(map(int, line.split('|')))
            rules.append(line)
        elif line == '':
            continue
        else:
            books.append(line)

    return books,rules

def solve_part_1(file_name):
    global input_2, sample_input_2
    books,rules = get_input(file_name)
    book_list_valid = True
    result = 0
    
    part_2_input = []
    
    for line in books:
        book_list = []
        tmp_list = line.split(',')
        for book in tmp_list:
            book_list.append(int(book))
        book_list_valid = True
        for book in book_list:
            if book_list_valid == False:
                break
            for rule in rules:
                if book == rule[0] and rule[1] in book_list and book_list.index(book) > book_list.index(rule[1]):
                    book_list_valid = False
                    part_2_input.append(book_list)
                    break
                else:
                    book_list_valid = True
                    continue
            
        if book_list_valid:
            book_list_len = len(book_list)
            middle_book_index = int((book_list_len -1) / 2)
            middle_book = book_list[middle_book_index]
            result += int(middle_book)
        if len(rules) > 22:
            input_2 = part_2_input
        else:
            sample_input_2 = part_2_input
    return result

def solve_part_2(input):
    result = 0
    book_list_valid = False
    rules = []

    if len(input) > 3:
        books,rules = get_input("input.txt")
    else:
        books,rules = get_input("sample_input.txt")
        
    # print(f"Input before: {input}")
    
    for book_list in input:
        # print(f"Book list: {book_list}")
        book_list_valid = False
        while book_list_valid == False:
            
            book_list_valid = True
            for book in book_list:
                for rule in rules:
                    if book == rule[0] and rule[1] in book_list and book_list.index(book) > book_list.index(rule[1]):
                        # print("Rule", rule)
                        book_list.remove(book)
                        idx = book_list.index(rule[1])
                        # print(f"Book: {book} is in the wrong place. Moving to index {idx}")
                        # print(f"Removed book: {book} - List is now: {book_list}")
                        book_list.insert(idx, book)
                        # print(f"Inserted book at index {idx} - Book list is now: {book_list} ")
                        book_list_valid = False
                        break
#                i += 1

 #           if i == len(book_list):
 #               book_list_valid = True
 #               break
                
        if book_list_valid:
            # print(f"Book list: {book_list}")
            book_list_len = len(book_list)
            middle_book_index = int((book_list_len -1) / 2)
            middle_book = book_list[middle_book_index]
            result += int(middle_book)
    
    return result
    
if solve_part_1("sample_input.txt") == expected_result_1:
    print(f"Test 1 OK. The result of the sample data is {solve_part_1('sample_input.txt')} which matches the expected result of {expected_result_1}.")
    print(f"The result of part 1 is {solve_part_1('input.txt')}.")
else:
    print(f"Test 1 FAILED. The result of the sample data is {solve_part_1('sample_input.txt')} which does not match the expected result of {expected_result_1}.")

bb = solve_part_2(sample_input_2)
if bb == expected_result_2:
    print(f"Test 2 OK. The result of the sample data is {solve_part_2(sample_input_2)} which matches the expected result of {expected_result_2}.")
    print(f"The result of part 2 is {solve_part_2(input_2)}.")
else:    
    print(f"Test 2 FAILED. The result of the sample data is {bb} which does not match the expected result of {expected_result_2}.")
    print(sample_input_2)
