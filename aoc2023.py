#! /usr/bin/env python
import argparse
import sys
sys.path.append("./all_days")


imports = [f'day{n:02.0f}' for n in range(1, 26)]
modules = {}
for x in imports:
    try:
        modules[x] = __import__(x)
        # print(f"Successfully imported {x}.")
    except ImportError:
        error = True
        # print(f"Error importing {x}.")


def main():
    parser = argparse.ArgumentParser(description="Advent of Code 2023")
    parser.add_argument("--day", type=int, help="Puzzle day")
    parser.add_argument("--star", type=int, help="Puzzle star")
    parser.add_argument('--dir', type=str, help='Input data directory')
    args = parser.parse_args()
    modules[f'day{args.number:02.0f}'].run(args.dir, args.star)


if __name__ == "__main__":
    main()
