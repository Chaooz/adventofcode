from os import path
import sys
sys.path.insert(1, '../Libs')
from advent_libs import *


def matrix_to_list(matrix):
    out_list = list()
    size = get_matrix_size(matrix)
    for y in range(size[0]):
        for x in range(size[1]):
            out_list.append( (x,y ))
    return out_list

def is_in_matrix(matrix, position):
    if ( position[0] < 0 or position[1] < 0 ):
        return False    
    size = get_matrix_size(matrix)
    if (position[0] >= size[0] or position[1] >= size[1] ):
        return False
    return True
