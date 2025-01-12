# Day00: title

# First star: description

# Second star: description

import os
import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from AoC_tools.read_data import read_data


def my_func(data):
    return data


def run(data_dir, star):
    data = read_data(f'{data_dir}/input-day00.txt')

    if star == 1:  # The final answer is:
        solution = my_func(data)
    elif star == 2:  # The final answer is:
        solution = my_func(data)
    else:
        raise Exception('Star number must be either 1 or 2.')

    print(f'The solution (star {star}) is: {solution}')
    return solution
