#
# Day 19: Beacon Scanner
#
#!/usr/lib/python3

import sys

# Import custom libraries
sys.path.insert(1, '../../Libs')
from advent_libs import *
from advent_libs_matrix import *
from advent_libs_list import *

#
# Assignment : Find scanner positions
# Rules
# * Scanners cannot detect other scanners
# * Scanner can detect beacon within 1000 
# * Scanner overlaps with at least 12 common beacons

class Vector2():
    x = int()
    y = int()

    def __init__(self, xy = None):
        if xy is not None:
            self.x = xy[0]
            self.y = xy[1]

    def __eq__(self, other):
        if isinstance(other,Vector2):
            return self.x == other.x and self.y == other.y
        else:
            return self.x == other[0] and self.y == other[1]

    def tuple(self):
        return ( self.x, self.y )

def create_2d_beacons(filename):
    lines = loadfile(filename)
    beaconList = []    
    for line in lines:
        line = line.replace("\n","")
        if line.startswith("--"):
            beacon = []
            beacon.append( (0,0,0,"S") )
        elif line == "":
            beaconList.append(beacon)
        else:
            x,y = line.split(",")
            beacon.append( (int(x),int(y), 0, "B") )

    beaconList.append(beacon)
    return beaconList

def create_3d_beacons(filename):
    lines = loadfile(filename)
    beaconList = []    
    for line in lines:
        line = line.replace("\n","")
        if line.startswith("--"):
            beacon = []
            beacon.append( (0,0,0,"S") )
        elif line == "":
            beaconList.append(beacon)
        else:
            x,y = line.split(",")
            beacon.append( (int(x),int(y), 0, "B") )

    beaconList.append(beacon)
    return beaconList

# How many points in the beacon list matches
def matchPoint(list1, list2):
    count = 0
    for entry1 in list1:        
        for entry2 in list2:
#            if entry2[2] != "S":
            if entry1[0] == entry2[0] and entry1[1] == entry2[1]:
                count += 1
    return count

def offset_points(list, x,y):
    newList = []
    for point in list:
        newList.append( (point[0] + x, point[1] + y, point[2]) )
    return newList

def findOffset(point1,point2):
    offsetX = point1[0] - point2[0]
    offsetY = point1[1] - point2[1]
    return (offsetX,offsetY)

def getOffsetWithMaches( beacon1, beacon2, numMatches):
    for point1 in beacon1:
        for point2 in beacon2:
            x,y = findOffset(point1, point2)    
            newList = offset_points(beacon2,x,y)
            num = matchPoint( beacon1, newList )
            if num >= numMatches:
                return newList
    print_warning("getOffsetWithMaches : none found")
    return None

def createMergedList(beaconList):
    mergedList = []
    firstBeacon = beaconList[0]

    for point in firstBeacon:
        mergedList.append(point)

    for index in range(1,len(beaconList)):
        nextBeacon = beaconList[index]
        newList = getOffsetWithMaches(firstBeacon,nextBeacon, 3)
        for point2 in newList:
            if point2 not in mergedList:
                mergedList.append(point2)

    return mergedList

def debugPrintBeacons(filename):
    beaconList = create_beacons(filename)
    newList = createMergedList(beaconList)
    max = max_point_in_list(newList)
    min = min_point_in_list(newList)
    size = ( max[0] - min[0], max[1] - min[1] )      
    matrix = create_empty_matrix( size[0] + 1, size[1] + 1, 0)
    matrix_plot_list(matrix, newList)
    print_matrix_color("Beacon",matrix,0,bcolors.DARK_GREY,"","")

print("")
print_color("Day 19: Beacon Scanner", bcolors.OKGREEN)
print("")

#unittest( create_beacons, [[(0, 2, 1), (4, 1, 1), (3, 3, 1)], [(-1, -1, 1), (-5, 0, 1), (-2, 1, 1)]], "unittest1.txt")

debugPrintBeacons("unittest1.txt")

