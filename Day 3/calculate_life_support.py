# Open file containing the depth measurements for reading
file = open("diagnostic_report.txt", "r")

# Read the measurements from the file, and add them to a list
binary_readouts = file.readlines()

# Close the file again, it's no longer needed
file.close()

i = 0

oxygen_generator_rating = binary_readouts

for i in range(0, 11):
    ones = list()
    zeros = list()
    for readout in oxygen_generator_rating:
        if readout[i] == "1":
            ones.append(readout)
        else:
            zeros.append(readout)
    if len(ones) >= len(zeros):
        oxygen_generator_rating = ones
    else:
        oxygen_generator_rating = zeros
    i += 1

oxygen_generator_rating_binary = str(oxygen_generator_rating[0])
oxygen_generator_rating_decimal = str(int(oxygen_generator_rating_binary,2))
print("Oxygen generator rating (Binary): " + oxygen_generator_rating_binary)
print("Oxygen generator rating (Decimal): " + oxygen_generator_rating_decimal)

co2_scrubber_rating = binary_readouts

i = 0

for i in range(0, 11):
    ones = list()
    zeros = list()
    for readout in co2_scrubber_rating:
        if readout[i] == "1":
            ones.append(readout)
        else:
            zeros.append(readout)
    if len(ones) >= len(zeros):
        co2_scrubber_rating = zeros
    else:
        co2_scrubber_rating = ones
    if len(co2_scrubber_rating) == 1:
        break
    i += 1

co2_scrubber_rating_binary = str(co2_scrubber_rating[0])
co2_scrubber_rating_decimal = str(int(co2_scrubber_rating_binary,2))
print("co2 scrubber rating (Binary): " + co2_scrubber_rating_binary)
print("co2 scrubber rating (Decimal): " + co2_scrubber_rating_decimal)

life_support_rating = int(oxygen_generator_rating_decimal) * int(co2_scrubber_rating_decimal)
print("Life Support Rating: " + str(life_support_rating))