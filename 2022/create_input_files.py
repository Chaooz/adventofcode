#!/usr/local/bin/python3

import os

dayrange = range(9, 26)

for day in dayrange:
    if (os.path.exists("Day " + str(day) + "/Thor/unittest.txt") == False):
        f = open("Day " + str(day) + "/Thor/unittest.txt", "w")
        f.write("The testinput for day " + str(day) + " is goes here")
        f.close()
    if (os.path.exists("Day " + str(day) + "/Thor/puzzleinput.txt") == False):
        f = open("Day " + str(day) + "/Thor/puzzleinput.txt", "w")
        f.write("The actual input for day " + str(day) + " is goes here")
        f.close()
    if (os.path.exists("Day " + str(day) + "/Thor/solution.py") == False):
        f = open("Day " + str(day) + "/Thor/solution.py", "w")
        f.write("#!/usr/local/bin/python3")
        f.close()
    if (os.path.exists("Day " + str(day) + "/Thor/puzzleinput_work.txt") == False):
        f = open("Day " + str(day) + "/Thor/puzzleinput_work.txt", "w")
        f.write("The actual work input for day " + str(day) + " is goes here")
        f.close()