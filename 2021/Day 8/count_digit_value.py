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
output_display = list()
output_message = list()
for tuple in tuple_list:
    output_message.append(tuple[0])
    output_display.append(tuple[1])

# Split the output list into a list of individual words
output_display_number_list = list()
for string in output_display:
    string = string.strip("\n")
    string = string.lstrip()
    string = string.rstrip()
    output_display_number_list.append(string)

output_message_list = list()
for string in output_message:
    string = string.strip("\n")
    string = string.lstrip()
    string = string.rstrip()
    output_message_list.append(string)

#
# Go through all characters in small_number, f.ex 1 ..which is AB
#
def small_number_present_in_big_number(big_number, small_number):
    for char in small_number:
        if not char in big_number:
            return False
    return True


# Map words to numbers
iterations = 0
total_sum = 0

for line in output_message_list:
    number = str()
    one = str()
    two = str()
    three = str()
    four = str()
    five = str()
    six = str()
    seven = str()
    eight = str()
    nine = str()
    zero = str()
    unknown_word = list()

    # Hente ut unike
    word_line = line.split(" ")
    for word in word_line:
        if len(word) == 2:
            one = sorted(word)
        elif len(word) == 3:
            seven = sorted(word)
        elif len(word) == 4:
            four = sorted(word)
        elif len(word) == 7:
            eight = sorted(word)

    # De uten avhengigheter    
    for word in word_line:
        if small_number_present_in_big_number(word, one):
            if len(word) == 5:
                three = sorted(word)
            elif len(word) == 6:
                if small_number_present_in_big_number(word,four):
                    nine = sorted(word)
                else:
                    zero = sorted(word)
        elif len(word) == 6:
            six = sorted(word)
        else:
            unknown_word.append(word)

    # De med avhengigheter
    for word in unknown_word:
        if small_number_present_in_big_number(six, word):
            five = sorted(word)
        else:
            two = sorted(word)
    ## print (one + "-" + two + "-" +  three + "-" + four + "-" + five + "-" + six + "-" + seven + "-" + eight + "-" + nine + "-" + zero)

    digit_string = str()
    word_line = output_display_number_list[iterations].split(" ")
    for word in word_line:
        word = sorted(word)
        if word == one:
            digit_string += "1"
        elif word == two:
            digit_string += "2"
        elif word == three:
            digit_string += "3"
        elif word == four:
            digit_string += "4"
        elif word == five:
            digit_string += "5"
        elif word == six:
            digit_string += "6"
        elif word == seven:
            digit_string += "7"
        elif word == eight:
            digit_string += "8"
        elif word == nine:
            digit_string += "9"
        elif word == zero:
            digit_string += "0"
        else:
            print("Unknown number found - Something has epically failed!")
            break
    #print(digit_string)
    total_sum += (int(digit_string))
    iterations += 1

print("The total of all the numbers on the 4 digit panel is: " + str(total_sum))
print("Thank you, and good night.")