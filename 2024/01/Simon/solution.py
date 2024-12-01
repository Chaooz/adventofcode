#!/usr/lib/python3
import sys
sys.path.insert(1, '../../../Libs')
from advent_libs import loadfile

raw_array = loadfile("input.txt")

first_num = []
second_num = []

for line in raw_array:
    new_line = line.split("   ")
    first_num.append(int(new_line[0]))
    second_num.append(int(new_line[1]))

first_num.sort()
second_num.sort()

distance = 0
iteration = 0

# Find disance score
for number in first_num:
    if first_num[iteration] > second_num[iteration]:
        diff = first_num[iteration] - second_num[iteration]
    else:
        diff = second_num[iteration] - first_num[iteration]
    distance += diff
    iteration += 1

print("Total distance is " + str(distance))

similarity_score = 0

# Find similarity score
for num in first_num:
    number_of_instances = second_num.count(num)
    similarity_score += number_of_instances * num

print("Similarity score is " + str(similarity_score))