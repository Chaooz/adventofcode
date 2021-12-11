def loadfile(filename):
    file = open(filename)
    lines = file.readlines()
    file.close()
    return lines

# Read txt-file into a list of strings
string_list = loadfile("signal_list.txt")

# Split the strings using the | as the delimiter. Store each string 
# in a tuple containing each of the 2 substrings. Add the tuple to 
# a list.
tuple_list = list()
for line in string_list:
    new_tuple = tuple(line.split("|"))
    tuple_list.append(new_tuple)

# Save the portion after | to a new list
output_list = list()
for tuple in tuple_list:
    output_list.append(tuple[1])

# Split the output list into a list of individual words
output_word_list = list()
for string in output_list:
    string = string.strip("\n")
    string = string.split(",")
    for substring in string:
        output_word_list.append(substring)

print(output_word_list)

# Count the number of strings in the list that are 2, 3, 4 and 7 chars long
#digit_total = 0
#for word in output_word_list:
#    if word == "ab":
#        digit_total += 1
#    elif word == "gcdfa":
#        digit_total += 2
#    elif word == "fbcad":
#        digit_total += 3
#    elif word == "eafb":
#        digit_total += 4
#    elif word == "cdfbe":
#        digit_total += 5
#    elif word == "cdfgeb":
#        digit_total += 6
#    elif word == "dab":
#        digit_total += 7
#    elif word == "acedgfb":
#        digit_total += 8
#    else:
#        digit_total += 9
#    print(digit_total)
    
#print("Sum of digits: " + str(digit_total))