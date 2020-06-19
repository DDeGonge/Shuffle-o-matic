__version__ = '0.1.0'

ALLRANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
ALLSUITS = ['D', 'H', 'S', 'C']

class Card(object):
    def __init__(self, rank = None, suit = None):
        # self.rank_img = None
        # self.suit_img = None
        self.full_img = None
        self.test_imgs = None
        self.rank = rank
        self.suit = suit

class CardSet(object):
    """ Group of cards where order doesn't matter, like a players hand or the flop """
    def __init__(self):
        self.cards = []  # 2D array, first dimension is card number and second contains acceptable cards
        self.card_found = []

    def add_card(self, rank = None, suit = None):
        """ Add a single or a range of cards to set """
        if rank is None:
            rank = ALLRANKS
        elif not isinstance(rank, list):
            rank = [rank]

        if suit is None:
            suit = ALLSUITS
        elif not isinstance(suit, list):
            suit = [suit]

        thiscard = [Card(rank=r, suit=s) for r in rank for s in suit]
        self.cards.append(thiscard)
        self.card_found.append(False)

    def remove_card(self, card):
        """ Remove this card from all card lists if it exists """
        for i, valid_cards in enumerate(self.cards):
            for j, c in enumerate(valid_cards):
                if self._cards_match(card, c):
                    del self.cards[i][j]

    @staticmethod
    def _cards_match(c1, c2):
        if c1.rank == c2.rank and c1.suit == c2.suit:
            return True
        return False

    def in_list(self, card, mark=True):
        for i, (found, cards) in enumerate(zip(self.card_found, self.cards)):
            for c in cards:
                if self._cards_match(card, c) and not found:
                    if mark:
                        self.card_found[i] = True
                    return True
        return False

class GameSet(object):
    """ Group of cardsets which make up a specific game. This object directly dictates
    which bins cards go to during shuffling """
    def __init__(self, n_players=None):
        self.n_players = n_players
        self.deck_order = []  # Indices for cardsets in desired deck order
        self.bin_order = []  # Initialized by self.break_into_bins()
        self.card_sets = []  # Must be in order dealer, p1, p2, etc
        self.bin_dispense_index = None

    def add_card_set(self, card_set):
        self.card_sets.append(card_set)

    def break_into_bins(self, n_bins):
        self.bin_dispense_index = [0] * (n_bins - 1)
        n_per_bin = int(len(self.deck_order) / (n_bins - 1)) + 1
        for i in range(n_bins - 1):
            this_bin_order = self.deck_order[n_per_bin * i:n_per_bin * (i + 1)]
            this_bin_order.reverse()
            self.bin_order.append(this_bin_order)

    def get_bin(self, card):
        """ Check which bin current card should be dispensed to """
        for bin_num, bin_i in enumerate(self.bin_dispense_index):
            if len(self.bin_order[bin_num]) is not 0 and bin_i < len(self.bin_order[bin_num]):
                card_set_index = self.bin_order[bin_num][bin_i]
                if self.card_sets[card_set_index].in_list(card):
                    self.bin_dispense_index[bin_num] += 1
                    return bin_num

        return None

    def is_shuffle_complete(self):
        if all([bin_i == len(self.bin_order[bin_num]) for bin_num, bin_i in enumerate(self.bin_dispense_index)]):
            return True
        return False

class BlackJack(GameSet):
    def generate_deck(self):
        for i in range(self.n_players * 2):
            self.deck_order.append((i + 1) % self.n_players)

class Holdem(GameSet):
    def generate_deck(self):
        # TODO
        pass
