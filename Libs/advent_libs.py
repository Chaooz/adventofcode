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

def createMatrix(textfile):
    file_lines = loadfile(textfile)
    matrix = list()
    for line in file_lines:
        row_list = list()
        line.strip("\n")
        for char in line:
            if not char == "\n":
                row_list.append(int(char))
        matrix.append(row_list)
    return matrix

def print_list(text, list):
    print ("--- " + text + " ---")
    print(str(list))
    #for line in list:
    #    print(line)
    print ("")


def print_matrix(text,size_x,size_y,matrix):
    print ("--- " + text + " ---")
    for x in range(size_x):
        line = ""
        for y in range(size_y):
            value = matrix[x][y]
            if ( value == 0):
                line = line + bcolors.BOLD + bcolors.WARNING
            else:
                line = line + bcolors.RESET

            if ( value < 10 ):
                line = line + "0"
            line = line + str(value) + " "
        print(line)
    print ("")

def unittest( func, expected, filename ):
    code_result = func(filename)
    if code_result == expected:
        print(bcolors.OKGREEN + "[OK]    Unittest " + filename + " with " + str(code_result) + " steps is OK! " + bcolors.RESET)
    else:
        print(bcolors.WARNING + "[ERROR] Unittest " + filename + " with " + str(code_result) + " steps is NOT OK! Got:" + str(code_result) + " Expected:" + str(expected) + bcolors.RESET)
