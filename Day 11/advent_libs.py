#
# Library for Advent of Code solutions
# https://adventofcode.com/
#
def loadfile(filename):
    file = open(filename)
    lines = file.readlines()
    file.close()
    return lines
