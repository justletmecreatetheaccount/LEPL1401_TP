# Solution to mission 1
# Theo Daron. September 26th 2022

max_index = 10

current_index = 1
while current_index <= max_index:
    square = current_index ** 2 # Computing current index square
    previous_squares_sum = 0
    previous_index = 1
    while previous_index <= current_index: # Iterating over all previous numbers (with the current one included) to sum every square.
        previous_squares_sum = previous_squares_sum + previous_index**2
        previous_index = previous_index + 1
    
    second_way_sum = current_index*(current_index+1)*(2*current_index + 1) // 6
        
        
    print(current_index, "\t", square, "\t", previous_squares_sum, "\t", second_way_sum) # Print every column one by one
    current_index = current_index + 1

"""
I did this code using only stuff we had seen during the lesson, here's things i could use to optimize the lisibility and the speed.

POSSIBLE IMPROVEMENTS (you can find my improved code into mise_en_route_IMPROVED.py)
---------------------
- To improve the speed, we can cache every square into a list (or a dictionnary) to avoid to re-compute them in every iteration
- For loop might be a better option for lisibility over while.
- Use sum function to avoid nested while and get more lisibility ( go in pair with list usage )
"""