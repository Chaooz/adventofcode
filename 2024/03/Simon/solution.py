#!/usr/lib/python3
"""
    Description: File to solve the Advent of Code 2024 Day 3 puzzle

    Returns:
        str: The solution to the puzzle
"""
import sys, re
sys.path.insert(1, '../../../Libs')
from advent_libs import loadfile, loadfile_as_string

SAMPLE_DATA = loadfile_as_string("sample_input.txt")
SAMPLE_DATA_2 = loadfile_as_string("sample_input_2.txt")
SAMPLE_EXPECTED_1 = 161
SAMPLE_EXPECTED_2 = 48
TEST1_OK = False
TEST2_OK = False
DATA = loadfile_as_string("input.txt")

def part1_sample(INPUT):
    """
    Will test the sample data for part 1

    Args:
        INPUT (list): A list of strings

    Returns:
        bool: True or False based on the result of the test
    """
    global TEST1_OK
    if parse_input_1(INPUT) == SAMPLE_EXPECTED_1:
        TEST1_OK = True
        return True

def part2_sample(INPUT):
    """
    Will test the sample data for part 2

    Args:
        INPUT (string): A string

    Returns:
        bool: True or False based on the result of the test
    """
    global TEST2_OK
    if parse_input_2(INPUT) == SAMPLE_EXPECTED_2:
        TEST2_OK = True
        return True

def part1(INPUT):
    """
    Will test the actual data for part 1
    
    Args:
        INPUT (list): A list of strings
        
    Returns:
        int: The solution to part 1
    """
    global TEST1_OK
    if TEST1_OK:
        return parse_input_1(INPUT)

def part2(INPUT):
    """
    Will test the actual data for part 2
    
    Args:
        INPUT (string): A string
        
    Returns:
        int: The solution to part 2
    """
    global TEST2_OK
    if TEST2_OK:
        return parse_input_2(INPUT)

def parse_input_1(INPUT):
    """
    Will parse the input data and return the sum of the multiplication

    Args:
        INPUT (list): A list of ints

    Returns:
        int: The sum of the multiplication
    """
    NUMBERS = []
    LINES = re.findall(r"mul\(\d+,\d+\)", INPUT)
    for LINE in LINES:
        LINE = LINE.lstrip('mul(').rstrip(')').split(',')
        NUMBER = int(LINE[0]) * int(LINE[1])
        NUMBERS.append(NUMBER)
    return sum(NUMBERS)

def parse_input_2(INPUT):
    """
    Will parse the input data and return the sum of the multiplication

    Args:
        INPUT (list): A list of ints

    Returns:
        int: The sum of the multiplication
    """
    NUMBERS = []
    INPUT = INPUT.replace("don't", "end").replace("do", "start")
    INPUT = f"start{INPUT}end"
    LINES = re.findall(r"(?<=start)(.*?)(?=end)", INPUT)
    for LINE in LINES:
        MULS = re.findall(r"mul\(\d+,\d+\)", LINE)
        for MUL in MULS:
            MUL = MUL.lstrip("mul(").rstrip(")").split(",")
            NUMBER = int(MUL[0]) * int(MUL[1])
            NUMBERS.append(NUMBER)
    return sum(NUMBERS)

def run_part1():
    """
    Will run the tests for part 1
    
    Args:
        None
        
    Returns: Nothing
    """
    if part1_sample(SAMPLE_DATA):
        print("Part 1 Sample Test Passed")
        print(f"The solution to part1 is {part1(DATA)}")
    else:
        print("Part 1 Sample Test Failed")
        
def run_part2():
    """
    Will run the tests for part 2
    
    Args:
        None
        
    Returns: Nothing
    """
    if part2_sample(SAMPLE_DATA_2):
        print("Part 2 Sample Test Passed")
        print(f"The solution to part2 is {part2(DATA)}")
    else:
        print("Part 2 Sample Test Failed")

run_part1()
run_part2()
