# Day02: Cube Conundrum

# First star: You play several games and record the information from each game (your puzzle input). Each game is listed
# with its ID number (like the 11 in Game 11: ...) followed by a semicolon-separated list of subsets of cubes that were
# revealed from the bag (like 3 red, 5 green, 4 blue).
# Determine which games would have been possible if the bag had been loaded with only 12 red cubes, 13 green cubes, and
# 14 blue cubes. What is the sum of the IDs of those games?

# Second star: As you continue your walk, the Elf poses a second question: in each game you played, what is the fewest
# number of cubes of each color that could have been in the bag to make the game possible?
# The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together.
# For each game, find the minimum set of cubes that must have been present. What is the sum of the power of these sets?

import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from AoC_tools.read_data import read_data


def parse_games(data):
    result = {}
    for k, v in data.items():
        game_id = int(k.split(' ')[1])
        games = v.split('; ')
        game_summary = []
        for game in games:
            local = {}
            blocks = game.split(', ')
            for block in blocks:
                cubes = block.split(' ')
                local[cubes[1]] = int(cubes[0])
            game_summary += [local]
        result[game_id] = game_summary
    return result


def possible_games(data, red=12, green=13, blue=14):
    games = parse_games(data)
    result = 0
    for k, v in games.items():
        if (
                (max([g['blue'] for g in v if 'blue' in g.keys()]) <= blue)
                and (max([g['red'] for g in v if 'red' in g.keys()]) <= red)
                and (max([g['green'] for g in v if 'green' in g.keys()]) <= green)
        ):
            result += k
    return result


def minimum_cubes(data):
    games = parse_games(data)
    result = 0
    for k, v in games.items():
        result += (
                max([g['blue'] for g in v if 'blue' in g.keys()] + [1])
                * max([g['red'] for g in v if 'red' in g.keys()] + [1])
                * max([g['green'] for g in v if 'green' in g.keys()] + [1])
        )
    return result


def run(data_dir, star):
    data = {line[0]: line[1] for line in read_data(f'{data_dir}/input-day02.txt', numbers=False, split=': ')}

    if star == 1:  # The final answer is:
        solution = possible_games(data)
    elif star == 2:  # The final answer is:
        solution = minimum_cubes(data)
    else:
        raise Exception('Star number must be either 1 or 2.')

    print(f'The solution (star {star}) is: {solution}')
    return solution
