# Open file containing the depth measurements for reading
file = open("movement.txt", "r")

# Read the measurements from the file, and add them to a list
movements = file.readlines()

# Close the file again, it's no longer needed
file.close()

# Create an empty list that will hold all the movements.
# Initialize the variables that will hold the position
# data.
movement_tuples = list()
horizontal_position = 0
depth = 0
aim = 0

# For each movement, split the string and add the two
# resulting strings to a tuple. Add this tuple to the
# list created to hold them.
for movement in movements:
    split_movement = movement.split()
    movement_tuple = tuple((split_movement))
    movement_tuples.append(movement_tuple)

# Loop through the movements, and update the position
# based on the movement specified.
for movement in movement_tuples:
    if movement[0] == "forward":
        horizontal_position = horizontal_position + int(movement[1])
        depth = depth + (aim * int(movement[1]))
    elif movement[0] == "up":
        aim = aim - int(movement[1])
    else:
        aim = aim + int(movement[1])

# Print the solution information.
print("Horizontal position: " + str(horizontal_position))
print("Depth: " + str(depth))
print("Product of horizontal position and depth: " + str(horizontal_position * depth))