# Open file containing the depth measurements for reading
file1 = open("boards.txt", "r")

# Read the measurements from the file, and add them to a list
boards = file1.readlines()

# Close the file again, it's no longer needed
file1.close()

# Open file containing the depth measurements for reading
file2 = open("drawing.txt", "r")

# Read the measurements from the file, and add them to a list
draw_numbers = file2.read()

# Close the file again, it's no longer needed
file2.close()

split_draw_numbers = draw_numbers.split(str(","))
matrix = list()
highest_board_number_of_draws = 0
winning_board = 0
board_is_checked = False
boards_checked = 0
winning_board_matrix = list()
last_drawn_number = 0

for row in boards:
    if len(row) == 1:
        boards_checked += 1
        numbers_drawn = 0
        for number in split_draw_numbers:
            if board_is_checked == True:
                break
            numbers_drawn += 1
            for x in range(5):
                for y in range(5):
                    cell = matrix[x][y]
                    if cell == number:
                        matrix[x][y] = cell + "*"
            for x in range(5):
                number_of_stars = 0
                for y in range(5):
                    cell = str(matrix[x][y])
                    if "*" in cell:
                        number_of_stars += 1
                if number_of_stars == 5:
                    board_is_checked = True
                    if numbers_drawn > highest_board_number_of_draws:
                        highest_board_number_of_draws = numbers_drawn
                        winning_board = boards_checked
                        winning_board_matrix = matrix.copy()
                        last_drawn_number = number
                        break
            for y in range(5):
                number_of_stars = 0
                for x in range(5):
                    cell = str(matrix[x][y])
                    if "*" in cell:
                        number_of_stars += 1
                if number_of_stars == 5:
                    board_is_checked = True
                    if numbers_drawn > highest_board_number_of_draws:
                        highest_board_number_of_draws = numbers_drawn
                        winning_board = boards_checked
                        winning_board_matrix = matrix.copy()
                        last_drawn_number = number
                        break
        matrix.clear()
        board_is_checked = False
    else:
        split_row = row.split()
        matrix.append(split_row)

print("Winning Board: " + str(winning_board))
for y in range(5):
    print(winning_board_matrix[y])

winning_score = 0
for x in range(5):
    for y in range(5):
        cell = winning_board_matrix[x][y]
        if "*" not in cell:
            winning_score += int(cell)

print("Winning score: " + str(winning_score))
print("Last number drawn: " + str(last_drawn_number))

solution = int(winning_score) * int(last_drawn_number)
print("Solution: " + str(solution))