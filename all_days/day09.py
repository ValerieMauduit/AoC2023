# Day 9: Mirage Maintenance

# First star: The OASIS produces a report of many values and how they are changing over time (your puzzle input). Each
# line in the report contains the history of a single value.
# To best protect the oasis, your environmental report should include a prediction of the next value in each history. To
# do this, start by making a new sequence from the difference at each step of your history. If that sequence is not all
# zeroes, repeat this process, using the sequence you just generated as the input sequence. Once all of the values in
# your latest sequence are zeroes, you can extrapolate what the next value of the original history should be.
# Analyze your OASIS report and extrapolate the next value for each history. What is the sum of these extrapolated
# values?

# Second star: Analyze your OASIS report again, this time extrapolating the previous value for each history. What is the
# sum of these extrapolated values?

import os
import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from AoC_tools.read_data import read_data


def extrapolated_value(line):
    if all([x == 0 for x in line]):
        return 0
    else:
        return line[-1] + extrapolated_value([line[n + 1] - line[n] for n in range(len(line) - 1)])


def previous_value(line):
    if all([x == 0 for x in line]):
        return 0
    else:
        return line[0] - previous_value([line[n + 1] - line[n] for n in range(len(line) - 1)])


def score(data, future=True):
    scores = []
    for oasis in data:
        oasis = [int(x) for x in oasis]
        if future:
            scores += [extrapolated_value(oasis)]
        else:
            scores += [previous_value(oasis)]
    return sum(scores)


def run(data_dir, star):
    data = read_data(f'{data_dir}/input-day09.txt', numbers=True, split=' ')

    if star == 1:  # The final answer is: 1641934234
        solution = score(data)
    elif star == 2:  # The final answer is: 975
        solution = score(data, future=False)
    else:
        raise Exception('Star number must be either 1 or 2.')

    print(f'The solution (star {star}) is: {solution}')
    return solution
