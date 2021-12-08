# Open file containing the depth measurements for reading
file = open("measurements.txt", "r")

# Read the measurements from the file, and add them to a list
measurement_list = file.readlines()

# Close the file again, it's no longer needed
file.close()

# Get the number of measurements
length = len(measurement_list)
print(length)

# Initialize the variable that will hold the 
# measurements that are higher than the previous one
increased_measurement = 0

# Loop through all the measurements, and count the ones 
# that are larger than the previous
for i in range(0, length):
    if i+1<length:
        first_measurement = int(measurement_list[i])
        second_measurement = int(measurement_list[i + 1])
    else:
        break

    if second_measurement > first_measurement:
        increased_measurement = increased_measurement + 1

# Finally, print the number of measurements that are larger than the previous
print(increased_measurement)