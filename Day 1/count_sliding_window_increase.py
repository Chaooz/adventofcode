# Open file containing the depth measurements for reading
file = open("measurements.txt", "r")

# Read the measurements from the file, and add them to a list
measurement_list = file.readlines()

# Close the file again, it's no longer needed
file.close()

# Get the number of measurements
length = len(measurement_list)

# Initialize the variable that will hold the 
# measurements that are higher than the previous one
increased_measurement = 0

# Loop through all the measurements, pull the next 4, and create
# the two sliding windows for comparison. Break if there is not
# enough measurements to create the two windows.
for i in range(0, length):
    if i+3<length:
        measurement1 = int(measurement_list[i])
        measurement2 = int(measurement_list[i+1])
        measurement3 = int(measurement_list[i+2])
        measurement4 = int(measurement_list[i+3])
    else:
        break

    first_sliding_window = measurement1 + measurement2 + measurement3
    second_sliding_window = measurement2 + measurement3 + measurement4

    # Compare the windows, and increment if the second one is larger
    # than the previous.
    if second_sliding_window > first_sliding_window:
        increased_measurement = increased_measurement + 1

# Finally, print the number of sliding windows that are larger than 
# the previous. 
print(increased_measurement)
