# Day 8: Haunted Wasteland

# First star: It seems like you're meant to use the left/right instructions to navigate the network. After examining the
# maps for a bit, two nodes stick out: AAA and ZZZ. You feel like AAA is where you are now, and you have to follow the
# left/right instructions until you reach ZZZ.
# This format defines each node of the network individually.
# Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?

# Second star: Simultaneously start on every node that ends with A. How many steps does it take before you're only on
# nodes that end with Z?

import os
import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from numpy import lcm
from AoC_tools.read_data import read_data


def parse_instructions(data):
    directions = data[0][0]
    nodes = {line[:3]: {'L': line[7:10], 'R': line[12:15]} for line in data[1]}
    return directions, nodes


def count_steps(data):
    directions, nodes = parse_instructions(data)
    nb_dir = len(directions)
    n, node = 0, 'AAA'
    while node != 'ZZZ':
        node = nodes[node][directions[n % nb_dir]]
        n += 1
    return n


def count_ghost_steps(data):
    directions, all_nodes = parse_instructions(data)
    nb_dir = len(directions)
    nodes = [node for node in all_nodes.keys() if node[-1] == 'A']
    steps_for_all_nodes = 1
    for node in nodes:
        print(node)
        n = 0
        while node[-1] != 'Z':
            node = all_nodes[node][directions[n % nb_dir]]
            n += 1
        steps_for_all_nodes = lcm(steps_for_all_nodes, n)
        print(f'--- {n} ---')
    return steps_for_all_nodes


def run(data_dir, star):
    data = read_data(f'{data_dir}/input-day08.txt', by_block=True, numbers=False)

    if star == 1:  # The final answer is: 13207
        solution = count_steps(data)
    elif star == 2:  # The final answer is: 12324145107121
        solution = count_ghost_steps(data)
    else:
        raise Exception('Star number must be either 1 or 2.')

    print(f'The solution (star {star}) is: {solution}')
    return solution
