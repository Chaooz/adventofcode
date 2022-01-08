#
# Day 14 Polymorization : https://adventofcode.com/2021/day/14
# 

import sys
import time
sys.path.insert(1, '../Libs')
from advent_libs import *
from collections import Counter

def decode_data(line_list):

    formula = str()
    code_list = list()
    read_formula = True

    for line in line_list:
        line = line.strip()

        if line == "":
            pass
        elif read_formula:
            read_formula = False
            formula = line
        else:
            key_value = line.split(" -> ")
            code_list.append(key_value)

    result = list()
    result.append(formula)
    result.append(code_list)
    return result

def get_code(code_list, key):
    for code in code_list:
        if code[0] == key:
            return code[1] 
    return "##" + key + "##"

def list_to_string(list):
    s = str()
    return s.join(list)

def get_unique_string(string):
    out_string = str()
    for char in string:
        if out_string.find(char) == -1:
            out_string = out_string + char

    return out_string

def count_letters(formula, out_string):
    count_list = list()
    for char in formula:
        count = 0
        for c2 in out_string:
            if char == c2:
                count = count + 1
        count_list.append( (char,count))

    return count_list

def run_fast_formula(start_string, code_list, max_loops):
    old_values = Counter()
    inserts = Counter()

    # Original string
    for char in start_string:
        inserts[char] += 1 

    # Generate startlist of a+b keys
    for i in range(1,len(start_string)):
        a = start_string[i - 1]
        b = start_string[i]
        key = a+b
        code = get_code(code_list, key )
        old_values[key] += 1

    # increase counter for a+code and code+b keys
    for _ in range(max_loops):
        new_values = Counter()
        for (a,b), value in old_values.items():
            code = get_code(code_list, a+b )
            #print("a:" + a + ", b:" + b + " c:" + code + " = " + str(value))
            new_values[a+code] += value
            new_values[code+b] += value
            inserts[code] += value
        old_values = new_values
    
    # Return max-min
    return max(inserts.values()) - min(inserts.values())



def run_formula(start_string, code_list, loops, max_loops):

    if loops >= max_loops:
        return start_string

    l = len(start_string)
    size = int(l * 2) - 1

    #print(" len:" + str(l) + " => " + str(size) + " loop:" + str(loops))

    ta = time.perf_counter()
    new_string = ["" for x in range(size)]
    new_string[0] = start_string[0]

    j = int(1)
    for i in range(1,len(start_string)):
        a = start_string[i-1]
        b = start_string[i]
        ab = a+b
        
        code = get_code( code_list, ab)
        new_string[j] = code
        new_string[j+1] = b
        j = j + 2

    #ss = list_to_string(new_string)
    tb = time.perf_counter()
    #print(f"{ta - tb:0.4f}")

    return run_formula(new_string, code_list, loops + 1, max_loops )

def run_polymarization(filename, max_loops):
    file_data = loadfile(filename)
    decoded_data = decode_data(file_data)
    end_string = run_formula(decoded_data[0], decoded_data[1], 0, max_loops)
    #print(end_string)

    s = ""
    s = s.join(end_string)

    return str(s)

def run_polymarization_result(filename, max_loop):
    file_data = loadfile(filename)
    decoded_data = decode_data(file_data)
    end_string = run_formula(decoded_data[0], decoded_data[1], 0, max_loop)
    unique_string = get_unique_string(end_string)
    formula_list = count_letters(unique_string, end_string)

    max_count = 0
    min_count = 99999

    for entry in formula_list:
        if min_count > entry[1]:
            min_count = entry[1]
        if max_count < entry[1]:
            max_count = entry[1]

    return int(max_count - min_count)

def run_fast_polymariazation_result(filename, max_loop):
    file_data = loadfile(filename)
    decoded_data = decode_data(file_data)
    result = run_fast_formula(decoded_data[0], decoded_data[1], max_loop)
    return result


# Unittest : Check charachter returns
unittest_input(run_polymarization, 1, "NCNBCHB","polymarization_data_example.txt")
unittest_input(run_polymarization, 2, "NBCCNBBBCBHCB","polymarization_data_example.txt")
unittest_input(run_polymarization, 3, "NBBBCNCCNBBNBNBBCHBHHBCHB","polymarization_data_example.txt")
unittest_input(run_polymarization, 4, "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB","polymarization_data_example.txt")

# Unittest: Test the actual result program wants
unittest_input(run_polymarization_result,1, 1,"polymarization_data_example.txt")
unittest_input(run_polymarization_result,5, 33,"polymarization_data_example.txt")
unittest_input(run_polymarization_result,10, 1588,"polymarization_data_example.txt")
# 40 in slow mode takes too long
#unittest(run_result_fourty,2188189693529,"polymarization_data_example.txt")

# Unittest : Test the fast way to do result
unittest_input(run_fast_polymariazation_result,1, 1,"polymarization_data_example.txt")
unittest_input(run_fast_polymariazation_result,5, 33,"polymarization_data_example.txt")
unittest_input(run_fast_polymariazation_result,10, 1588,"polymarization_data_example.txt")
unittest_input(run_fast_polymariazation_result,40, 2188189693529,"polymarization_data_example.txt")

# Run the actual program
unittest_input(run_fast_polymariazation_result,40, 3528317079545,"polymarization_data.txt")
