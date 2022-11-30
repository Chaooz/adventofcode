# Function to read the content of the puzzle input file
def loadfile(filename):
    file = open(filename)
    lines = file.read()
    file.close()
    return lines

# Function to find the highest value in a list
def highest_value_in_list(input_list):
    ret = 0
    for value in input_list:
        if value > ret:
            ret = value
    return ret

# Create list of initial positions
crab_position_string = loadfile("crab_initial_positions.txt")
crab_position_list = crab_position_string.split(",")
crab_positions = list()
for crab in crab_position_list:
    crab_positions.append(int(crab))

# Initialize a variable to hold the lowest fuel ammount and the best position
lowest_fuel_consumption = 9999999999999999999
best_position = 0

# Find highest position in the list
highest_position = highest_value_in_list(crab_positions)
print("Highest Position: " + str(highest_position))

# Loop through each position between 1 and list max, calculating the fuel needed to get all crabs to this position
# While looping, if the new value is lower than the previous best, record the new best and new position
for i in range(highest_position):
    fuel_consumption = 0
    for crab in crab_positions:
        if crab > i:
            fuel_to_position = crab - i
            fuel_consumption += fuel_to_position
        else:
            fuel_to_position = i - crab
            fuel_consumption += fuel_to_position
    if fuel_consumption < lowest_fuel_consumption:
        lowest_fuel_consumption = fuel_consumption
        best_position = i

print("The best position is " + str(best_position))
print("Fuel consumption to get all crabs to this position is " + str(lowest_fuel_consumption))