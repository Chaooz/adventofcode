#!/usr/local/bin/python3

import sys

# Import custom libraries
sys.path.insert(1, '../../../Libs')
from advent_libs import *
from advent_libs_vector2 import *
from advent_libs_matrix import *

print("")
print_color("Day 15: Beacon Exclusion Zone", bcolors.OKGREEN)
print("")

class SensorData:
    beacon : Vector2
    sensor : Vector2
    width : int

    def intersect(self, lineY:int) -> bool:
        if ( lineY >= self.sensor.y - self.width and lineY <= self.sensor.y + self.width ):
            return True
        return False

    def GetSectorWidth(self, lineY:int) -> Vector2:
        diffY = self.sensor.y - lineY if self.sensor.y > lineY else lineY - self.sensor.y
        v = Vector2( self.sensor.x - self.width + diffY, self.sensor.x + self.width - diffY)
        print("width:" + str(lineY) + " => " + self.sensor.ToString() + " v:" + v.ToString())
        return v

    
def readInput(lines):
    beaconList = []
    for line in lines:
        line = line.strip()
        line = line.replace(",","")
        line = line.replace(":","")
        a,b,sensorX,sensorY,c,d,e,f,beaconX,beaconY = line.split(" ")
        sensor = Vector2( int(sensorX.split("=")[1]), int(sensorY.split("=")[1]))
        beacon = Vector2( int(beaconX.split("=")[1]), int(beaconY.split("=")[1]))

        sensorData = SensorData()
        sensorData.sensor = sensor
        sensorData.beacon = beacon
        sensorData.width = 0
        beaconList.append(sensorData)

    return beaconList

def calcNumPoints(sensor:Vector2, beacon:Vector2):
    pointX = sensor.x - beacon.x if beacon.x < sensor.x else beacon.x - sensor.x
    pointY = sensor.y - beacon.y if beacon.y < sensor.y else beacon.y - sensor.y
    return pointX + pointY + 1

def calcLine(matrix:Matrix, line):
    num = 0
    for x in range(0,matrix.sizeX):
        c = matrix.Get(x,line)
        if c == "#":
            num += 1
    return num

def debugDrawSensorPoint(matrix:Matrix,x,y):
    c = matrix.Get(x,y)
    if c == ".":
        matrix.Set( x,y, "#")

def showDebugMatrix(sensorData:SensorData, offset:Vector2, countXLine:Vector2, countYLine:int):

    # Calucate max/min value
    minPoint = Vector2(0,0)
    maxPoint = Vector2(0,0)

    for data in sensorData:

        if data.sensor.x < minPoint.x: minPoint.x = data.sensor.x
        if data.sensor.y < minPoint.y: minPoint.y = data.sensor.y
        if data.beacon.x < minPoint.x: minPoint.x = data.beacon.x
        if data.beacon.y < minPoint.y: minPoint.y = data.beacon.y

        if data.sensor.x > maxPoint.x: maxPoint.x = data.sensor.x
        if data.sensor.y > maxPoint.y: maxPoint.y = data.sensor.y
        if data.beacon.x > maxPoint.x: maxPoint.x = data.beacon.x
        if data.beacon.y > maxPoint.y: maxPoint.y = data.beacon.y

    matrixSize = Vector2(maxPoint.x - minPoint.x + (offset.x*2), maxPoint.y - minPoint.y + (offset.y*2))

    # Offset all points ( for printing of matrix )
    for data in sensorData:
        data.beacon.x -= minPoint.x - offset.x
        data.beacon.y -= minPoint.y - offset.y
        data.sensor.x -= minPoint.x - offset.x
        data.sensor.y -= minPoint.y - offset.y

    matrix = Matrix("Test", matrixSize.x, matrixSize.y, ".")

    colorList = list()
    colorList.append(("B", bcolors.YELLOW))
    colorList.append(("S", bcolors.RED))
    colorList.append(("s", bcolors.OKGREEN))
    colorList.append(("@", bcolors.WHITE))

    for data in sensorData:
        matrix.SetPoint(data.beacon, "B")

        if data.intersect(countYLine):
            matrix.SetPoint(data.sensor, "s")
        else:
            matrix.SetPoint(data.sensor, "S")

        for p in range( countXLine.x, countXLine.y):
            c = matrix.Get(p + offset.x, countYLine + offset.y)
            if c == ".":
                matrix.Set( p + offset.x, countYLine + offset.y, "@")

        for y in range(0, data.width ):
            for x in range( 0, data.width - y ):
                debugDrawSensorPoint(matrix, data.sensor.x + x, data.sensor.y + y)
                debugDrawSensorPoint(matrix, data.sensor.x + x, data.sensor.y - y)
                debugDrawSensorPoint(matrix, data.sensor.x - x, data.sensor.y + y)
                debugDrawSensorPoint(matrix, data.sensor.x - x, data.sensor.y - y)

    matrix.PrintWithColor(colorList, bcolors.DARK_GREY, ""," ")


def solvePuzzle(filename:str, offset:Vector2, countLine:int, debug:bool):
    lines = loadfile(filename)
    beaconList = readInput(lines)

    # Calculate max width for each sensor
    combinedSize = Vector2(0,0)
    for data in beaconList:
        data.width = calcNumPoints(data.sensor, data.beacon)
        if data.intersect(countLine):
            sectorWidth = data.GetSectorWidth(countLine)
            if sectorWidth.x < combinedSize.x: combinedSize.x = sectorWidth.x
            if sectorWidth.y > combinedSize.y: combinedSize.y = sectorWidth.y

    num = combinedSize.y - combinedSize.x
    print(combinedSize.ToString())
    print(num)

    # Draw matrix with Sensors, Beacons and coverage area
    if debug:
        showDebugMatrix(beaconList, offset, combinedSize, countLine)

    return num

def testPuzzle1(filename):
    return solvePuzzle(filename, Vector2(10,10), 10, True)

def solvePuzzle1(filename):
    return solvePuzzle(filename, Vector2(10,5), 10, True)

def solvePuzzle2(filename):
    lines = loadfile(filename)
    return 0

unittest(testPuzzle1, 26, "unittest.txt")
#unittest(solvePuzzle1, 1, "unittest.txt")
#unittest(solvePuzzle1, 1, "puzzleinput.txt")
#unittest(solvePuzzle2, 1, "puzzleinput.txt")