def loadfile(filename):
    file = open(filename)
    lines = file.readlines()
    file.close()
    return lines

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

def findMatrixBoundries(matrix):
    

def findLowpoints(matrix):
    for 