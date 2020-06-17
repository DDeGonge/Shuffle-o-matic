__version__ = '0.1.0'

import os
from helpers.Gameplay import *

CMD_FILE = '/var/www/html/data.txt'
SHUFFLES = ['RAND', 'BJACK', 'HOLD']

def check_for_cmd():
    """ Returns tuple of [Type] [Data] where type is the shuffle type and data
    will contain either random shuffle parameters or the top deck order required """
    with open(CMD_FILE, 'r+') as f:
        data = f.readline()
        f.truncate(0)

    rawdata = data.split(',')
    if rawdata[0] in SHUFFLES:
        shuffletype = SHUFFLES.index(rawdata[0])
        if shuffletype is 0:
            return (rawdata[0], format_rand(rawdata[1:]))
        elif shuffletype is 1:
            return (rawdata[0], format_bjack(rawdata[1:]))
        elif shuffletype is 2:
            return (rawdata[0], format_holdem(rawdata[1:]))

    return (None, None)

def format_rand(data):
    return [float(i) for i in data]

def format_bjack(data):
    # Gather data
    n_players = int(data[0])
    def wincheck(val):
        if val is "true":
            return True
        return False
    winner = [wincheck(i) for i in data[1:]]

    # Build desired deck based on winners
    deck = BlackJack(n_players=n_players)
    for i, w in enumerate(winner):
        if i < n_players:
            hand = CardSet()
            if w is True:
                hand.add_card(rank='A')
                hand.add_card(rank=['K', 'Q', 'J', '10'])
            else:
                hand.add_card(rank=['2', '3', '4', '5', '6', '7', '8', '9'])
                hand.add_card(rank=['2', '3', '4', '5', '6', '7', '8', '9'])
            deck.add_card_set(hand)

    deck.generate_deck()
    return deck

def format_holdem(data):
    print("TODO")

if __name__=='__main__':
    data = ['4','','true','true','true','','']
    deck = format_bjack(data)
    deck.break_into_bins(8)
    print(deck.deck_order)
    print(deck.bin_order)
    print(deck.card_sets)
    print(deck.bin_dispense_index)

    two = Card(rank='2', suit='D')
    ace = Card(rank='A', suit='D')
    ten = Card(rank='10', suit='D')

    for i in range(3):
        print('two: ', deck.get_bin(two))
        print(deck.bin_dispense_index, '\n')
        print('ace: ', deck.get_bin(ace))
        print(deck.bin_dispense_index, '\n')
        print('ten: ', deck.get_bin(ten))
        print(deck.bin_dispense_index, '\n')
        print(deck.is_shuffle_complete())
        print('\n\n')
