from os import path
import sys
sys.path.insert(1, '../Libs')
from advent_libs import *

def create_empty_matrix(size_x,size_y, value = 0):
    matrix = [[value for col in range(size_y)] for row in range(size_x)]
    return matrix

def create_empty_matrix2(size):
    matrix = [[0 for col in range(size[0])] for row in range(size[1])]
    return matrix

def get_matrix_size(matrix):
    size_x = int(len(matrix))
    size_y = int(len(matrix[0]))
    return (size_x,size_y)

def create_matrix_from_file(textfile):
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

def matrix_to_list(matrix):
    out_list = list()
    size = get_matrix_size(matrix)
    for y in range(size[0]):
        for x in range(size[1]):
            out_list.append( (x,y ))
    return out_list

def matrix_plot_list(matrix,path_list):
    for (xx,yy,value) in path_list:
        matrix[xx][yy] = value

def is_in_matrix(matrix, position):
    if ( position[0] < 0 or position[1] < 0 ):
        return False    
    size = get_matrix_size(matrix)
    if (position[0] >= size[0] or position[1] >= size[1] ):
        return False
    return True

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

def print_matrix(text,matrix):
    print_matrix_color_padded(text,matrix,"",bcolors.RESET,"")

def print_matrix_color(text,matrix,value_highlight,color, pad = "00", space = " "):
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
