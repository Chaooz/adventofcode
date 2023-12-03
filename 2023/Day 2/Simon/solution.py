#!/usr/lib/python3

import sys
from colorama import Fore
# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *

# Constants
MAX_RED_CUBES = 12
MAX_GREEN_CUBES = 13
MAX_BLUE_CUBES = 14
TEST_1_EXPECTED = 8
TEST_2_EXPECTED = 2286

####################################################################################################
def get_game_id(game):
    return int(game.split(":")[0].split()[1])

####################################################################################################
def check_validity(game):
    valid = True

    global MAX_RED_CUBES
    global MAX_GREEN_CUBES
    global MAX_BLUE_CUBES

    draws = game.split(":")[1].split(";")

    for draw in draws:
        cube_set = draw.split(",")
        for color in cube_set:
            if color.split()[1] == "red":
                if int(color.split()[0]) > MAX_RED_CUBES:
                    valid = False
            elif color.split()[1] == "green":
                if int(color.split()[0]) > MAX_GREEN_CUBES:
                    valid = False
            elif color.split()[1] == "blue":
                if int(color.split()[0]) > MAX_BLUE_CUBES:
                    valid = False

    return valid

####################################################################################################
def find_game_sum(game_list):
    valid_game_sum = 0

    for game in game_list:
        if check_validity(game) == True:
            valid_game_sum += get_game_id(game)

    return valid_game_sum

####################################################################################################
def code_test_1(game_list):
    valid_game_sum = find_game_sum(game_list)

    if valid_game_sum == TEST_1_EXPECTED:
        return True
    else:
        return False

####################################################################################################
def min_possible_cubes(game):
    min_red_cubes = 0
    min_green_cubes = 0
    min_blue_cubes = 0

    draws = game.split(":")[1].split(";")

    for draw in draws:
        cube_set = draw.split(",")
        for color in cube_set:
            if color.split()[1] == "red":
                if int(color.split()[0]) > min_red_cubes:
                    min_red_cubes = int(color.split()[0])
            elif color.split()[1] == "green":
                if int(color.split()[0]) > min_green_cubes:
                    min_green_cubes = int(color.split()[0])
            elif color.split()[1] == "blue":
                if int(color.split()[0]) > min_blue_cubes:
                    min_blue_cubes = int(color.split()[0])
    
    return [min_red_cubes, min_green_cubes, min_blue_cubes]

####################################################################################################
def find_game_product(cube_set):
    red_cubes = int(cube_set[0])
    green_cubes = int(cube_set[1])
    blue_cubes = int(cube_set[2])

    return red_cubes * green_cubes * blue_cubes

####################################################################################################
def find_sum_of_products(game_list):
    sum_of_products = 0

    for game in game_list:
        cube_set = min_possible_cubes(game)
        sum_of_products += find_game_product(cube_set)

    return sum_of_products

####################################################################################################
def code_test_2(game_list):
    sum_of_products = find_sum_of_products(game_list)

    if sum_of_products == TEST_2_EXPECTED:
        return True
    else:
        return False
    
####################################################################################################
def main():
    # Load the input file
    test_game_list = loadfile("test1.txt")

    # Test the logic of the program
    test_result_1 = code_test_1(test_game_list)
    test_result_2 = code_test_2(test_game_list)

    if test_result_1 is True:
        print(Fore.GREEN + "Test 1 successful." + Fore.RESET)
    else:
        print(Fore.RED + "Test 1 failed.")
        print("Expected: " + str(TEST_1_EXPECTED))
        print("Received: " + str(find_game_sum(test_game_list)) + Fore.RESET)
        print("")
    
    if test_result_2 is True:
        print(Fore.GREEN + "Test 2 successful." + Fore.RESET)
    else:
        print(Fore.RED + "Test 2 failed.")
        print("Expected: " + str(TEST_2_EXPECTED))
        print("Received: " + str(find_game_sum(test_game_list)) + Fore.RESET)
        print("")
    
    # Load the input file
    game_list = loadfile("input.txt")

    # Find the sum of the valid games
    valid_game_sum = find_game_sum(game_list)
    sum_of_products = find_sum_of_products(game_list)

    # Print the result
    print("The sum of the valid games is: " + str(valid_game_sum))
    print("The sum of the products is: " + str(sum_of_products))

main()
