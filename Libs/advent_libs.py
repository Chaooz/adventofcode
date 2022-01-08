#
# Library for Advent of Code solutions
# https://adventofcode.com/
#

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

def print_list(text, list):
    print ("--- " + text + " ---")
    
    print(str(list))
    #for line in list:
    #    print(line)
    print ("")

def pad_number(number,pad):
    num_str = str(number)
    l = len(pad)
    l2 = l - len(num_str)
    if ( l2 > 0 ):
        for i in range(l2):
            num_str = pad[0] + num_str
    return num_str

def unittest( func, expected, filename ):
    code_result = func(filename)
    if code_result == expected:
        print_ok("Unittest " + func.__name__ + " with " + str(code_result) + " is OK! input:" + filename)
    else:
        print_error("Unittest " + func.__name__ + " with " + str(code_result) + " is NOT OK! Got:" + str(code_result) + " Expected:" + str(expected) + " input:" + filename)

def unittest_input( func, input, expected, filename ):
    code_result = func(filename, input)
    if code_result == expected:
        print_ok("Unittest " + func.__name__ + "(" + str(input) + ") with " + str(code_result) + " is OK! input:" + filename)
    else:
        print_error("Unittest " + func.__name__ + "(" + str(input) + ") with " + str(code_result) + " is NOT OK! Got:" + str(code_result) + " Expected:" + str(expected) + " input:" + filename)

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

