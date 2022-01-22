#!/usr/bin/python3
#
# Day 18 Snailfish : https://adventofcode.com/2021/day/18
# 

from dis import show_code
from re import A
import sys
import time
import ast
import math
from tkinter.tix import Tree
sys.path.insert(1, '../Libs')
from advent_libs import *
from advent_libs_matrix import *

# Depricated
def parse_line(line, i, level):
    number_list = list()
    startPos = -1
    txt = ""

    spacer = ""
    for n in range(0,level):
        spacer += "-"

    print(spacer + " parse-level:" + str(level) + " i:" + str(i))
    while i < len(line):
        startChar = line[i]
        i += 1
        if startChar == "[":
            i, sub_list = parse_line(line,i,level + 1)
            number_list.append(sub_list)
            print("char:[  = " + str(sub_list))
        elif startChar == "]":
            print("char:]  = " + txt)
            number_list.append(txt)
            break
        elif startChar == ",":
            print("char:,  = " + txt)
            if len(txt) > 0:
                number_list.append(txt)
            txt = ""
        else:
            txt += startChar

    return i, number_list

# If a level 4 occurs ( 4 [[[[ ) ..fex [[[[0,1 then
# left number (0) is added to parent left number
# right number (1) is added to parent right number
# exploded number becomes 0

global left_number
global right_number
global trigger_explode
global debug

def explode_tree( tree_list, level ):
    global left_number
    global right_number
    global trigger_explode
    global debug

    if level == 0:
        debug = None

    left = -1
    right = -1

    i = 0
    b = False
    for number in tree_list:
        replace_index = 1-i
        if isinstance(number,list):
            number, left, right, remove_child = explode_tree(number,level + 1)

            #if left_number > - 1:
            #    print("subexplode left3:" + str(left_number) + ":" + str(tree_list[replace_index]))

            #if right_number > - 1:
            #    print("subexplode right3:" + str(right_number) + ":" + str(tree_list[replace_index]))

            # if left of explode needs replacement. Do so
            key_left = tree_list[0]
            key_right = tree_list[1]
            if left > -1 and isinstance(key_left,int):
                print("subexplode left-up:" + str(key_left) + " + " + str(left_number) + " = " + str(key_left+left_number))
                tree_list[0] += left_number
                left_number = -1
                left = -1
            elif right > -1 and isinstance(key_right,int):
                print("subexplode right-up:" + str(key_right) + " + " + str(right_number) + " = " + str(key_right+right_number))
                tree_list[1] += right_number
                right_number = -1
                right = -1

            if remove_child:
                tree_list[i] = 0
                b = True

        elif level > 3 and trigger_explode:
            if isinstance(tree_list[replace_index],int):
                left_number = tree_list[0]
                right_number = tree_list[1]
                trigger_explode = False
                print("Explode keypair: [" + str(left_number) + "," + str(right_number) + "]")
                debug = tree_list
                return tree_list, left_number, right_number, True
        elif b == False:
            if right_number > -1 :
                tree_list[i] = number + right_number
                print("subexplode right-down:" + str(number) + " + " + str(right_number) + " = " + str(number+right_number))
                right_number = -1
            elif left_number > -1 :
                tree_list[i] = number + left_number
                print("subexplode left-down:" + str(number) + " + " + str(left_number) + " = " + str(number+left_number))
                left_number = -1

        i += 1

    return tree_list, left, right, False

def split_tree( tree_list, did_split ):
    i = 0
    for number in tree_list:
        if isinstance(number,list):
            a, did_split = split_tree(number,did_split)
        elif number >= 10 and not did_split:
            a = math.floor(number/2)
            b = math.ceil(number/2)
            number = list()
            number.append(a)
            number.append(b)
            tree_list[i] = number
            did_split = True
        i += 1

    return tree_list, did_split

def run_explode_input( input ):

    global left_number
    global right_number
    global trigger_explode

    left_number = -1
    right_number = -1
    trigger_explode = True

    tree = ast.literal_eval(input)
#    print_tree_list("",tree)
    new_tree, remove, l,r = explode_tree(tree,0)
    tree_str = str(new_tree)
    tree_str = tree_str.replace(" ", "")

    if left_number > -1:
        print("could ot replace left?" + str(left_number))

    return tree_str

def run_explode_input_full( input ):
    while(True):
        result = run_explode_input(input)
        if result == input:
            return result
        print("After explode:" + str(result))
        input = result
    return input

def add_numbers( number1, number2 ):
    result = "[" + number1 + "," + number2 + "]"
    print("-------------------------------------------------------------------")
    print("  " + str(number1))
    print("+ " + str(number2))
    print("= " + str(result))
    print("-------------------------------------------------------------------")
    return result

def run_add_numbers(input, parameters):
    number1,number2 = parameters
    return add_numbers(number1,number2)

def run_split_input(input):
    tree = ast.literal_eval(input)
    tree,b = split_tree(tree, False)
#    print(str(tree))

    tree_str = str(tree)
    tree_str = tree_str.replace(" ", "")
    return tree_str

def sum_tree_list( number_list ):
    total = 0
    i = 3
    for number in number_list:
        if isinstance(number,list):
            number = sum_tree_list(number)
        total += number * i
        i -= 1
    return total

def run_sum_input(input):
    tree = ast.literal_eval(input)
#    print_tree_list("",tree)
    return sum_tree_list(tree)

#def run_sum_lines(filename):
#    data = loadfile(filename)
#    for line in data:
#        do_calc(line)

def run_full_calc(input):

    #input = run_add_numbers(input, parameters)

    while( True ):
        a = input

        exit_loop = False
        while(not exit_loop):
            result = run_explode_input(input)
            txt = input
            if not debug is None:
                highlight = str(debug)
                highlight = highlight.replace(" ", "")
                txt = string_highlight(input,highlight, bcolors.WARNING)
            print("run_explode_input:" + str(txt) + " => " + str(result))

            if input == result:
                exit_loop = True
            input = result

        exit_loop = False
        while(not exit_loop):
            result = run_split_input(input)
            print("run_split_input:" + str(input) + " => " + str(result))
            if input == result:
                exit_loop = True
            input = result

        if a == input:
            break

    return input

def run_sum_from_file(filename):
    lines = loadfile(filename)
    line = lines[0].replace("\n","")
    for i in range(1,len(lines)):
        line2 = lines[i].replace("\n","")
        line = add_numbers( line, line2 )
        result = run_full_calc(line) 
        v = str(result)
        print(v)
        break
       
    return result

# Basic calc unittests
unittest(run_sum_input,29,"[9,1]")
unittest(run_sum_input,21,"[1,9]")
unittest(run_sum_input, 143, "[[1,2],[[3,4],5]]")
unittest(run_sum_input, 1384, "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")
unittest(run_sum_input, 445, "[[[[1,1],[2,2]],[3,3]],[4,4]]")
unittest(run_sum_input, 791, "[[[[3,0],[5,3]],[4,4]],[5,5]]")
unittest(run_sum_input, 1137, "[[[[5,0],[7,4]],[5,5]],[6,6]]")
unittest(run_sum_input, 3488, "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")

unittest(run_explode_input, "[[[[0,9],2],3],4]", "[[[[[9,8],1],2],3],4]")
unittest(run_explode_input, "[7,[6,[5,[7,0]]]]", "[7,[6,[5,[4,[3,2]]]]]")
unittest(run_explode_input, "[[6,[5,[7,0]]],3]", "[[6,[5,[4,[3,2]]]],1]")
unittest(run_explode_input, "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")
unittest(run_explode_input, "[[3,[2,[8,0]]],[9,[5,[7,0]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
unittest(run_explode_input, "[[[[0,7],4],[7,[[8,4],9]]],[1,1]]", "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")
unittest(run_explode_input, "[[[[0,7],4],[15,[0,13]]],[1,1]]", "[[[[0,7],4],[7,[[8,4],9]]],[1,1]]")

unittest(run_split_input, "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]", "[[[[0,7],4],[15,[0,13]]],[1,1]]")
unittest(run_split_input, "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]", "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]")

#unittest_input(run_add_numbers, ("[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]"), "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]", "")
#unittest(run_full_calc, "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")


unittest(run_sum_from_file, "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]", "unittest2_day18_data.txt")
#unittest(run_sum_from_file, "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]", "unit1.txt")

