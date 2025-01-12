import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from all_days import day02


def test_sets():
    return [
        {
            'number': 1,
            'input': {
                'Game 1': '3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green',
                'Game 2': '1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue',
                'Game 3': '8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red',
                'Game 4': '1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red',
                'Game 5': '6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'
            }
            ,
            'expected1': 8,
            'expected2': 2286
        },
    ]


def test_first_star(test_data, expected):
    solution = day02.possible_games(test_data)
    if solution != expected:
        print("Your output is:")
        print(solution)
        raise Exception(f'This is not the solution, you should get {expected}')
    print('--- Test OK')


def test_second_star(test_data, expected):
    solution = day02.minimum_cubes(test_data)
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
