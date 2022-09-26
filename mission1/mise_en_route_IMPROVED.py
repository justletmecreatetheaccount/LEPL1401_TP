# Solution to mission 1
# IMPROVED Version - I'm using stuff we didn't see during the lesson
# The second way to compute sum can be found in the basic solution.
# Theo Daron. September 26th 2022

max_index = 10
    
squares = []

for number in range(1, max_index + 1):
    square = number ** 2 # Computing current index square
    squares.append(square)
    previous_squares_sum = sum(squares)
    print(number, "\t", square, "\t", previous_squares_sum) # Print every column one by one
