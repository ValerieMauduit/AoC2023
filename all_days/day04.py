# Day 4: Scratchcards

# First star: The Elf leads you over to the pile of colorful cards. There, you discover dozens of scratchcards, all with
# their opaque covering already scratched off. Picking one up, it looks like each card has two lists of numbers
# separated by a vertical bar (|): a list of winning numbers and then a list of numbers you have. You organize the
# information into a table (your puzzle input).
# As far as the Elf has been able to figure out, you have to figure out which of the numbers you have appear in the list
# of winning numbers. The first match makes the card worth one point and each match after the first doubles the point
# value of that card.
# Take a seat in the large pile of colorful cards. How many points are they worth in total?

# Second star: There's no such thing as "points". Instead, scratchcards only cause you to win more scratchcards equal to
# the number of winning numbers you have.
# Specifically, you win copies of the scratchcards below the winning card equal to the number of matches. So, if card 10
# were to have 5 matching numbers, you would win one copy each of cards 11, 12, 13, 14, and 15.
# Copies of scratchcards are scored like normal scratchcards and have the same card number as the card they copied. So,
# if you win a copy of card 10 and it has 5 matching numbers, it would then win a copy of the same cards that the
# original card 10 won: cards 11, 12, 13, 14, and 15. This process repeats until none of the copies cause you to win any
# more cards. (Cards will never make you copy a card past the end of the table.)
# Process all of the original and copied scratchcards until no more scratchcards are won. Including the original set of
# scratchcards, how many total scratchcards do you end up with?


import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from AoC_tools.read_data import read_data


def parse_card(line):
    values = line.split(': ')[1]
    cards = values.split(' | ')
    winning_cards = [int(c) for c in cards[0].split()]
    hand_cards = [int(c) for c in cards[1].split()]
    return winning_cards, hand_cards


def total_points(data):
    score = 0
    for card in data:
        winning, having = parse_card(card)
        appearing_cards = [c for c in having if c in winning]
        if len(appearing_cards) > 0:
            score += 2 ** (len(appearing_cards) - 1)
    return score


def total_scratch_cards(data):
    scratch_cards = {v: 1 for v in range(1, len(data) + 1)}
    n = 0
    for card in data:
        n += 1
        winning, having = parse_card(card)
        appearing_cards = [c for c in having if c in winning]
        for c in range(n + 1, n + 1 + len(appearing_cards)):
            scratch_cards[c] += scratch_cards[n]
    return sum(scratch_cards.values())


def run(data_dir, star):
    data = read_data(f'{data_dir}/input-day04.txt', numbers=False)

    if star == 1:  # The final answer is: 21213
        solution = total_points(data)
    elif star == 2:  # The final answer is: 8549735
        solution = total_scratch_cards(data)
    else:
        raise Exception('Star number must be either 1 or 2.')

    print(f'The solution (star {star}) is: {solution}')
    return solution
