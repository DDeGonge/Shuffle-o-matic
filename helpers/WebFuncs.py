__version__ = '0.1.0'

# CMD_FILE = '/var/www/html/data.txt'
CMD_FILE = 'data.txt'
SHUFFLES = ['RAND', 'BJACK', 'HOLD']

class CardReq(object):
    """ Can use lists if multiple cards ok """
    allranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    allsuits = ['D', 'H', 'S', 'C']
    def __init__(*args):
        set_card(*args)

    def set_card(self, rank = None, suit = None):
        if rank is None:
            self.rank = allranks
        elif not isinstance(rank, list):
            self.rank = [rank]
        else:
            self.rank = rank

        if suit is None:
            self.suit = allsuits
        elif not isinstance(suit, list):
            self.suit = [suit]
        else:
            self.suit = suit

    def match(self, card):
        if card.rank in self.rank and card.suit in self.suit:
            return True
        return False

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

    # Format deck order based on who should win and n of players
    # winner list goes dealer, p1, p2, etc
    cards = [CardReq] * (n_players * 2)
    if winner[0] is True:
        cards[n_players - 1].set_card(rank='A')
        cards[2*n_players - 1].set_card(rank=['K', 'Q', 'J', '10'])

    for i, w in enumerate(winner[1:]):
        if w is True:
            cards[i].set_card(rank='A')
            cards[n_players + i].set_card(rank=['K', 'Q', 'J', '10'])

    return cards

def format_holdem(data):
    print("TODO")