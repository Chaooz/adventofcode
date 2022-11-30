def loadfile(filename):
    file = open(filename)
    lines = file.readlines()
    file.close()
    return lines

def creatematrix(maxX, maxY):
    x = maxX
    y = maxY
    matrix = [0] * x
    for p in range (x):
        matrix[p] = [0] * y
    return matrix


def getMaxX(lines):
    ret = 0
    for segment in lines:
        if ( int(segment[0]) > ret ):
            ret = int(segment[0])
        elif (int(segment[2]) > ret ):
            ret = int(segment[2])
    return ret

def getMaxY(lines):
    ret = 0
    for segment in lines:
        if ( int(segment[1]) > ret ):
            ret = int(segment[1])
        elif (int(segment[3]) > ret ):
            ret = int(segment[3])
    return ret

lines = loadfile("line_segments.txt")

vent_field = creatematrix(999, 999)

coordinate_list = list()

for segment in lines:
    segment = segment.replace(" -> ", ",")
    segment = segment.strip("\n")
    segment = segment.split(",")
    coordinate_tuple = tuple(segment)
    coordinate_list.append(coordinate_tuple)

# Get max range
maxX = getMaxX(coordinate_list)
maxY = getMaxY(coordinate_list)

print ("range = " + str(maxX) + " x " + str(maxY) )


for segment in coordinate_list:
    segx0 = int(segment[0])
    segy0 = int(segment[1])
    segx1 = int(segment[2])
    segy1 = int(segment[3])

    if segment[0] == segment[2]:
        
        minY = segy0
        maxY = segy1
        if minY > maxY:
            maxY = segy0
            minY = segy1

        for y in range(minY, maxY +1):
            cell = vent_field[segx0][y]
            cell = int(cell) + 1
            vent_field[segx0][y] = str(cell)
    
    elif segment[1] == segment[3]:

        minX = segx0
        maxX = segx1
        if minX > maxX:
            maxX = segx0
            minX = segx1

        for x in range(minX, maxX +1):
            cell = vent_field[x][segy0]
            cell = int(cell) + 1
            vent_field[x][segy0] = str(cell)
    
    else:

        minX = segx0
        maxX = segx1
        minY = segy0
        maxY = segy1
        if minX > maxX:
            maxX = segx0
            minX = segx1
            maxY = segy0
            minY = segy1

        y_vector = -1
        if minY < maxY:
            y_vector = 1

        num_steps = 0
        for x in range(minX,maxX +1):
            cell = vent_field[x][minY + num_steps]
            cell = int(cell) +1
            vent_field[x][minY+num_steps] = str(cell)
            num_steps += y_vector
    
number_of_overlaps = 0

for x in range(999):
    for y in range(999):
        cell = vent_field[x][y]
        if int(cell) > 1:
            number_of_overlaps += 1

print("Number of overlaps: " + str(number_of_overlaps))