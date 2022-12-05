
import sys
from advent_libs import *

def listToString(s):
    str1 = ""
    for ele in s:
        if str1 == "":
            str1 += "["
        else:
            str1 += ","
        str1 += str(ele)
    str1 += "]"
    return str1

#
# Create a list of tuples from the textfile
#
def listFromFile(textfile, delimiter):
    file_lines = loadfile(textfile)
    my_list = list()
    for line in file_lines:
        line = line.strip()
        key_value = line.split(delimiter)        
        my_list.append(key_value)
    return my_list

def min_point_in_list(point_list):
    min_x = 0
    min_y = 0
    for input in point_list:
        x = int(input[0])
        y = int(input[1])
        if x < min_x:
            min_x = x
        if y < min_y:
            min_y = y
    return (min_x, min_y)

# Get the max x and y in a list (used to create matrix)
def max_point_in_list(point_list):
    max_x = 0
    max_y = 0
    for input in point_list:
        x = int(input[0])
        y = int(input[1])
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
    return (max_x, max_y)

def list_offset_points(list, x,y):
    newList = []
    for point in list:
        newList.append( (point[0] + x, point[1] + y) )
    return newList

def print_list(text, list):
    print ("--- " + text + " ---")
    
    print(str(list))
    #for line in list:
    #    print(line)
    print ("")
