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
        if ( lineY > self.sensor.y - self.width and lineY < self.sensor.y + self.width ):
            return True
        return False

    def GetSectorWidth(self, lineY:int) -> Vector2:        
        diffY = self.sensor.y - lineY if self.sensor.y > lineY else lineY - self.sensor.y
        v = Vector2( self.sensor.x - self.width + diffY + 1, self.sensor.x + self.width - diffY - 1)
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

#
# calcNumPoints
# Find the number of points needed to make a square
#
def calcNumPoints(sensor:Vector2, beacon:Vector2):
    pointX = sensor.x - beacon.x if beacon.x < sensor.x else beacon.x - sensor.x
    pointY = sensor.y - beacon.y if beacon.y < sensor.y else beacon.y - sensor.y
    return pointX + pointY + 1

def generateRange(beaconList, intersectLine:int):
    selectedBeaconList = Vector2List()

    # Find the range for each beacon on a specific line
    for data in beaconList:
        if data.intersect(intersectLine):
            sectorWidth = data.GetSectorWidth(intersectLine)
            selectedBeaconList.append(sectorWidth)            

    # Sort ranges with smallest start first
    selectedBeaconList.Sort()
    print("generateRange:" + selectedBeaconList.ToString())

    # Merge list
    combinedList = Vector2List()
    combinedSize = Vector2(999999999,0)
    for data in selectedBeaconList.data:
        # Expand ranges
        didFind = False
        for index in range(0, combinedList.len()):
            combinedData = combinedList.Get(index)

            # First is inside range
            if data.x >= combinedData.x and data.x <= combinedData.y:
                didFind = True
                # If second is larger, expand the range
                if data.y > combinedData.y: 
                    combinedData.y = data.y
                    combinedList.SetWithIndex(index,combinedData)
#                    print("Expand:" + combinedData.ToString() + " y:" + str(combinedData.y) + " < " + str(data.y))
            # Second is inside range
            if data.y >= combinedData.x and data.y <= combinedData.y:
                didFind = True
                # If first is smaller, shrink the range
                if data.x < combinedData.x: 
 #                   print("Shrink:" + combinedData.ToString() + " x:" + str(combinedData.x) + " < " + str(data.x))
                    combinedData.x = data.x
                    combinedList.SetWithIndex(index,combinedData)
 
        if not didFind:
#            print("could not find : " + data.ToString() + " => " + combinedList.ToString())
            combinedList.append(data)

    print("combinedList " + combinedList.ToString())
    return combinedList

def debugDrawSensorPoint(matrix:Matrix,x,y, character:str):
    c = matrix.Get(x,y)
    if c == "." or c == "o":
      matrix.Set( x,y, character)

def showDebugMatrix(sensorData:SensorData, rangeList:Vector2List, countYLine:int, printIndex:int):

    # Calucate max/min value
    minPoint = Vector2(0,0)
    maxPoint = Vector2(0,0)

    for data in sensorData:
        w = data.width

        if data.sensor.x - w < minPoint.x: minPoint.x = data.sensor.x - w
        if data.sensor.y - w < minPoint.y: minPoint.y = data.sensor.y - w
        if data.beacon.x - w < minPoint.x: minPoint.x = data.beacon.x - w
        if data.beacon.y - w < minPoint.y: minPoint.y = data.beacon.y - w

        if data.sensor.x + w > maxPoint.x: maxPoint.x = data.sensor.x + w
        if data.sensor.y + w > maxPoint.y: maxPoint.y = data.sensor.y + w
        if data.beacon.x + w > maxPoint.x: maxPoint.x = data.beacon.x + w
        if data.beacon.y + w > maxPoint.y: maxPoint.y = data.beacon.y + w

    matrixSize = Vector2(maxPoint.x - minPoint.x, maxPoint.y - minPoint.y)
    matrix = Matrix("Test", matrixSize.x, matrixSize.y, ".")

    colorList = list()
    colorList.append(("B", bcolors.YELLOW))
    colorList.append(("b", bcolors.YELLOW))
    colorList.append(("s", bcolors.RED))
    colorList.append(("S", bcolors.OKGREEN))
    colorList.append(("@", bcolors.YELLOW))
    colorList.append(("o", bcolors.DARK_GREY))
    colorList.append(("#", bcolors.LIGHT_GREY))
    colorList.append(("0", bcolors.OKGREEN))

    printNum = 0
    for data in sensorData:
        printNum += 1
        bPoint = matrix.GetPoint(data.beacon)
        sPoint = matrix.GetPoint(data.sensor)

        c = "o"
        if data.intersect(countYLine):
            matrix.SetPoint(data.sensor, "S")
            matrix.SetPoint(data.beacon, "B")
            c = "#"
        elif bPoint != "B" :
            matrix.SetPoint(data.beacon, "b")
        elif sPoint != "S" :
            matrix.SetPoint(data.sensor, "s")

        if printIndex == printNum or printIndex == -1:
            for y in range(0, data.width ):
                for x in range( 0, data.width - y - 1):
                    debugDrawSensorPoint(matrix, data.sensor.x + x, data.sensor.y + y, "o")
                    debugDrawSensorPoint(matrix, data.sensor.x + x, data.sensor.y - y, "o")
                    debugDrawSensorPoint(matrix, data.sensor.x - x, data.sensor.y + y, "o")
                    debugDrawSensorPoint(matrix, data.sensor.x - x, data.sensor.y - y, "o")

                # Draw outline of the area with "#" for areas included in the calculation
                debugDrawSensorPoint(matrix, data.sensor.x + data.width - y - 1, data.sensor.y + y, c)
                debugDrawSensorPoint(matrix, data.sensor.x - data.width + y + 1, data.sensor.y - y, c)
                debugDrawSensorPoint(matrix, data.sensor.x + data.width - y - 1, data.sensor.y - y, c)
                debugDrawSensorPoint(matrix, data.sensor.x - data.width + y + 1, data.sensor.y + y, c)

        # Print the Y line
        for dataRange in rangeList:
            for p in range( dataRange.x, dataRange.y + 1):
                c = matrix.Get(p, countYLine)
                if c == ".":
                    matrix.Set(p, countYLine, "@")

#    matrix.SetPoint(Vector2(24,21), "0")

    matrix.PrintWithColor(colorList, bcolors.DARK_GREY, ""," ")


def offsetDataPoints(beaconList:list, offset:Vector2):
    # Offset the beaconlist
    for data in beaconList:
        data.sensor.x += offset.x
        data.sensor.y += offset.y
        data.beacon.x += offset.x
        data.beacon.y += offset.y
    return beaconList

def updateWidth(beaconList:list):
    for data in beaconList:
        data.width = calcNumPoints(data.sensor, data.beacon)
    return beaconList

def solveInternalPuzzle1(filename:str, offset:Vector2, countLine:int, debug:bool, showBox:int):
    lines = loadfile(filename)
    beaconList = readInput(lines)

    beaconList = offsetDataPoints(beaconList, offset)
    countLine += offset.y

    beaconList = updateWidth(beaconList)
    rangeList = generateRange(beaconList,countLine)

    # Draw matrix with Sensors, Beacons and coverage area
    if debug:
        showDebugMatrix(beaconList, rangeList, countLine, showBox)

    selectedRange = rangeList.First()
    return selectedRange.y - selectedRange.x

def solveInternalPuzzle2(filename:str, offset:Vector2, countLine:int, debug:bool, showBox:int):
    lines = loadfile(filename)
    beaconList = readInput(lines)
    
    beaconList = offsetDataPoints(beaconList, offset)
    countLine += offset.y

    beaconList = updateWidth(beaconList)
    rangeList = generateRange(beaconList,countLine)

    # Draw matrix with Sensors, Beacons and coverage area
    if debug:
        showDebugMatrix(beaconList, rangeList, countLine, showBox)

    # Find the points within range

#    num = combinedSize.y - combinedSize.x
    return -1

def testPuzzle1(filename):
    return solveInternalPuzzle1(filename, Vector2(10,10), 10, True, -1)

def solvePuzzle1(filename):
    return solveInternalPuzzle1(filename, Vector2(0,0), 2000000, False, -1 )

def testPuzzle2(filename):
    return solveInternalPuzzle2(filename, Vector2(10,10), 11, False, -1)

unittest(testPuzzle1, 26, "unittest.txt")
unittest(solvePuzzle1, 4748135, "puzzleinput.txt")
unittest(testPuzzle2, 1, "unittest.txt")
