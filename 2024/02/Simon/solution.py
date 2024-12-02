#!/usr/lib/python3

import sys
sys.path.insert(1, '../../../Libs')
from advent_libs import loadfile

def convert_to_ints(line):
    if isinstance(line,list):
        return line
    else:
        line = line.split(" ")
        int_line = []
        for number in line:
            int_line.append(int(number))
        return int_line

def is_safe(line):
    int_line = convert_to_ints(line)
    if int_line == sorted(int_line) or int_line == sorted(int_line, reverse=True):
        current_number = 0
        next_number = 0
        for i in range(len(int_line) - 1):
            current_number = int_line[i]
            next_number = int_line[i + 1]
            line_is_safe = True
            if abs(current_number - next_number) > 3 or abs(current_number - next_number) == 0:
                line_is_safe = False
                break
            else:
                continue
        return bool(line_is_safe)

def is_safe_with_dampener(line):
    int_line = convert_to_ints(line)

    for i in range(0,len(int_line)):
        modded_line = int_line[:i] + int_line[i+1:]
        #print("mod",modded_line)
        if is_safe(modded_line):
            return True
    return False

lines = loadfile("input.txt")

safe_lines = 0
safe_lines_with_dampener = 0

for line in lines:
    if is_safe(line):
        safe_lines += 1
    else:
        #print("samp",line)
        if is_safe_with_dampener(line):
            safe_lines_with_dampener += 1

safe_lines_with_dampener = safe_lines + safe_lines_with_dampener

# Print the number of safe lines
print(str(safe_lines) + " lines are safe without using the problem dampener.")
print(str(safe_lines_with_dampener) + " lines are safe if the problem dampener is used.")
