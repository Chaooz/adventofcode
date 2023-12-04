#!/usr/lib/python3

import sys
# import re
from colorama import Fore
# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import loadfile

TEST_1_EXPECTED = 4361
WRONG_NUMBER = 308
TEST_2_EXPECTED = 467835


def contains_symbols(string:str):
    #, search=re.compile(r'[^0-9.]').search

    """
    Check if a string contains symbols.

    Args:
        string (str): The input string to check.

    Returns:
        bool: True if the string contains symbols, False otherwise.
    """

    for c in string:

        if c == "\n":
            continue
        
        if c.isnumeric() or c == ".":
            continue

        # print("regex:" + c + " True")
        return True

    # print("regex:" + string + " False")
    return False
#    return bool(search(string))

def check_part_number(number, schematic, line_index, start_index, end_index):
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

    # print("Index: [" + str(start_index) + "][" + str(end_index) + "]")

    if start_index < 1:
        start_index = 1

    if next_line is not None:
        if end_index > len(next_line):
            end_index = len(next_line-1)

        if contains_symbols(next_line[start_index-1:end_index+2]):
            if number == WRONG_NUMBER:
                print("next line: " + next_line[start_index-1:end_index+2])
            return True
    if previous_line is not None:
        if end_index > len(previous_line):
            end_index = len(previous_line-1)

        #print("previous line: [" + str(start_index) + "][" + str(end_index) + "]" + previous_line[start_index-1:end_index+2])
        if contains_symbols(previous_line[start_index-1:end_index+2]):
            if number == WRONG_NUMBER:
                print("previous line: " + previous_line[start_index-1:end_index+2])
            return True

    # print("current line: " + current_line)
    # print("previous char: " + current_line[start_index-1])
    # print("next char: " + current_line[end_index+1])
    if contains_symbols(current_line[start_index-1]):
        if number == WRONG_NUMBER:
            print("previous char: " + current_line[start_index-1])
        return True

    if contains_symbols(current_line[end_index+1]):
        if number == WRONG_NUMBER:
            print("next char: " + current_line[end_index+1])
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

        schematic_index = schematic.index(line)
        #line = line.strip("\n")

        #print("Checking line: " + line)
        number_ongoing = False
        number_start_index = 0
        number_end_index = 0
        current_index = 0

        for char in line:
            if char.isnumeric():
                if not number_ongoing:
                    number_ongoing = True
                    number_start_index = current_index
                    number_end_index = current_index
                    # print(Fore.YELLOW + "Number started at line " + str(schematic_index) + ", index " + str(current_index) + " with value " + char + Fore.RESET)
                else:
                    number_end_index = current_index
                    # print(Fore.YELLOW + "Number continued at line " + str(schematic_index) + ", index " + str(current_index) + " with value " + char + Fore.RESET)
            else:
                if number_ongoing:
                    number_ongoing = False
                    # print(Fore.YELLOW + "Number ended at line " + str(schematic_index) + ", index " + str(current_index) + " with value " + char + Fore.RESET)
                    number = int(line[number_start_index:number_end_index+1])
                    if number == WRONG_NUMBER:
                        print(Fore.YELLOW + "Number is " + str(number) + " line:" + str(schematic_index+1) + Fore.RESET)
                    if check_part_number(number, schematic, schematic_index, number_start_index, number_end_index):
                        sum_of_part_numbers += number
                        #print(Fore.GREEN + "Number is valid - " + str(number) + " added to sum" + Fore.RESET)
                        #print(Fore.GREEN + "Sum is now " + str(sum_of_part_numbers) + Fore.RESET)

            current_index += 1

    return sum_of_part_numbers

def get_connected_gear(number, schematic, schematic_index, number_start_index, number_end_index ):
    """
    Check if a given number is connected to a '*' in the schematic.

    Args:
        number (int): The number to check.
        schematic (list): The schematic as a list of strings.
        schematic_index (int): The index of the line in the schematic where the number is located.
        number_start_index (int): The starting index of the number in the line.
        number_end_index (int): The ending index of the number in the line.

    Returns:
        None
    """

    #print("Check if number "+  str(number ) + " is connected to a *")

    b = ""

    startY = schematic_index - 1
    if ( startY < 0 ):
        startY = 0

    endY = schematic_index + 2
    if ( endY > len(schematic) - 1 ):
        endY = len(schematic) - 1

    # Se over,midten,under
    for yy in range(startY, endY):
        line = schematic[yy]

        for xx in range( number_start_index - 1, number_end_index + 2):
            char = line[xx]
            if char == "*":
                return (xx,yy)

    return None




#
# New stuff
#
def find_kewl_stuff(schematic):

    sum_of_part_numbers = 0

    gearList = list()
    temp_stars = []

    for line in schematic:

        schematic_index = schematic.index(line)
        #line = line.strip("\n")

        #print("Checking line: " + line)
        number_ongoing = False
        number_start_index = 0
        number_end_index = 0
        current_index = 0

        for char in line:
            if char.isnumeric():
                if not number_ongoing:
                    number_ongoing = True
                    number_start_index = current_index
                    number_end_index = current_index
                    # print(Fore.YELLOW + "Number started at line " + str(schematic_index) + ", index " + str(current_index) + " with value " + char + Fore.RESET)
                else:
                    number_end_index = current_index
                    # print(Fore.YELLOW + "Number continued at line " + str(schematic_index) + ", index " + str(current_index) + " with value " + char + Fore.RESET)
            else:
                if number_ongoing:
                    number_ongoing = False
                    # print(Fore.YELLOW + "Number ended at line " + str(schematic_index) + ", index " + str(current_index) + " with value " + char + Fore.RESET)
                    number = int(line[number_start_index:number_end_index+1])
                    if number == WRONG_NUMBER:
                        print(Fore.YELLOW + "Number is " + str(number) + " line:" + str(schematic_index+1) + Fore.RESET)


                    if check_part_number(number, schematic, schematic_index, number_start_index, number_end_index):
                        #sum_of_part_numbers += number

                        gear = get_connected_gear(number, schematic, schematic_index, number_start_index, number_end_index )
                        if gear is not None:
                            #print(Fore.GREEN + "Number is valid - " + str(number) + " added to sum" + Fore.RESET)

                            # Hvis stjernen finnes fra før
                            was_found = False
                            for star in temp_stars:
                                if star[0] == gear[0] and star[1] == gear[1]:
                                    old_number = star[2]
                                    sum_of_part_numbers += old_number * number
                                    was_found = True
                                    #print("Found matching pair " + str(old_number) + " and " + str(number) + " with gear [" + str(gear[0]) + "x" + str(gear[1]) + "]" )

                            if not was_found:
                                temp_stars.append( (gear[0],gear[1], number) )
                                #print("Add number to temp_stars")



                        #print(Fore.GREEN + "Sum is now " + str(sum_of_part_numbers) + Fore.RESET)

            current_index += 1

        # Blabla

#    print(temp_stars)

    return sum_of_part_numbers

def find_gears(schematic):
    """
    Find all gears in the schematic.

    Args:
        schematic (list): The schematic to find the gears in.

    Returns:
        list: A list of all gears in the schematic.
    """

    for line in schematic:
        index = schematic.index(line)

        character_position = line.find('*')
        if character_position > -1:
            print(line)

            for yy in range(index-1,index+2):
                test_line = schematic[yy]
                for x in range(character_position-1, character_position+1):
                    char = test_line[x]
                    if char.isnumeric():
                        print("Number found at [" + str(x) + "x" + str(yy) + "] for Gear:" + char)

    #return gears

def main():
    """
    Main function.
    """
    test1_sum = find_part_number_total(loadfile('test.txt'))
    test2_sum = find_kewl_stuff(loadfile('test.txt'))
    if test1_sum != TEST_1_EXPECTED:
        print(Fore.RED + 'Test 1 Failed: Expected ' + str(TEST_1_EXPECTED) + ', got ' + str(test1_sum))
    else:
        print(Fore.GREEN + 'Test 1 Passed' + Fore.RESET)
        print(" ")
        print(Fore.GREEN + 'Part 1 Solution: ' + str(find_part_number_total(loadfile('input.txt'))))

    if test2_sum != TEST_2_EXPECTED:
        print(Fore.RED + 'Test 2 Failed: Expected ' + str(TEST_2_EXPECTED) + ', got ' + str(test2_sum))
    else:
        print(Fore.GREEN + 'Test 2 Passed' + Fore.RESET)
        print(" ")
        print(Fore.GREEN + 'Part 2 Solution: ' + str(find_kewl_stuff(loadfile('input.txt'))))

main()
