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
    x = len(matrix)
    y = len(matrix[0])
    ret = (x,y)
    return ret

def findRisk(matrix):
    boundries = findMatrixBoundries(matrix)
    lowpoints = 0

    for x in range(boundries[0]):
        for y in range(boundries[1]):
            cell = matrix[x][y]
            
            if y-1 < 0:
                over_cell = 11
            else:
                over_cell = matrix[x][y-1]

            if y+2 > boundries[1]:
                under_cell = 11
            else:
                under_cell = matrix[x][y+1]

            if x-1 < 0:
                left_cell = 11
            else:
                left_cell = matrix[x-1][y]

            if x+2 > boundries[0]:
                right_cell = 11
            else:
                right_cell = matrix[x+1][y]

            if cell < over_cell and cell < under_cell and cell < left_cell and cell < right_cell:
                lowpoints += cell + 1

    return lowpoints

heightmap = createMatrix("height_map.txt")
risk_score = findRisk(heightmap)

print("The risk score is " + str(risk_score))