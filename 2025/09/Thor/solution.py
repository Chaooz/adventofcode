#!/usr/local/bin/python3
# https://adventofcode.com/2025/day/09

import sys
import re

# Import custom libraries
sys.path.insert(1, '../../../Libs')
sys.path.insert(1, '../Libs')

from advent_libs import *
from advent_libs_vector2 import *
from advent_libs_models import *

def solvePuzzle1(filename):    
    lines = loadfile(filename)
    points = []
    for line in lines:
        x,y = line.strip().split(",")
        points.append( (int(x), int(y)) )

    maxArea = 0
    for i, pointA in enumerate(points):
        for j, pointB in enumerate(points):
            if i>=j:
                continue
            area = abs(pointA[0]-pointB[0]+1) * abs(pointA[1]-pointB[1]+1)
            if area > maxArea:
                maxArea = area

    return maxArea

def solvePuzzle2(filename):
    lines = loadfile(filename)
    points = []
    for line in lines:
        x,y = line.strip().split(",")
        points.append( Vector2(int(x), int(y)) )

    # Create polygon
    polygon = Polygon(points + [points[0]])

    maxArea = 0
    for i, pointA in enumerate(points):
        for j, pointB in enumerate(points):
            if i>=j:
                continue

            minX = min(pointA.x, pointB.x)
            maxX = max(pointA.x, pointB.x)
            minY = min(pointA.y, pointB.y)
            maxY = max(pointA.y, pointB.y)

            area = abs(maxX - minX + 1) * abs(maxY - minY + 1)

            if area > maxArea:
    
                # Check if area crosses polygon edges
                if polygon.isAreaCrossing( minX, minY, maxX, maxY ):
                    continue

                # Check if the center of the area is inside the polygon
                if not polygon.isPointInside(Vector2(minX + 0.5, minY + 0.5)):
                    continue

                maxArea = area

    return maxArea

UNITTEST.DEBUG_ENABLED = False

setupCode("Day 9: Movie Theater")

unittest(solvePuzzle1, 50, "unittest1.txt")
unittest(solvePuzzle2, 24, "unittest1.txt")

runCode(9,solvePuzzle1, 4735222687, "input.txt")
runCode(9,solvePuzzle2, 1569262188, "input.txt")
