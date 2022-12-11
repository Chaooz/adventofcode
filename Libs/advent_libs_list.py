
import sys
from advent_libs import *
from advent_libs_vector2 import *


class Vector2List:

    name:str
    data:list
    current_index:int

    def __init__(self,name = "") -> None:
        self.data = list()
        self.name = name
        self.current_index = 0
        pass

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_index < len(self.data):
            point = self.data[self.current_index]
            self.current_index += 1
            return point
        raise StopIteration
        
    def len(self):
        return len(self.data)

    def appendList(self, data:list) -> None:
        for entry in data:
            if ( len( entry > 2 ) ):
                self.data.append( Vector2( entry[0], entry[1] ), entry[3])
            else:
                self.data.append( Vector2( entry[0], entry[1] ))

    def append(self,data:Vector2):
        self.data.append(data)
#        print("VecList.append[" + self.name + "]:" + data.ToString() + " " + str(self.len()))

    def Get(self, index:int) -> Vector2:
        d = self.data[index]
#        print("VecList.Get[" + self.name + "]:" + str(index) + " => " + d.ToString())
        return d

    def GetWithPos(self, otherPos:Vector2) -> Vector2:
        for pos in self.data:
            if pos == otherPos:
                return pos
        return None

    def First(self) -> Vector2:
        if len(self.data) > 0:
            return self.data[0]
        return None

    def Last(self) -> Vector2:
        if len(self.data) > 0:
            return self.data[ len(self.data) - 1]
        return None

    def ToString(self, maxLines = 100) -> str:
        s = ""
        for line in self.data:
            s += self.name + ": " + line.ToString() + "\n"
            maxLines -= 1
            if maxLines <= 0:
                return s
        return s

    def Print(self, maxLines = 100):
        p = self.ToString(maxLines)
        print(p)

    def MaxPoint(self) -> Vector2:
        x = y = 0
        for vec in self.data:
           if vec.x > x: x = vec.x
           if vec.y > y: y = vec.y
        return Vector2(x,y) 

    def MinPoint(self) -> Vector2:
        x = y = 9999999999999
        for vec in self.data:
           if vec.x < x: x = vec.x
           if vec.y < y: y = vec.y
        return Vector2(x,y) 



#
# All under here is depricated
#


def listToString(s):
    str1 = ""
    for ele in s:
        if str1 == "":
            str1 += "["
        else:
            str1 += ","
        str1 += str(ele)
    str1 += "]"
    return str1

#
# Create a list of tuples from the textfile
#
def listFromFile(textfile, delimiter):
    file_lines = loadfile(textfile)
    my_list = list()
    for line in file_lines:
        line = line.strip()
        key_value = line.split(delimiter)        
        my_list.append(key_value)
    return my_list

def min_point_in_list(point_list):
    min_x = 0
    min_y = 0
    for input in point_list:
        x = int(input[0])
        y = int(input[1])
        if x < min_x:
            min_x = x
        if y < min_y:
            min_y = y
    return (min_x, min_y)

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
