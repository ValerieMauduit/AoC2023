# Day 3: Gear Ratios

# First star: If you can add up all the part numbers in the engine schematic, it should be easy to work out which part
# is missing.
# The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers
# and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part
# number" and should be included in your sum. (Periods (.) do not count as a symbol.)
# What is the sum of all of the part numbers in the engine schematic?

# Second star: The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol
# that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.
# This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which
# gear needs to be replaced.
# What is the sum of all of the gear ratios in your engine schematic?

import os
import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import re

from AoC_tools.read_data import read_data
from AoC_tools.work_with_dicts import update_dict
from AoC_tools.work_with_maps import AocMap


def engine_parts(data):
    engine_ids = {}
    n = 0
    for line in data:
        for match in re.finditer('[0-9]+', line):
            # Caution: the span is the start and the end values (not the start and the length as I thought)
            engine_ids = update_dict(engine_ids, int(match.group()), [[n, match.span()]], cumulative=True)

        n += 1
    return engine_ids


def symbols(data):
    symbol_positions = []
    n = 0
    for line in data:
        symbol_positions += [(n, match.span()[0]) for match in re.finditer('[^0-9.]+', line)]
        n += 1
    return symbol_positions


def get_valid_parts_sum(data):
    engine_ids = engine_parts(data)
    symbol_pos = symbols(data)
    result = 0
    for part_id, positions in engine_ids.items():
        for pos in positions:
            neighbours = (
                    [(pos[0] - 1, c) for c in range(pos[1][0] - 1, pos[1][1] + 1)]
                    + [(pos[0] + 1, c) for c in range(pos[1][0] - 1, pos[1][1] + 1)]
                    + [(pos[0], pos[1][0] - 1), (pos[0], pos[1][1])]
            )
            if any([n in symbol_pos for n in neighbours]):
                result += part_id
    return result


def get_gear_ratio_sum(data):
    gear_ratio_sum = 0
    engine_map = AocMap(data)
    possible_gears = engine_map.get_marker_coords('*')
    for gear_pos in possible_gears:
        engine_map.set_position(gear_pos)
        neighbours_pos = engine_map.get_neighbours_coordinates(diagonals=True)
        gear_parts = []
        for n_pos in neighbours_pos:
            p = n_pos[0]
            value = engine_map.get_point([p, n_pos[1]])
            # Get the digits to the left
            part_id = ''
            while (p >= 0) and (value in '0123456789'):
                part_id = engine_map.get_point([p, n_pos[1]]) + part_id
                p = p - 1
                value = engine_map.get_point([p, n_pos[1]])
            if len(part_id) > 0:
                # Get the digits to the right
                p = n_pos[0] + 1
                value = engine_map.get_point([p, n_pos[1]])
                while (p < engine_map.width) and (value in '0123456789'):
                    part_id = part_id + engine_map.get_point([p, n_pos[1]])
                    p = p + 1
                    value = engine_map.get_point([p, n_pos[1]])
                # Add the part id to the gear
                gear_parts += [int(part_id)]
        # If 2 parts, add the gear ratio
        gear_parts = list(set(gear_parts))
        if len(gear_parts) == 2:
            gear_ratio_sum += gear_parts[0] * gear_parts[1]
    return gear_ratio_sum


def run(data_dir, star):
    data = read_data(f'{data_dir}/input-day03.txt', numbers=False)

    if star == 1:  # The final answer is: 528799
        # I can have twice the same number, I must add up the parts with the same id
        solution = get_valid_parts_sum(data)
    elif star == 2:  # The final answer is: 84907174
        # I am ashamed because it didn't work with my last columns (when there is a digit in the last column) so I added
        # a column of dots to make it work
        solution = get_gear_ratio_sum(data)
    else:
        raise Exception('Star number must be either 1 or 2.')

    print(f'The solution (star {star}) is: {solution}')
    return solution
