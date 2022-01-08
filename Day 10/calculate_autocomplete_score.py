counter = 0
incomplete_lines = list()
total_score = 0
scores = list()
scoringString = str()
EOL = False

def loadfile(filename):
    file = open(filename)
    lines = file.readlines()
    file.close()
    return lines

def getCharScore(char):
    if char == "(":
        score = 1
    elif char == "[":
        score = 2
    elif char == "{":
        score = 3
    elif char == "<":
        score = 4
    else:
        score = 0

    return score

def getLineScore(charList):
    lineScore = 0

    for char in charList:
        print(lineScore)
        lineScore = lineScore * 5
        print(lineScore)
        lineScore += getCharScore(char)
        print(char)
        print(lineScore)
        print("----")

    return lineScore

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

def checkChar(line):
    global counter
    global total_score
    global incomplete_lines

    while counter < len(line):
    
        startChar = line[counter]
        counter += 1
        if startChar == "(" or startChar == "{" or startChar == "[" or startChar == "<":
            endChar = checkChar(line)
            if ( endChar == "-"):
                return "-"
            if ( endChar == "\n" ):
                return "-"
            elif not checkCharMatch(startChar, endChar):
                return "-"
        else:
            return startChar
    
    incomplete_lines.append(line)
    return "-"

def checkLines(filename):
    global counter
    lines = loadfile(filename)

    for line in lines:
        line = line.rstrip()
        line = line.strip("\n")
        counter = 0
        checkChar(line)

def autocompleteChar(line):
    global counter
    global total_score
    global EOL
    global scoringString

    while counter < len(line):
    
        startChar = line[counter]
        counter += 1
        if EOL:
            return startChar

        if startChar == "(" or startChar == "{" or startChar == "[" or startChar == "<":
            endChar = autocompleteChar(line)
            if endChar == "-":
                scoringString = scoringString + startChar
                return "-"
        else:
            return startChar
    
    EOL = True
    return "-"

def completeLines(lines):
    global counter
    global total_score
    global EOL
    global scoringString

    for line in lines:
        counter = 0
        total_score = 0
        EOL = False
        scoringString = str()
        autocompleteChar(line)
        print(scoringString)
        #print(len(scoringString))
        print(line)
        scores.append(getLineScore(scoringString))

checkLines("nav_subsystem.txt")
#print(incomplete_lines)
completeLines(incomplete_lines)

print(scores)
scores.sort()
#print(scores)
final_score = scores[int(len(scores) / 2)]

print(final_score)


	
