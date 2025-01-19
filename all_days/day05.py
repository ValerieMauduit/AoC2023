# Day 5: If You Give A Seed A Fertilizer

# First star: The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists what type of
# soil to use with each kind of seed, what type of fertilizer to use with each kind of soil, what type of water to use
# with each kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is identified with a number,
# but numbers are reused by each category - that is, soil 123 and fertilizer 123 aren't necessarily related to each
# other.
# The almanac starts by listing which seeds need to be planted.
# The rest of the almanac contains a list of maps which describe how to convert numbers from a source category into
# numbers in a destination category. That is, the section that starts with seed-to-soil map: describes how to convert a
# seed number (the source) to a soil number (the destination). This lets the gardener and his team know which soil to
# use with which seeds, which water to use with which fertilizer, and so on.
# Rather than list every source number and its corresponding destination number one by one, the maps describe entire
# ranges of numbers that can be converted. Each line within a map contains three numbers: the destination range start,
# the source range start, and the range length.
# Any source numbers that aren't mapped correspond to the same destination number.
# What is the lowest location number that corresponds to any of the initial seed numbers?

# Second star: Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks
# like the seeds: line actually describes ranges of seed numbers.
# The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and
# the second value is the length of the range.
# Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest
# location number that corresponds to any of the initial seed numbers?

import os
import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import pandas as pd
from AoC_tools.read_data import read_data


def parse_almanac(data):
    seeds = [int(s) for s in data[0][0].split(': ')[1].split()]
    production_maps = {}
    for block in data[1:]:
        transformation = block[0].split()[0]
        mapping = transformation.split('-')
        translations = [[int(v) for v in l.split()] for l in block[1:]]
        sources = [t[1] for t in translations]
        sources.sort()
        formatted_translations = {0: 0}
        for source in sources:
            translation = [t for t in translations if t[1] == source][0]
            destination = translation[0]
            span = translation[2]
            if (source > 0) and (source - 1 not in formatted_translations.keys()):
                formatted_translations[source - 1] = 0
            formatted_translations[source] = destination - source
            formatted_translations[source + span - 1] = destination - source
            formatted_translations[source + span] = 0
        production_maps[mapping[0]] = {'to': mapping[2], 'transformation': formatted_translations}
    return seeds, production_maps


def get_next_value(value, translation_map):
    mapping_values = [k for k in translation_map.keys() if k >= value]
    if len(mapping_values) > 0:
        mapping_value = min(mapping_values)
        return value + translation_map[mapping_value]
    return value


def get_location_value(seed, translation_maps):
    category, value = 'seed', seed
    while category != 'location':
        value = get_next_value(value, translation_maps[category]['transformation'])
        category = translation_maps[category]['to']
    return value


def lowest_location(data):
    seeds, production_maps = parse_almanac(data)
    locations = [get_location_value(seed, production_maps) for seed in seeds]
    return min(locations)


def lowest_location_for_ranges(data):
    seeds, product_maps = parse_almanac(data)
    translations = ['seed', 'soil', 'fertilizer', 'water', 'light', 'temperature', 'humidity', 'location']
    df_global = pd.DataFrame({
        'seed': product_maps['seed']['transformation'].keys(),
        'se2so': product_maps['seed']['transformation'].values()
    })
    df_global['soil'] = df_global['seed'] + df_global['se2so']
    # Fill all the transformations
    for t1, t2 in zip(translations[1:-1], translations[2:]):
        print('-' * 42)
        print(t1)
        transformation = f'{t1[:2]}2{t2[:2]}'
        df_local = pd.DataFrame({
            t1: product_maps[t1]['transformation'].keys(),
            transformation: product_maps[t1]['transformation'].values()
        })
        df_global = df_global.merge(df_local, on=t1, how='outer', validate='1:1').sort_values(by=t1)
        df_global[transformation] = df_global[transformation].ffill()
        df_global[t2] = df_global[t1] + df_global[transformation]
        print(df_global.shape)
    print('=== back to seed ===')
    for t1, t2 in zip(translations[-2::-1], translations[-3::-1]):
        transformation = f'{t2[:2]}2{t1[:2]}'
        df_global = df_global.sort_values(by=t1)
        df_global[transformation] = df_global[transformation].ffill()
        df_global[t2] = df_global[t1] - df_global[transformation]
    print('=== add seed spans ===')
    seed_spans = [s + r - 1 for s, r in zip(seeds[::2], seeds[1::2])] + seeds[::2]
    seed_spans.sort()
    df_global = df_global.sort_values(by='seed')
    df_global = df_global.merge(pd.DataFrame({'seed': seed_spans}), on='seed', how='outer', validate='1:1')
    for t1, t2 in zip(translations[:-1], translations[1:]):
        transformation = f'{t1[:2]}2{t2[:2]}'
        df_global = df_global.sort_values(by=t1)
        df_global[transformation] = df_global[transformation].ffill()
        df_global[t2] = df_global[t2].fillna(df_global[t1] + df_global[transformation])
    print('=== filter of seeds spans')
    solution = pd.DataFrame()
    for s1, s2 in zip(seed_spans[::2], seed_spans[1::2]):
        solution = pd.concat([solution, df_global.loc[(df_global['seed'] >= s1) & (df_global['seed'] <= s2)]])
    return solution['location'].min()


def run(data_dir, star):
    data = read_data(f'{data_dir}/input-day05.txt', numbers=False, by_block=True)

    if star == 1:  # The final answer is: 111627841
        solution = lowest_location(data)
    elif star == 2:  # The final answer is: 69323688
        solution = lowest_location_for_ranges(data)
    else:
        raise Exception('Star number must be either 1 or 2.')

    print(f'The solution (star {star}) is: {solution}')
    return solution
