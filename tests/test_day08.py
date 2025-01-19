import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from all_days import day08


def test_sets():
    return [
        {
            'number': 1,
            'input': [
                ['RL'],
                [
                    'AAA = (BBB, CCC)', 'BBB = (DDD, EEE)', 'CCC = (ZZZ, GGG)', 'DDD = (DDD, DDD)', 'EEE = (EEE, EEE)',
                    'GGG = (GGG, GGG)', 'ZZZ = (ZZZ, ZZZ)'
                ]
            ],
            'expected1': 2,
            'expected2': 2
        },
        {
            'number': 2,
            'input': [['LLR'], ['AAA = (BBB, BBB)', 'BBB = (AAA, ZZZ)', 'ZZZ = (ZZZ, ZZZ)']],
            'expected1': 6,
            'expected2': 6
        },
        {
            'number': 3,
            'input': [
                ['LR'],
                [
                    '11A = (11B, XXX)', '11B = (XXX, 11Z)', '11Z = (11B, XXX)', '22A = (22B, XXX)', '22B = (22C, 22C)',
                    '22C = (22Z, 22Z)', '22Z = (22B, 22B)', 'XXX = (XXX, XXX)'
                ]
            ],
            'expected1': None,
            'expected2': 6
        },
    ]


def test_first_star(test_data, expected):
    solution = day08.count_steps(test_data)
    if solution != expected:
        print("Your output is:")
        print(solution)
        raise Exception(f'This is not the solution, you should get {expected}')
    print('--- Test OK')


def test_second_star(test_data, expected):
    solution = day08.count_ghost_steps(test_data)
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
            if test['number'] < 3:
                test_first_star(test['input'], test['expected1'])
        elif test_case == 2:
            test_second_star(test['input'], test['expected2'])
        else:
            print("Error, the star must be 1 or 2.")


if __name__ == '__main__':
    main()
