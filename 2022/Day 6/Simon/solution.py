#!/usr/local/bin/python3

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *

def identifyMarker(dataStream, markerlength):
    iteration = 0
    for bit in dataStream:
        potentialMarker = dataStream[iteration:iteration+markerlength]
        counter = 0
        for i in potentialMarker:
            if potentialMarker.count(i) == 1:
                counter += 1
            else:
                counter = 0
        if counter == markerlength:
            return potentialMarker, iteration + markerlength
        iteration += 1

def outputEmission(dataStream):
    streams = loadfile(dataStream)
    for stream in streams:
        result = identifyMarker(stream, 14)
        # print(result)
        print("Marker after : " + str(result[1]) + " bits")
        print("Marker: " + str(result[0]))
        print("-------------")

outputEmission("input.txt")