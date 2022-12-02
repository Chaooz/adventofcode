#
# Library for Advent of Code solutions
# https://adventofcode.com/
#
import time

class bcolors:
    RESET = '\033[39m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DARK_GREY = '\033[1;30;40m'


def loadfile(filename):
    file = open(filename)
    lines = file.readlines()
    file.close()
    return lines

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
        line = line.strip("\n")
        key_value = line.split(delimiter)        
        my_list.append(key_value)
    return my_list

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

def point_to_str(text,point):
    return text + str(point[0]) + "x" + str(point[1])

def string_highlight(string,highlight, color):
    new_text = color + highlight + bcolors.RESET
    return string.replace(highlight, new_text,1)

def print_list(text, list):
    print ("--- " + text + " ---")
    
    print(str(list))
    #for line in list:
    #    print(line)
    print ("")

def print_tree_list(spacer, tree_list : list):
    for line in tree_list:
        if isinstance(line,list):
#            print("Tree1:" + spacer + str(line))
            print("Tree1:" + spacer + "T")
            if spacer =="":
                spacer = "+"
            print_tree_list( spacer + "-", line)
        elif isinstance(line,str):
            print("Tree2:" + spacer + " " + line)
        else:
            print("Tree3:" + spacer + " " + str(line))
#    print ("")

def pad_number(number,pad):
    num_str = str(number)
    l = len(pad)
    l2 = l - len(num_str)
    if ( l2 > 0 ):
        for i in range(l2):
            num_str = pad[0] + num_str
    return num_str

def unittest( func, expected, filename ):
    st = time.time()
    code_result = func(filename)
    et = time.time()
    strTime = " (execution time:" + str(round(et-st,2)) + ")"

    if code_result == expected:
        print_ok("Unittest " + func.__name__ + " with " + str(code_result) + " is OK! input:" + str(filename) + strTime)
    else:
        print_error("Unittest " + func.__name__ + " with " + str(code_result) + " is NOT OK! Got:" + str(code_result) + " Expected:" + str(expected) + " input:" + str(filename) + strTime)

def unittest_list( func, expected, filename ):
    st = time.time()
    code_result = func(filename)
    et = time.time()
    strTime = " (execution time:" + str(round(et-st,2)) + ")"

    s_result = listToString(code_result)
    s_input = listToString(filename)
    if code_result == expected:
        print_ok("Unittest " + func.__name__ + " with " + str(s_result) + " is OK! input:" + s_input + strTime)
    else:
        print_error("Unittest " + func.__name__ + " with " + str(s_result) + " is NOT OK! Got:" + str(s_result) + " Expected:" + str(expected) + " input:" + s_input + strTime)



def unittest_input( func, input, expected, filename ):

    st = time.time()
    code_result = func(filename, input)
    et = time.time()
    strTime = " (execution time:" + str(round(et-st,2)) + ")"

    if code_result == expected:
        print_ok("Unittest " + func.__name__ + "(" + str(input) + ") with " + str(code_result) + " is OK! input:" + filename + strTime)
    else:
        print_error("Unittest " + func.__name__ + "(" + str(input) + ") with " + str(code_result) + " is NOT OK! Got:" + str(code_result) + " Expected:" + str(expected) + " input:" + filename + strTime)

def print_assert(value,text):
    if not value:
        print(bcolors.FAIL + "[ASSERT]  " + text + bcolors.RESET)
        assert False

def print_error(text):
    print(bcolors.WARNING + "[ERROR]   " + text + bcolors.RESET)

def print_warning(text):
    print(bcolors.WARNING + "[WARNING] " + text + bcolors.RESET)

def print_ok(text):
    print(bcolors.OKGREEN + "[OK]      " + text + bcolors.RESET)

def print_debug(text):
    print(text)
    pass

