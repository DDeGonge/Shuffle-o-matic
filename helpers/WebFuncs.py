__version__ = '0.1.0'

# CMD_FILE = '/var/www/html/data.txt'
CMD_FILE = 'data.txt'
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
    print("TODO")

def format_holdem(data):
    print("TODO")