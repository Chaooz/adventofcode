#!/usr/lib/python3

import sys
from colorama import Fore
# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import loadfile

TEST_1_EXPECTED = 13
TEST_2_EXPECTED = 30

def get_card_points(input):
    """
    Calculates the total points earned from a given input of card numbers and winning numbers.

    Args:
        input (list): A list of strings representing each line of input.

    Returns:
        int: The total points earned from the card numbers.

    """
    card_points = 0
    for line in input:
        card_numbers = line.split("|")[1].split()
        winning_numbers = line.split("|")[0].split(":")[1].split()
        number = 0

        for card_number in card_numbers:
            if card_number in winning_numbers:
                if number == 0:
                    number = 1
                else:
                    number *= 2
        card_points += number
    return card_points

def generate_deck(input):
    card_deck = []
    for line in input:
        card_numbers = line.split("|")[1].split()
        winning_numbers = line.split("|")[0].split(":")[1].split()
        card_deck.append([card_numbers, winning_numbers, 1])
    return card_deck

def process_deck(deck):
    number_of_cards = 0
    i = 0
    while i < len(deck):
        card_numbers = deck[i][0]
        winning_numbers = deck[i][1]
        card_copies = deck[i][2]
        win_count = sum(card_number in winning_numbers for card_number in card_numbers)
        number_of_cards += card_copies
        if win_count > 0:
            for j in range(1, win_count + 1):
                if i + j < len(deck):
                    deck[i + j][2] += card_copies
        i += 1
    return number_of_cards

def main():
    test_1_result = get_card_points(loadfile("test.txt"))
    if test_1_result != TEST_1_EXPECTED:
        print(Fore.RED + "Test 1 failed!" + Fore.RESET)
        print("Expected: " + str(TEST_1_EXPECTED))
        print("Got: " + str(test_1_result))
        return
    else:
        print(Fore.GREEN + "Test 1 passed!" + Fore.RESET)
        print("Part 1 result: " + str(get_card_points(loadfile("input.txt"))))
    
    test_2_result = process_deck(generate_deck(loadfile("test.txt")))
    if test_2_result != TEST_2_EXPECTED:
        print(Fore.RED + "Test 2 failed!" + Fore.RESET)
        print("Expected: " + str(TEST_2_EXPECTED))
        print("Got: " + str(test_2_result))
        return
    else:
        print(Fore.GREEN + "Test 2 passed!" + Fore.RESET)
        print("Part 2 result: " + str(process_deck(generate_deck(loadfile("input.txt")))))

main()
