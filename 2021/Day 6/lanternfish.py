from time import time

def loadfile(filename):
    file = open(filename)
    lines = file.read()
    file.close()
    return lines

number_of_days = 256

# Create list of fishies with corresponding TTS (Time to spawn)
fishie_string = loadfile("fishies.txt")
fishie_list = fishie_string.split(",")
fishies = list()
for fishie in fishie_list:
    fishies.append(int(fishie))

age0 = 0
age1 = 0
age2 = 0
age3 = 0
age4 = 0
age5 = 0
age6 = 0
age7 = 0
age8 = 0

for fishie in fishies:
    if fishie == 1:
        age1 += 1
    elif fishie == 2:
        age2 += 1
    elif fishie == 3:
        age3 += 1
    elif fishie == 4:
        age4 += 1
    elif fishie == 5:
        age5 += 1

# Loop through fishies, updating TTS and counting the number of new fishies

while number_of_days != 0:
    new_fishies = age0
    age0 = age1
    age1 = age2
    age2 = age3
    age3 = age4
    age4 = age5
    age5 = age6
    age6 = age7 + new_fishies
    age7 = age8
    age8 = new_fishies
    number_of_days -= 1

end_fishies = age0 + age1 + age2 + age3 + age4 + age5 + age6 + age7 + age8
print("Number of fishes after 256 days: " + str(end_fishies))


