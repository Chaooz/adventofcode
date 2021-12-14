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

def findLowpoints(matrix):
    boundries = findMatrixBoundries(matrix)
    lowpoints = list()

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
                lowpoint = (x,y)
                lowpoints.append(lowpoint)

    return lowpoints

def can_move_to_checkpoint(matrix, x, y, boundries, checked_cells):
    cell = 0
    if y >= 0 and x >= 0 and x < boundries[0] and y < boundries[1] : 
        cell = matrix[x][y]
        if cell < 9:

            # Did we already visit this cell ?
            for visited in checked_cells:
                if ( visited[0] == x and visited[1] == y ):
                    return 0

            # Virgin cell
            checked_cells.append((x,y))

            size = 1
            # print(str(x) + " " + str(y) + " " + str(len(checked_cells)))
            size += can_move_to_checkpoint( matrix, x, y - 1, boundries, checked_cells)
            size += can_move_to_checkpoint( matrix, x, y + 1, boundries, checked_cells)
            size += can_move_to_checkpoint( matrix, x - 1, y, boundries, checked_cells)
            size += can_move_to_checkpoint( matrix, x + 1, y, boundries, checked_cells)

            return size
        
    return 0

def basinsize(matrix,lowpoint):
    size = 1
    x = lowpoint[0]
    y = lowpoint[1]
    boundries = findMatrixBoundries(matrix)
    checked_cells = list()

    cell = matrix[x][y]

    size = can_move_to_checkpoint( matrix, x, y, boundries, checked_cells)
    
    return size

heightmap = createMatrix("height_map.txt")
lowpoints = findLowpoints(heightmap)

top1 = 0
top2 = 0
top3 = 0

for lowpoint in lowpoints:
    size = basinsize(heightmap,lowpoint)
    #print(str(size))

    if size > top1:
        top3 = top2
        top2 = top1
        top1 = size
    elif size > top2:
        top3 = top2
        top2 = size
    elif size > top3:
        top3 = size

solution = top3 * top2 * top1

print("Solution is " + str(solution))