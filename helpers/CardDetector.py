import helpers.Config as cfg
import numpy as np
import cv2
import sys
import os
from PIL import Image

np.set_printoptions(threshold=sys.maxsize)

RANK_DIFF_MAX = 5000
SUIT_DIFF_MAX = 5000
RANK_WIDTH = 70
RANK_HEIGHT = 125
SUIT_WIDTH = 70
SUIT_HEIGHT = 100
BW_THRESH = 45

class Card(object):
    rank = None
    suit = None
    rank_img = None
    suit_img = None

class Train_ranks(object):
    def __init__(self):
        self.img = [] # Thresholded, sized rank image loaded from hard drive
        self.name = "Placeholder"

class Train_suits(object):
    def __init__(self):
        self.img = [] # Thresholded, sized suit image loaded from hard drive
        self.name = "Placeholder"

def Identify_Card(img, train_ranks, train_suits):
    # First process image
    processed_img = preprocess_image(img)
    c = get_card_with_cropped_imgs(processed_img)
    c = match_card(c, train_ranks, train_suits)
    return c

def preprocess_image(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    img_w, img_h = np.shape(img)[:2]
    bkg_level = gray[int(img_h/100)][int(img_w/2)]
    thresh_level = bkg_level + BW_THRESH
    _, proc_img = cv2.threshold(blur,thresh_level,255,cv2.THRESH_BINARY)
    return proc_img

def get_card_with_cropped_imgs(img):
    # Then crop out rank and suit
    c = Card
    img_cropped = img[cfg.H_MIN:cfg.H_MAX, cfg.W_MIN:cfg.W_MAX]
    Qrank = img_cropped[:cfg.H_SPLIT, :]
    Qsuit = img_cropped[cfg.H_SPLIT:, :]

    # Find rank contour and bounding rectangle, isolate and find largest contour
    dummy, Qrank_cnts, hier = cv2.findContours(Qrank, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    Qrank_cnts = sorted(Qrank_cnts, key=cv2.contourArea,reverse=True)
    if len(Qrank_cnts) != 0:
        x1,y1,w1,h1 = cv2.boundingRect(Qrank_cnts[0])
        Qrank_roi = Qrank[y1:y1+h1, x1:x1+w1]
        Qrank_roi = cv2.bitwise_not(Qrank_roi)
        Qrank_sized = cv2.resize(Qrank_roi, (RANK_WIDTH, RANK_HEIGHT), interpolation=cv2.INTER_CUBIC)
        c.rank_img = Qrank_sized

    # Find suit contour and bounding rectangle, isolate and find largest contour
    dummy, Qsuit_cnts, hier = cv2.findContours(Qsuit, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    Qsuit_cnts = sorted(Qsuit_cnts, key=cv2.contourArea,reverse=True)
    if len(Qsuit_cnts) != 0:
        x2,y2,w2,h2 = cv2.boundingRect(Qsuit_cnts[0])
        Qsuit_roi = Qsuit[y2:y2+h2, x2:x2+w2]
        Qsuit_roi = cv2.bitwise_not(Qsuit_roi)
        Qsuit_sized = cv2.resize(Qsuit_roi, (SUIT_WIDTH, SUIT_HEIGHT), interpolation=cv2.INTER_CUBIC)
        c.suit_img = Qsuit_sized

    return c

def match_card(qCard, train_ranks, train_suits):
    """Finds best rank and suit matches for the query card. Differences
    the query card rank and suit images with the train rank and suit images.
    The best match is the rank or suit image that has the least difference."""

    best_rank_match_diff = 10000
    best_suit_match_diff = 10000
    best_rank_match_name = "Unknown"
    best_suit_match_name = "Unknown"
    i = 0

    print(qCard.rank_img.shape, qCard.suit_img.shape)
    im = Image.fromarray(qCard.rank_img)
    im.save("/home/pi/rank.jpg")
    im = Image.fromarray(qCard.suit_img)
    im.save("/home/pi/suit.jpg")

    # If no contours were found in query card in preprocess_card function,
    # the img size is zero, so skip the differencing process
    # (card will be left as Unknown)
    if (len(qCard.rank_img) != 0) and (len(qCard.suit_img) != 0):
        
        # Difference the query card rank image from each of the train rank images,
        # and store the result with the least difference
        for Trank in train_ranks:
                diff_img = cv2.absdiff(qCard.rank_img, Trank.img)
                rank_diff = int(np.sum(diff_img)/255)
                
                if rank_diff < best_rank_match_diff:
                    best_rank_diff_img = diff_img
                    best_rank_match_diff = rank_diff
                    best_rank_name = Trank.name

        # Same process with suit images
        for Tsuit in train_suits:
                diff_img = cv2.absdiff(qCard.suit_img, Tsuit.img)
                suit_diff = int(np.sum(diff_img)/255)
                
                if suit_diff < best_suit_match_diff:
                    best_suit_diff_img = diff_img
                    best_suit_match_diff = suit_diff
                    best_suit_name = Tsuit.name

    # Combine best rank match and best suit match to get query card's identity.
    # If the best matches have too high of a difference value, card identity
    # is still Unknown
    if (best_rank_match_diff < RANK_DIFF_MAX):
        qCard.rank = best_rank_name

    if (best_suit_match_diff < SUIT_DIFF_MAX):
        qCard.suit = best_suit_name

    print('rank best diff: {}\nsuit best diff: {}'.format(best_rank_match_diff, best_suit_match_diff))

    # Return the identiy of the card and the quality of the suit and rank match
    return qCard

def load_ranks(filepath):
    """Loads rank images from directory specified by filepath. Stores
    them in a list of Train_ranks objects."""

    train_ranks = []
    i = 0
    
    for Rank in ['Ace','Two','Three','Four','Five','Six','Seven',
                 'Eight','Nine','Ten','Jack','Queen','King']:
        train_ranks.append(Train_ranks())
        train_ranks[i].name = Rank
        filename = Rank + '.jpg'
        train_ranks[i].img = cv2.imread(os.path.join(filepath, filename), cv2.IMREAD_GRAYSCALE)
        i = i + 1

    return train_ranks

def load_suits(filepath):
    """Loads suit images from directory specified by filepath. Stores
    them in a list of Train_suits objects."""

    train_suits = []
    i = 0
    
    for Suit in ['Spades','Diamonds','Clubs','Hearts']:
        train_suits.append(Train_suits())
        train_suits[i].name = Suit
        filename = Suit + '.jpg'
        train_suits[i].img = cv2.imread(os.path.join(filepath, filename), cv2.IMREAD_GRAYSCALE)
        i = i + 1

    return train_suits