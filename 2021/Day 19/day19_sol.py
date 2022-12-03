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

def create_beacons(filename):
    lines = loadfile(filename)
    beaconList = []    
    for line in lines:
        line = line.replace("\n","")
        if line.startswith("--"):
            beacon = []
            beacon.append( (0,0, "S") )
        elif line == "":
            beaconList.append(beacon)
        else:
            x,y = line.split(",")
            beacon.append( (int(x),int(y), "B") )

    beaconList.append(beacon)
    return beaconList

def debugPrintBeacons(filename):
    beaconList = create_beacons(filename)

    for beacon in beaconList:

        max = max_point_in_list(beacon)
        min = min_point_in_list(beacon)
        size = ( max[0] - min[0], max[1] - min[1] )        
        matrix = create_empty_matrix( size[0] + 1, size[1] + 1, 0)
 
        offsetBeacon = list_offset( 0 - min )

        matrix_plot_list(matrix, beacon)

        print_matrix_color("Beacon",matrix,0,bcolors.DARK_GREY,"","")

unittest( create_beacons, [[(0, 2, 1), (4, 1, 1), (3, 3, 1)], [(-1, -1, 1), (-5, 0, 1), (-2, 1, 1)]], "unittest1.txt")

debugPrintBeacons("unittest1.txt")

