import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from all_days import day04


def test_sets():
    return [
        {
            'number': 1,
            'input': [
                'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53', 'Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19',
                'Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1', 'Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83',
                'Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36', 'Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'
            ],
            'expected1': 13,
            'expected2': 30
        },
    ]


def test_first_star(test_data, expected):
    solution = day04.total_points(test_data)
    if solution != expected:
        print("Your output is:")
        print(solution)
        raise Exception(f'This is not the solution, you should get {expected}')
    print('--- Test OK')


def test_second_star(test_data, expected):
    solution = day04.total_scratch_cards(test_data)
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
