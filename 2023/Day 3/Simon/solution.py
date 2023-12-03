#!/usr/lib/python3

import sys
import re
from colorama import Fore
# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import loadfile

TEST_1_EXPECTED = 4361

def contains_symbols(string, search=re.compile(r'[^0-9.]').search):
    """
    Check if a string contains symbols.

    Args:
        string (str): The input string to check.

    Returns:
        bool: True if the string contains symbols, False otherwise.
    """
    return not bool(search(string))

def check_part_number(schematic, line_index, start_index, end_index):
    """
    Check if the part number at the given line index, start index, and end index is valid.
    
    Args:
        line_index (int): The index of the line containing the part number.
        start_index (int): The starting index of the part number.
        end_index (int): The ending index of the part number.
    
    Returns:
        bool: True if the part number is valid, False otherwise.
    """
    if line_index == 0:
        next_line_index = line_index + 1
        next_line = schematic[next_line_index]
        previous_line = None
    elif line_index == len(schematic) - 1:
        previous_line_index = line_index - 1
        previous_line = schematic[previous_line_index]
        next_line = None
    else:
        next_line_index = line_index + 1
        next_line = schematic[next_line_index]
        previous_line_index = line_index - 1
        previous_line = schematic[previous_line_index]
    current_line = schematic[line_index]

    if next_line is not None:
        if contains_symbols(next_line[start_index-1:end_index+1]):
            return True
    if previous_line is not None:
        if contains_symbols(previous_line[start_index-1:end_index+1]):
            return True
    if contains_symbols(current_line[start_index-1]) or contains_symbols(current_line[end_index+1]):
        return True

    return False

def find_part_number_total(schematic):
    """
    Find the total of all valid part numbers in the schematic.

    Args:
        schematic (list): The schematic to find the total of.

    Returns:
        int: The total of all part numbers in the schematic.
    """
    sum_of_part_numbers = 0

    for line in schematic:
        number_ongoing = False
        number_start_index = 0
        number_end_index = 0
        current_index = 0

        for char in line:
            if char.isnumeric():
                if not number_ongoing:
                    number_ongoing = True
                    number_start_index = current_index
                    print(Fore.YELLOW + "Number started at line " + str(schematic.index(line)) + ", index " + str(current_index) + " with value " + char + Fore.RESET)
                else:
                    number_end_index = current_index
                    print(Fore.YELLOW + "Number continued at line " + str(schematic.index(line)) + ", index " + str(current_index) + " with value " + char + Fore.RESET)
            else:
                if number_ongoing:
                    number_ongoing = False
                    print(Fore.YELLOW + "Number ended at line " + str(schematic.index(line)) + ", index " + str(current_index) + " with value " + char + Fore.RESET)
                    number = int(line[number_start_index:number_end_index+1])
                    print(Fore.YELLOW + "Number is " + str(number) + Fore.RESET)
                    if check_part_number(schematic, schematic.index(line), number_start_index, number_end_index):
                        sum_of_part_numbers += number
                        print(Fore.GREEN + "Sum is now " + str(sum_of_part_numbers) + Fore.RESET)

            current_index += 1

    return sum_of_part_numbers

def main():
    """
    Main function.
    """
    test1_sum = find_part_number_total(loadfile('test.txt'))
    if test1_sum != TEST_1_EXPECTED:
        print(Fore.RED + 'Test 1 Failed: Expected ' + str(TEST_1_EXPECTED) + ', got ' + str(test1_sum))
    else:
        print(Fore.GREEN + 'Test 1 Passed' + Fore.RESET)
        print(" ")
        print(Fore.GREEN + 'Part 1 Solution: ' + str(find_part_number_total(loadfile('input.txt'))))

main()
