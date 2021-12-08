# Open file containing the depth measurements for reading
file = open("diagnostic_report.txt", "r")

# Read the measurements from the file, and add them to a list
binary_readouts = file.readlines()

# Close the file again, it's no longer needed
file.close()

bin1 = 0
bin2 = 0
bin3 = 0
bin4 = 0
bin5 = 0
bin6 = 0
bin7 = 0
bin8 = 0
bin9 = 0
bin10 = 0
bin11 = 0
bin12 = 0


gamma = str()
epsilon = str()

for readout in binary_readouts:
    iteration = 0 
    for char in readout:
        iteration += 1
        if char == "1":
            if iteration == 1:
                bin1 += 1
            elif iteration == 2:
                bin2 += 1
            elif iteration == 3:
                bin3 += 1
            elif iteration == 4:
                bin4 += 1
            elif iteration == 5:
                bin5 += 1
            elif iteration == 6:
                bin6 += 1
            elif iteration == 7:
                bin7 += 1
            elif iteration == 8:
                bin8 += 1
            elif iteration == 9:
                bin9 += 1
            elif iteration == 10:
                bin10 += 1
            elif iteration == 11:
                bin11 += 1
            else:
                bin12 += 1

if bin1 >= 500:
    gamma = "1"
else:
    gamma = "0"
if bin2 >= 500:
    gamma = gamma + "1"
else:
    gamma = gamma + "0"
if bin3 >= 500:
    gamma = gamma + "1"
else:
    gamma = gamma + "0"
if bin4 >= 500:
    gamma = gamma + "1"
else:
    gamma = gamma + "0"
if bin5 >= 500:
    gamma = gamma + "1"
else:
    gamma = gamma + "0"
if bin6 >= 500:
    gamma = gamma + "1"
else:
    gamma = gamma + "0"
if bin7 >= 500:
    gamma = gamma + "1"
else:
    gamma = gamma + "0"
if bin8 >= 500:
    gamma = gamma + "1"
else:
    gamma = gamma + "0"
if bin9 >= 500:
    gamma = gamma + "1"
else:
    gamma = gamma + "0"
if bin10 >= 500:
    gamma = gamma + "1"
else:
    gamma = gamma + "0"
if bin11 >= 500:
    gamma = gamma + "1"
else:
    gamma = gamma + "0"
if bin12 >= 500:
    gamma = gamma + "1"
else:
    gamma = gamma + "0"

iteration = 0
for char in gamma:
    if gamma[iteration] == "1":
        epsilon = epsilon + "0"
    else:
        epsilon = epsilon +"1"
    iteration += 1

print("Gamma rate: " + gamma)
print("Epsilon rate: " + epsilon)

decimal_gamma = int(gamma,2)
decimal_epsilon = int(epsilon,2)

print("Gamma rate in decimal: " + str(decimal_gamma))
print("Epsilon rate in decimal: " + str(decimal_epsilon))

power_consumption = decimal_epsilon * decimal_gamma

print("Power Consumption: " + str(power_consumption))