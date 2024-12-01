#!/usr/lib/python3
import sys
sys.path.insert(1, '../../../Libs')
from advent_libs import loadfile

# Load the data from the input file
raw_list = loadfile("input.txt")

# Create 2 empty lists to store the numbers
first_num = []
second_num = []

# Add the 2 numbers to its respective list
for line in raw_list:
    new_line = line.split("   ")
    first_num.append(int(new_line[0]))
    second_num.append(int(new_line[1]))

# Sort the lists
first_num.sort()
second_num.sort()

# Initialize variables
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

# Print the distance score
print("Total distance is " + str(distance))


# Initialize variables
similarity_score = 0

# Find similarity score
for num in first_num:
    number_of_instances = second_num.count(num)
    similarity_score += number_of_instances * num

# Print the similarity score
print("Similarity score is " + str(similarity_score))