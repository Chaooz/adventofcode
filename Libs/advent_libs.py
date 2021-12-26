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

def create_empty_matrix(size_x,size_y):
    matrix = [[0 for col in range(size_y)] for row in range(size_x)]
    return matrix

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

def get_matrix_size(matrix):
    size_x = int(len(matrix))
    size_y = int(len(matrix[0]))
    return (size_x,size_y)

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

def print_matrix(text,matrix):
    size = get_matrix_size(matrix)

    size_x = size[0]
    size_y = size[1]

    print ("--- " + text + " " + str(size_x) + "x" + str(size_y) + " ---")
    for y in range(size_y):
        line = ""
        for x in range(size_x):
            value = matrix[x][y]
            if ( value == 0):
                line = line + bcolors.BOLD + bcolors.WARNING
            else:
                line = line + bcolors.RESET

            if ( value < 10 ):
                line = line + "0"
            line = line + str(value) + " "
        print(line)
    print ("" + bcolors.RESET)

def unittest( func, expected, filename ):
    code_result = func(filename)
    if code_result == expected:
        print(bcolors.OKGREEN + "[OK]    Unittest " + filename + " with " + str(code_result) + " steps is OK! " + bcolors.RESET)
    else:
        print(bcolors.WARNING + "[ERROR] Unittest " + filename + " with " + str(code_result) + " steps is NOT OK! Got:" + str(code_result) + " Expected:" + str(expected) + bcolors.RESET)
