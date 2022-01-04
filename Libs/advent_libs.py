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

def create_empty_matrix(size_x,size_y):
    matrix = [[0 for col in range(size_y)] for row in range(size_x)]
    return matrix

def create_empty_matrix2(size):
    matrix = [[0 for col in range(size[0])] for row in range(size[1])]
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

def compress_matrix(matrix, rate):
    size = get_matrix_size(matrix)
    size_x = int(size[0])
    size_y = int(size[1])

    compressed_size_x = int(size_x / rate)
    compressed_size_y = int(size_y / rate)

    #print("Compress matrix " + str(size_x) + "x" + str(size_y) + " => " + str(compressed_size_x) + "x" + str(compressed_size_y))
    compressed_matrix = create_empty_matrix(compressed_size_x, compressed_size_y)

    for y in range(size_y):
        for x in range(size_x):
            xx = int(x/rate)
            yy = int(y/rate)

            val = matrix[x][y]
            compressed_matrix[xx][yy] = compressed_matrix[xx][yy] + val

    return compressed_matrix

def matrix_cut(matrix,start_x, start_y, end_x, end_y):

    print("matrix cut:" + str(start_x) + "x" + str(start_y) + " => " + str(end_x) + "x" + str(end_y))

    cut_matrix = create_empty_matrix( end_x - start_x, end_y - start_y)

    xx = 0
    yy = 0
    for y in range(start_y, end_y):
        for x in range( start_x, end_x):
            cut_matrix[xx][yy] = matrix[x][y]
            xx = xx + 1
        v = cut_matrix[0][yy]
        v2 = matrix[0][yy]
        #print(str(yy) + " => " + str(v) + " : " + str(v2))

        xx = 0
        yy = yy + 1

    return cut_matrix

def matrix_splice_x(matrix1, matrix2):
    size1 = get_matrix_size(matrix1)
    size2 = get_matrix_size(matrix2)
    size_x = size1[0] + size2[0]
    size_y = size1[1]

    spliced_matrix = create_empty_matrix( size_x, size_y )

    for y in range(size1[1]):
        for x in range(size1[0]):
            spliced_matrix[x][y] = matrix1[x][y]

    for y in range(size2[1]):
        for x in range(size2[0]):
            spliced_matrix[ size1[0] + x][y] = matrix2[x][y]

    return spliced_matrix

def matrix_copy(matrix):

    size = get_matrix_size(matrix)
    matrix_copy = create_empty_matrix( size[0], size[1] )

    for y in range(size[1]):
        for x in range(size[0]):
            matrix_copy[x][y] = matrix[x][y]

    return matrix_copy


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

def print_matrix(text,matrix):
    size = get_matrix_size(matrix)

    size_x = size[0]
    size_y = size[1]

    print ("--- " + text + " " + str(size_x) + "x" + str(size_y) + " ---")
    for y in range(size_y):
        line = ""
        for x in range(size_x):
            value = matrix[x][y]
            if ( value < 10 ):
                line = line + "0"
            line = line + str(value) + " "
        print(line)
    print ("" + bcolors.RESET)

def print_matrix_color(text,matrix,value_highlight,color):
    print_matrix_color_padded(text,matrix,value_highlight,color,"00")

def print_matrix_color_padded(text,matrix,value_highlight,color, pad, space = " "):
    size = get_matrix_size(matrix)

    size_x = size[0]
    size_y = size[1]
    pad_size = len(pad)
    pady_size = len(str(size_y-1))

    print ("      --- " + text + " " + str(size_x) + "x" + str(size_y)  + " ---")
    print("")

    header  = bcolors.DARK_GREY
    header2 = bcolors.DARK_GREY

    for i in range(pady_size):
        header = header + " " 
        header2 = header2 + " "

    header = header + " + "
    header2 = header2 + "   "

    for x in range(size_x):
        xx = x % 10

        header2 += pad_number( xx , pad )
        for i in range(pad_size):
            header = header + "-"
        header2 = header2 + space
        header = header + space

    print(header2)
    print(header)

    pady = ""
    for i in range(pady_size):
        pady += "0"

    for y in range(size_y):
        line = ""
        line = line + bcolors.BOLD + color
        line = line + pad_number(y,pady)
        line = line + bcolors.DARK_GREY
        line = line + " | "

        for x in range(size_x):
            value = matrix[x][y]
            if ( value == value_highlight):
                line = line + bcolors.BOLD + color
            else:
                line = line + bcolors.RESET

            line += pad_number( value , pad )
            line += space
        print(line)
    print ("" + bcolors.RESET)

def unittest( func, expected, filename ):
    code_result = func(filename)
    if code_result == expected:
        print_ok("Unittest " + filename + " with " + str(code_result) + " is OK! ")
    else:
        print_error("Unittest " + filename + " with " + str(code_result) + " is NOT OK! Got:" + str(code_result) + " Expected:" + str(expected))

def unittest_input( func, input, expected, filename ):
    code_result = func(filename, input)
    if code_result == expected:
        print_ok("Unittest " + func.__name__ + "(" + str(input) + ") with " + str(code_result) + " is OK! file:" + filename)
    else:
        print_error("Unittest " + func.__name__ + "(" + str(input) + ") with " + str(code_result) + " is NOT OK! Got:" + str(code_result) + " Expected:" + str(expected) + " file:" + filename)


def print_error(text):
    print(bcolors.WARNING + "[ERROR]   " + text + bcolors.RESET)

def print_warning(text):
    print(bcolors.WARNING + "[WARNING] " + text + bcolors.RESET)

def print_ok(text):
    print(bcolors.OKGREEN + "[OK]      " + text + bcolors.RESET)
