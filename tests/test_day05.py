import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from all_days import day05


def test_sets():
    return [
        {
            'number': 1,
            'input': [
                ['seeds: 79 14 55 13'],
                ['seed-to-soil map:', '50 98 2', '52 50 48'],
                ['soil-to-fertilizer map:', '0 15 37', '37 52 2', '39 0 15'],
                ['fertilizer-to-water map:', '49 53 8', '0 11 42', '42 0 7', '57 7 4'],
                ['water-to-light map:', '88 18 7', '18 25 70'],
                ['light-to-temperature map:', '45 77 23', '81 45 19', '68 64 13'],
                ['temperature-to-humidity map:', '0 69 1', '1 0 69'],
                ['humidity-to-location map:', '60 56 37', '56 93 4']
            ],
            'expected1': 35,
            'expected2': 46
        },
    ]


def test_first_star(test_data, expected):
    solution = day05.lowest_location(test_data)
    if solution != expected:
        print("Your output is:")
        print(solution)
        raise Exception(f'This is not the solution, you should get {expected}')
    print('--- Test OK')


def test_second_star(test_data, expected):
    solution = day05.lowest_location_for_ranges(test_data)
    if solution != expected:
        print("Your output is:")
        print(solution)
        raise Exception(f'This is not the solution, you should get {expected}')
    print('--- Test OK')


def main():
    test_case = int(input('Which star to test? '))
    for test in test_sets():
        print(f"=== Test #{test['number']} ===")
        if test_case == 1:
            test_first_star(test['input'], test['expected1'])
        elif test_case == 2:
            test_second_star(test['input'], test['expected2'])
        else:
            print("Error, the star must be 1 or 2.")


if __name__ == '__main__':
    main()
