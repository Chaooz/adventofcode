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
        list = substring.split()
        for chars in list:
            output_word_list.append(chars)

# Count the number of strings in the list that are 2, 3, 4 and 7 chars long
unique_chars = 0
for word in output_word_list:
    if len(word) == 2 or len(word) == 3 or len(word) == 4 or len(word) == 7:
        unique_chars += 1

print("Unique digits appear " + str(unique_chars) + " times")