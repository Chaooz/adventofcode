from os import path
import sys
sys.path.insert(1, '../Libs')
from advent_libs import *
from advent_libs_list import *
from advent_libs_vector2 import *

class Matrix:

    name:str
    sizeX:int
    sizeY:int

    # Replace with this
    width:int
    height:int

    def __init__(self, name:str, sizeX:int, sizeY:int, value) -> None:
        self.name = name
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.width = sizeX
        self.height = sizeY 
        if sizeX > 0 and sizeY > 0:
            self.data = [[value for col in range(sizeY)] for row in range(sizeX)]

    def InsertFromVector2List(self,vectorList:Vector2List, character:str = ""):
        for vector in vectorList:
            d = self.data[vector.x][vector.y]
            if ( isinstance(d,int)):
                self.data[vector.x][vector.y] += 1
            else:
                self.data[vector.x][vector.y] = character

    #
    # Create a new empty matrix with the same size
    #
    def EmptyCopy(self, newTitle:str, defaultValue = 0):
        newMatrix = Matrix(newTitle, self.sizeX, self.sizeY, defaultValue)
        return newMatrix

    def Duplicate(self, newTitle:str):
        newMatrix = Matrix(newTitle, self.sizeX, self.sizeY, "")
        for y in range(self.sizeY):
            for x in range(self.sizeX):
                newMatrix.data[x][y] = self.data[x][y]
        return newMatrix

    # If point is inside the matrix
    def IsInside(self,x,y) -> bool:
        return x >= 0 and x < self.sizeX and y >= 0 and y < self.sizeY

    def IsPointInside(self, point:Vector2 ) -> bool:
        return point.x >= 0 and point.x < self.sizeX and point.y >= 0 and point.y < self.sizeY

    def IsOutOfBounds(self, point:Vector2 ) -> bool:
        return self.IsPointInside(point) == False

    def Set(self,x, y, character ):
        if self.IsInside(x,y):
            self.data[x][y] = character
        else:
            print_error("Matrix.Set : " + str(x) + "x" + str(y) + " is outside of matrix")

    def SetPoint(self, point, character, exclude = None ):
        if self.IsPointInside(point):
            if exclude != None:
                if self.data[point.x][point.y] in exclude:
                    return
            self.data[point.x][point.y] = character
        else:
            print_error("Matrix.Set : " + point.ToString() + " is outside of matrix")

    def SetMatrix(self,matrix):
        for y in range(matrix.sizeY):
            for x in range(matrix.sizeX):
                self.data[x][y] = matrix.data[x][y]

    def Get(self, x, y):
        if self.IsInside(x,y):
            return self.data[x][y]
        print_warning("Matrix.Get : " + str(x) + "x" + str(y) + " is outsde of matrix")

    def GetPoint(self, point:Vector2):
        if self.IsPointInside(point):
            return self.data[point.x][point.y]
        print_warning("Matrix.GetPoint : " + point.ToString() + " is outsde of matrix")

    def Print(self,value_highlight:str = "", color = bcolors.DARK_GREY, pad = "", space = " "):
        # TODO:Move function here and depricateother function
        print_matrix_color(self.name, self.data,value_highlight,color, pad,space)

    def PrintWithColor(self,valueList, defaultColor = bcolors.DARK_GREY, pad = "00", space = " "):
        print_matrix_colorlist(self.name,self.data,valueList, bcolors.DARK_GREY, defaultColor, pad, space)

    def PrintMultiple(self,valueList, color, defaultColor = bcolors.DARK_GREY, pad = "00", space = " "):
        print_matrix_colorlist(self.name,self.data,valueList, color, defaultColor, pad, space)

    def CreateFromList(name:str,file_lines:list, defaultValue:str):
        sizeY = len(file_lines)
        sizeX = len(file_lines[0].strip())
        width = sizeX
        height = sizeY
        matrix = Matrix(name,sizeX, sizeY, defaultValue)

        for y in range(0,len(file_lines)):
            line = file_lines[y]
            line = line.strip()
            for x in range(len(line)):
                matrix.data[x][y] = line[x]
        return matrix

    def CreateFromFile(textfile:str, defaultValue:str = "."):
        file_lines = loadfile(textfile)
        return Matrix.CreateFromList(textfile, file_lines, defaultValue)

    def FindFirst(self, character:str) -> Vector2:
        for y in range(self.sizeY):
            for x in range(self.sizeX):
                if self.data[x][y] == character:
                    return Vector2(x,y)
        return None

    def FindFirst(self, listOfChars:list) -> Vector2:
        for y in range(self.sizeY):
            for x in range(self.sizeX):
                for character in listOfChars:
                    if self.data[x][y] == character:
                        return Vector2(x,y)
        return None

    def FindAll(self, character:str) -> list:
        pointList = list()
        for y in range(self.sizeY):
            for x in range(self.sizeX):
                if self.data[x][y] == character:
                    pointList.append(Vector2(x,y))
        return pointList

    # Count the number of occurances of a character
    def Count(self, character:str):
        sum = 0
        for y in range(self.sizeY):
            for x in range(self.sizeX):
                if self.data[x][y] == character:
                    sum += 1
        return sum

    def RotateLeft(self):
        newMatrix = Matrix(self.name, self.sizeY, self.sizeX, "." )
        for y in range(0, self.sizeY):
            for x in range(0, self.sizeX):
                newMatrix.Set(y, self.sizeX - x - 1, self.Get(x, y))
        self.SetMatrix(newMatrix)

    def RotateRight(self):
        newMatrix = Matrix(self.name, self.sizeY, self.sizeX, "." )
        for y in range(0, self.sizeY):
            for x in range(0, self.sizeX):
                newMatrix.Set(self.sizeY - y - 1, x, self.Get(x, y))
        self.SetMatrix(newMatrix)


    def Raytrace(self, start:Vector2, direction:Vector2, openSpace:str):
        position = start
        while True:
            if self.IsOutOfBounds(position):
                return None

            char = self.Get(position.x, position.y)
            if char != openSpace:
                return position
        
            position = position + direction

    def FillAreaOuterInternal(self, visit:list, position, wall:str, fill:str):

        path_list = list()
        path_list.append(position)

        while True:

            if len(path_list) == 0:
                return

            position = path_list.pop()

            if self.IsOutOfBounds(position):
                continue

            char = self.GetPoint(position)
            if char == wall:
                continue

            if char == fill:
                continue
            
            self.SetPoint(position, fill)

            path_list.append(position + Vector2(1,0))
            path_list.append(position + Vector2(-1,0))
            path_list.append(position + Vector2(0,1))
            path_list.append(position + Vector2(0,-1))


    def FillAreaOuter(self, position, wall:str, character:str):

        visited = list()
        size = self.sizeX
        for x in range(size):
            self.FillAreaOuterInternal(visited, Vector2(x,0), wall, character)
            self.FillAreaOuterInternal(visited, Vector2(x,size-1), wall, character)
            self.FillAreaOuterInternal(visited, Vector2(0,x), wall, character)
            self.FillAreaOuterInternal(visited, Vector2(size-1,x), wall, character)


    def FillArea(self, position:Vector2, openSpace:str, character:str):
        for y in range(self.sizeY):
            isInside = False
            lastIsWall = False
            for x in range(self.sizeX):
                char = self.data[x][y]
                if isInside == False and char == openSpace and lastIsWall == True:
                    # Check if we have a wall after this openSpace
                    if self.Raytrace(Vector2(x,y), Vector2(1,0), openSpace) != None:
                        isInside = True
                elif isInside == True and char == openSpace and lastIsWall == True:
                    isInside = False

                if isInside and char == openSpace:
                    self.data[x][y] = character

                lastIsWall = char != openSpace

    # Create a new Matrix with scaledown version
    def GetScaledMatrix(self, rate, defaultValue):

        compressed_size_x = int(self.sizeX / rate)
        compressed_size_y = int(self.sizeY / rate)

#        print("Compress matrix " + str(self.sizeX) + "x" + str(self.sizeY) + " => " + str(compressed_size_x) + "x" + str(compressed_size_y))
        compressed_matrix = Matrix(self.name, compressed_size_x, compressed_size_y, defaultValue)

        for y in range(self.sizeY):
            for x in range(self.sizeX):
                xx = int(x/rate)
                yy = int(y/rate)

                val = self.data[x][y]
                if compressed_matrix.data[xx][yy] == defaultValue:
                    compressed_matrix.data[xx][yy] = val

        return compressed_matrix

#
# Depricated
#

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

def create_matrix_from_file_flipped(textfile):
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

#
# Create a full matrix from file
#
def create_matrix_from_file(textfile):
    file_lines = loadfile(textfile)

    ySize = len(file_lines)
    xSize = len(file_lines[0].strip())
    matrix = create_empty_matrix(xSize,ySize)

    for y in range(0,len(file_lines)):
        line = file_lines[y]
        line = line.strip()
        for x in range(len(line)):
            data = line[x]
            matrix[x][y] = data
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
    print_matrix_color(text,matrix,"",bcolors.RESET,"")

def print_matrix_color(text,matrix,value_highlight,color, pad = "00", space = " "):
    valueList = list()
    valueList.append(value_highlight)
    print_matrix_colorlist(text,matrix,valueList, color, bcolors.WHITE, pad, space)

def print_matrix_colorlist(text,matrix, valueList, color, defaultColor, pad = "00", space = " "):
    size = get_matrix_size(matrix)

    size_x = size[0]
    size_y = size[1]
    pad_size = len(pad)
    pady_size = len(str(size_y-1))

    print ("      --- " + text + " " + str(size_x) + "x" + str(size_y)  + " ---")
    print("")

    header  = defaultColor
    header2 = color

    for i in range(pady_size):
        header = header + " " 
        header2 = header2 + " "

    header = header + " + "
    header2 = header2 + "   "

    pad_header_x = ""
    if len(pad)>1:
        for i in range(pad_size):
            pad_header_x += "0"
#        pad_header_x = pad[0] + pad_header_x[0] + pad_header_x[1]

    for x in range(size_x):
        xx = x % 10
        if len(pad) > 1:
            xx = x % 100

        xxPad = pad_number( xx , pad_header_x )

#        if xx == 0:
#            xxPad = bcolors.BOLD + bcolors.WHITE + xxPad
        xxPad = bcolors.WHITE + xxPad + bcolors.DARK_GREY

        header2 += xxPad
        for i in range(pad_size):
            header = header + "-"
        header2 = header2 + space
        header = header + space

    print(bcolors.BOLD + color +  header2)
    print(bcolors.BOLD + defaultColor + header)

    pady = ""
    for i in range(pady_size):
        pady += "0"

    for y in range(size_y):
        line = ""
        line = line + bcolors.BOLD + bcolors.WHITE
        line = line + pad_number(y,pady)
        line = line + defaultColor
        line = line + " | "

        for x in range(size_x):
            value = matrix[x][y]

            highlight_color = defaultColor
            v = "" + str(value)

            if isinstance(valueList,int):
                if value == valueList:
                    highlight_color = bcolors.BOLD + color
            else:
                for highlight_value in valueList:
                    if isinstance(highlight_value,int) and value == highlight_value:
                        highlight_color = bcolors.BOLD + color
                    elif isinstance(highlight_value,str) and highlight_value in v:
                        highlight_color = bcolors.BOLD + color
                    elif isinstance(highlight_value,tuple):
                        tupleValue = highlight_value[0]
                        tupleColor = highlight_value[1]
                        if tupleValue in v: 
                            highlight_color = bcolors.BOLD + tupleColor

            line = line + highlight_color
            line += pad_number( value , pad )
            line += space
        print(line)
    print ("" + bcolors.RESET)
