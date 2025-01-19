import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from all_days import day06


def test_sets():
    return [
        {
            'number': 1,
            'input': {'Time': [7, 15, 30], 'Distance': [9, 40, 200]},
            'expected1': 288
        },
        {
            'number': 2,
            'input': {'Time': [71530], 'Distance': [940200]},
            'expected1': 71503
        },

    ]


def test_first_star(test_data, expected):
    solution = day06.global_score(test_data)
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
        else:
            print("Error, the star must be 1 or 2.")


if __name__ == '__main__':
    main()
