def loadfile(filename):
    file = open(filename)
    lines = file.readlines()
    file.close()
    return lines

def getCharScore(char):
    if char == ")":
        score = 3
    elif char == "]":
        score = 57
    elif char == "}":
        score = 1197
    elif char == ">":
        score = 25137
    else:
        score = 0
    return score

def checkCharMatch(startChar, endChar):
    if startChar == "(" and endChar == ")":
        return True
    elif startChar == "[" and endChar == "]":
        return True
    elif startChar == "<" and endChar == ">":
        return True
    elif startChar == "{" and endChar == "}":
        return True
    else:
        return False

counter = 0
total_score = 0

def checkChar(line):
    global counter
    global total_score

    while counter <= len(line):
    
        startChar = line[counter]
        counter += 1
        if startChar == "(" or startChar == "{" or startChar == "[" or startChar == "<":
            endChar = checkChar(line)
            if not checkCharMatch(startChar, endChar):
                score = getCharScore(endChar)
                total_score += score
                return "-"
        else:
            return startChar
    
    return "-"

def checkLines(filename):
    global counter
    lines = loadfile(filename)

    for line in lines:
        counter = 0
        checkChar(line)

checkLines("nav_subsystem.txt")
print("Total score is " + str(total_score))