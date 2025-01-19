# Day 7: Camel Cards

# First star: In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of each
# hand. A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. The relative strength of
# each card follows this order, where A is the highest and 2 is the lowest.
# Every hand is exactly one type. From strongest to weakest, they are:
# - Five of a kind, where all five cards have the same label: AAAAA
# - Four of a kind, where four cards have the same label and one card has a different label: AA8AA
# - Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
# - Three of a kind, where three cards have the same label, and the remaining two cards are each different from any
#   other card in the hand: TTT98
# - Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third
#   label: 23432
# - One pair, where two cards share one label, and the other three cards have a different label from the pair and each
#   other: A23A4
# - High card, where all cards' labels are distinct: 23456
# Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.
# If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand.
# If these cards are different, the hand with the stronger first card is considered stronger. If the first card in each
# hand have the same label, however, then move on to considering the second card in each hand. If they differ, the hand
# with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the
# fifth.
# To play Camel Cards, you are given a list of hands and their corresponding bid (your puzzle input).
# Each hand wins an amount equal to its bid multiplied by its rank, where the weakest hand gets rank 1, the
# second-weakest hand gets rank 2, and so on up to the strongest hand.
# Find the rank of every hand in your set. What are the total winnings?

# Second star: To make things a little more interesting, the Elf introduces one additional rule. Now, J cards are jokers
# - wildcards that can act like whatever card would make the hand the strongest type possible.
# To balance this, J cards are now the weakest individual cards, weaker even than 2. The other cards stay in the same
# order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.
# Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?

import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import pandas as pd
from AoC_tools.read_data import read_data

CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 20
}


def rank_hands(data):
    ranked = pd.DataFrame(columns=['hand', 'bid'], data=data)
    ranked['bid'] = pd.to_numeric(ranked['bid'])
    cards = CARD_VALUES.keys()
    # Count each kind of card
    for card in cards:
        ranked[card] = ranked['hand'].apply(lambda s: s.count(card))
    # Determine the figure
    ranked['figure_score'] = 0
    ranked.loc[ranked[cards].max(axis=1) <= 1, 'figure_score'] = 1
    ranked.loc[(ranked[cards] == 2).any(axis=1), 'figure_score'] = 2
    ranked.loc[(ranked[cards] == 2).sum(axis=1) == 2, 'figure_score'] = 3
    ranked.loc[(ranked[cards] == 3).any(axis=1), 'figure_score'] = 4
    ranked.loc[(ranked[cards] == 3).any(axis=1) & (ranked[cards] == 2).any(axis=1), 'figure_score'] = 5
    ranked.loc[(ranked[cards] == 4).any(axis=1), 'figure_score'] = 6
    ranked.loc[(ranked[cards] == 5).any(axis=1), 'figure_score'] = 7
    # Value of cards by order
    for c in range(5):
        ranked[f'card{c}'] = ranked['hand'].apply(lambda x: CARD_VALUES[x[c]])
    # Score
    ranked['score'] = (
            ranked['card4'] + 100 * ranked['card3'] + 1e4 * ranked['card2'] + 1e6 * ranked['card1']
            + 1e8 * ranked['card0'] + 1e10 * ranked['figure_score']
    )
    ranked['rank'] = ranked['score'].rank()
    return ranked


def rank_with_jokers(data):
    ranked = pd.DataFrame(columns=['hand', 'bid'], data=data)
    ranked['bid'] = pd.to_numeric(ranked['bid'])
    cards = CARD_VALUES.keys()
    # Count each kind of card
    for card in cards:
        ranked[card] = ranked['hand'].apply(lambda s: s.count(card))
    # Count series of cards
    for n in range(2, 6):
        ranked[f'count{n}'] = (ranked[[c for c in cards if c != 'J']] == n).sum(axis=1)
    # Determine the figure
    ranked['figure_score'] = 0
    ranked.loc[(ranked['count2'] > 0) | (ranked['J'] > 0), 'figure_score'] = 1  # at least one pair
    ranked.loc[
        (ranked['count2'] > 1) | ((ranked['count2'] > 0) & (ranked['J'] > 1)),
        'figure_score'
    ] = 2  # at least two pairs
    ranked.loc[
        (ranked['count3'] > 0) | ((ranked['count2'] > 0) & (ranked['J'] > 0)) | (ranked['J'] > 1),
        'figure_score'
    ] = 3  # at least triple
    # ABBJJ BBJJJ
    ranked.loc[
        ((ranked['count3'] > 0) & (ranked['count2'] > 0)) | ((ranked['count3'] > 0) & (ranked['J'] > 0))
        | ((ranked['count2'] > 1) & (ranked['J'] > 0))| ((ranked['count2'] > 0) & (ranked['J'] > 1)),
        'figure_score'
    ] = 4  # a full - caution, the J replace the same value for the whole hand
    ranked.loc[
        (ranked['count4'] > 0) | ((ranked['count3'] > 0) & (ranked['J'] > 0))
        | ((ranked['count2'] > 0) & (ranked['J'] > 1)) | (ranked['J'] > 2),
        'figure_score'
    ] = 5  # square
    ranked.loc[
        (ranked['count5'] > 0) | ((ranked['count4'] > 0) & (ranked['J'] > 0))
        | ((ranked['count3'] > 0) & (ranked['J'] > 1)) | ((ranked['count2'] > 0) & (ranked['J'] > 2))
        | (ranked['J'] > 3),
        'figure_score'
    ] = 6  # five of a kind
    # Value of cards by order
    modified_card_values = CARD_VALUES
    modified_card_values['J'] = 1
    for c in range(5):
        ranked[f'card{c}'] = ranked['hand'].apply(lambda x: CARD_VALUES[x[c]])
    # Score
    ranked['score'] = (
            ranked['card4'] + 100 * ranked['card3'] + 1e4 * ranked['card2'] + 1e6 * ranked['card1']
            + 1e8 * ranked['card0'] + 1e10 * ranked['figure_score']
    )
    ranked['rank'] = ranked['score'].rank()
    return ranked


def total_winnings(data, with_jokers=False):
    if with_jokers:
        ranked_hands = rank_with_jokers(data)
    else:
        ranked_hands = rank_hands(data)
    ranked_hands['winning'] = ranked_hands['bid'] * ranked_hands['rank']
    return ranked_hands['winning'].sum()


def run(data_dir, star):
    data = read_data(f'{data_dir}/input-day07.txt', numbers=False, split=' ')

    if star == 1:  # The final answer is: 253866470
        solution = total_winnings(data)
    elif star == 2:  # The final answer is: 254494947
        solution = total_winnings(data, with_jokers=True)
    else:
        raise Exception('Star number must be either 1 or 2.')

    print(f'The solution (star {star}) is: {solution}')
    return solution
