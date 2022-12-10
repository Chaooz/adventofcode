#
# Library for Advent of Code solutions
# https://adventofcode.com/
#
import time

# print("\033[0;37;40m Normal text\n")
# print("\033[2;37;40m Underlined text\033[0;37;40m \n")
# print("\033[1;37;40m Bright Colour\033[0;37;40m \n")
# print("\033[3;37;40m Negative Colour\033[0;37;40m \n")
# print("\033[5;37;40m Negative Colour\033[0;37;40m\n")
 
# print("\033[1;37;40m \033[2;37:40m TextColour BlackBackground          TextColour GreyBackground                WhiteText ColouredBackground\033[0;37;40m\n")
# print("\033[1;30;40m Dark Gray      \033[0m 1;30;40m            \033[0;30;47m Black      \033[0m 0;30;47m               \033[0;37;41m Black      \033[0m 0;37;41m")
# print("\033[1;31;40m Bright Red     \033[0m 1;31;40m            \033[0;31;47m Red        \033[0m 0;31;47m               \033[0;37;42m Black      \033[0m 0;37;42m")
# print("\033[1;32;40m Bright Green   \033[0m 1;32;40m            \033[0;32;47m Green      \033[0m 0;32;47m               \033[0;37;43m Black      \033[0m 0;37;43m")
# print("\033[1;33;40m Yellow         \033[0m 1;33;40m            \033[0;33;47m Brown      \033[0m 0;33;47m               \033[0;37;44m Black      \033[0m 0;37;44m")
# print("\033[1;34;40m Bright Blue    \033[0m 1;34;40m            \033[0;34;47m Blue       \033[0m 0;34;47m               \033[0;37;45m Black      \033[0m 0;37;45m")
# print("\033[1;35;40m Bright Magenta \033[0m 1;35;40m            \033[0;35;47m Magenta    \033[0m 0;35;47m               \033[0;37;46m Black      \033[0m 0;37;46m")
# print("\033[1;36;40m Bright Cyan    \033[0m 1;36;40m            \033[0;36;47m Cyan       \033[0m 0;36;47m               \033[0;37;47m Black      \033[0m 0;37;47m")
# print("\033[1;37;40m White          \033[0m 1;37;40m            \033[0;37;40m Light Grey \033[0m 0;37;40m               \033[0;37;48m Black      \033[0m 0;37;48m")
class bcolors:
    RESET = '\033[39m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DARK_GREY = '\033[1;30;40m'
    WHITE = '\033[1;37;40m'
    YELLOW = '\033[1;33;40m'


def loadfile(filename):
    file = open(filename)
    lines = file.readlines()
    file.close()
    return lines

def point_to_str(text,point):
    return text + str(point[0]) + "x" + str(point[1])

def string_highlight(string,highlight, color):
    new_text = color + highlight + bcolors.RESET
    return string.replace(highlight, new_text,1)


def print_tree_list(spacer, tree_list : list):
    for line in tree_list:
        if isinstance(line,list):
#            print("Tree1:" + spacer + str(line))
            print("Tree1:" + spacer + "T")
            if spacer =="":
                spacer = "+"
            print_tree_list( spacer + "-", line)
        elif isinstance(line,str):
            print("Tree2:" + spacer + " " + line)
        else:
            print("Tree3:" + spacer + " " + str(line))
#    print ("")

def pad_number(number,pad):
    num_str = str(number)
    l = len(pad)
    l2 = l - len(num_str)
    if ( l2 > 0 ):
        for i in range(0,l2):
            num_str = pad[l2-i-1] + num_str
    return num_str

def unittest( func, expected, filename ):
    st = time.time()
    code_result = func(filename)
    et = time.time()
    strTime = " (execution time:" + str(round(et-st,2)) + ")"

    if code_result == expected:
        print_ok("Unittest " + func.__name__ + " with " + str(code_result) + " is OK! input:" + str(filename) + strTime)
    else:
        print_error("Unittest " + func.__name__ + " with " + str(code_result) + " is NOT OK!  Expected:" + str(expected) + " input:" + str(filename) + strTime)

def unittest_list( func, expected, filename ):
    st = time.time()
    code_result = func(filename)
    et = time.time()
    strTime = " (execution time:" + str(round(et-st,2)) + ")"

    s_result = listToString(code_result)
    s_input = listToString(filename)
    if code_result == expected:
        print_ok("Unittest " + func.__name__ + " with " + str(s_result) + " is OK! input:" + s_input + strTime)
    else:
        print_error("Unittest " + func.__name__ + " with " + str(s_result) + " is NOT OK! Got:" + str(s_result) + " Expected:" + str(expected) + " input:" + s_input + strTime)



def unittest_input( func, input, expected, filename ):

    st = time.time()
    code_result = func(filename, input)
    et = time.time()
    strTime = " (execution time:" + str(round(et-st,2)) + ")"

    if code_result == expected:
        print_ok("Unittest " + func.__name__ + "(" + str(input) + ") with " + str(code_result) + " is OK! input:" + filename + strTime)
    else:
        print_error("Unittest " + func.__name__ + "(" + str(input) + ") with " + str(code_result) + " is NOT OK! Got:" + str(code_result) + " Expected:" + str(expected) + " input:" + filename + strTime)

def print_assert(value,text):
    if not value:
        print(bcolors.FAIL + "[ASSERT]  " + text + bcolors.RESET)
        assert False

def print_error(text):
    print(bcolors.WARNING + "[ERROR]   " + text + bcolors.RESET)

def print_warning(text):
    print(bcolors.WARNING + "[WARNING] " + text + bcolors.RESET)

def print_ok(text):
    print(bcolors.OKGREEN + "[OK]      " + text + bcolors.RESET)

def print_color(text,color):
    print(color + "          " + text + bcolors.RESET)

def print_debug(text):
    print(text)
    pass

