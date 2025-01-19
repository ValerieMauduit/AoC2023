# Day 6: Wait For It

# First star: As part of signing up, you get a sheet of paper (your puzzle input) that lists the time allowed for each
# race and also the best distance ever recorded in that race. To guarantee you win the grand prize, you need to make
# sure you go farther in each race than the current record holder.
# The boats are much smaller than you expected - they're actually toy boats, each with a big button on top. Holding
# down the button charges the boat, and releasing the button allows the boat to move. Boats move faster if their button
# was held longer, but time spent holding the button counts against the total race time. You can only hold the button at
# the start of the race, and boats don't move until the button is released.
# Your toy boat has a starting speed of zero millimeters per millisecond. For each whole millisecond you spend at the
# beginning of the race holding down the button, the boat's speed increases by one millimeter per millisecond.
# Determine the number of ways you could beat the record in each race. What do you get if you multiply these numbers
# together?

# Second star: As the race is about to start, you realize the piece of paper with race times and record distances you
# got earlier actually just has very bad kerning. There's really only one race - ignore the spaces between the numbers
# on each line.
# How many ways can you beat the record in this one much longer race?

import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import math


def race_score(time, distance):
    print('-' * 42)
    discriminant = time * time - 4 * distance
    x1, x2 = math.floor((time - math.sqrt(discriminant)) / 2 + 1), math.ceil((time + math.sqrt(discriminant)) / 2 - 1)
    print(f'allowed time: {time}')
    print(f'winning from {x1} to {x2}')
    return len(range(x1, x2)) + 1


def global_score(data):
    score = 1
    for time, distance in zip(data['Time'], data['Distance']):
        score = score * race_score(time, distance)
    return score


def run(data_dir, star):
    data = {'Time': [48, 93, 84, 66], 'Distance': [261, 1192, 1019, 1063]}
    data2 = {'Time': [48938466], 'Distance': [261119210191063]}

    if star == 1:  # The final answer is: 1312850
        solution = global_score(data)
    elif star == 2:  # The final answer is: 36749103
        solution = global_score(data2)
    else:
        raise Exception('Star number must be either 1 or 2.')

    print(f'The solution (star {star}) is: {solution}')
    return solution
