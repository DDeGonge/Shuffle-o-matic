import helpers.Config as cfg
from helpers.Gameplay import Card
import numpy as np
import cv2
import sys
import os
from PIL import Image


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
    _, proc_img = cv2.threshold(blur, cfg.BW_THRESH, 255, cv2.THRESH_BINARY)
    return proc_img


def get_card_with_cropped_imgs(img):
    # Then crop out rank and suit
    c = Card
    c.full_img = img[cfg.H_MIN:cfg.H_MAX, cfg.W_MIN:cfg.W_MAX]

    if cfg.DEBUG_MODE:
        debug_save_img(c.full_img, 'fullimg.jpg')

    # Find and isolate up to N largest contours in image
    c = isolate_object_with_contour(c)

    return c


def isolate_object_with_contour(QCard):
    """ Returns bounding boxes of N largest contours found """
    Qimg = cv2.bitwise_not(QCard.full_img)
    _, contours, _ = cv2.findContours(Qimg, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    if len(contours) > cfg.MAX_CONTOURS_TO_CHECK:
        contours = contours[:cfg.MAX_CONTOURS_TO_CHECK]

    def contour_to_bb(contour):
        x,y,w,h = cv2.boundingRect(contour)
        return Qimg[y:y+h, x:x+w]

    if len(contours) != 0:
        QCard.test_imgs = [contour_to_bb(contour) for contour in contours]

    return QCard


def match_card(qCard, train_ranks, train_suits):
    """Finds best rank and suit matches for the query card. Differences
    the query card rank and suit images with the train rank and suit images.
    The best match is the rank or suit image that has the least difference."""

    best_rank_match_diff = 10000
    best_suit_match_diff = 10000
    qCard.rank = None
    qCard.suit = None

    # Must find at least 2 to find both rank and suit
    if len(qCard.test_imgs) < 2:
        return

    for i, test_img in enumerate(qCard.test_imgs):
        # Find best rank match
        rank_img = cv2.resize(test_img, (cfg.RANK_WIDTH, cfg.RANK_HEIGHT), interpolation=cv2.INTER_CUBIC)
        for Trank in train_ranks:
            diff_img = cv2.absdiff(rank_img, Trank.img)
            rank_diff = int(np.sum(diff_img)/255)
            
            if rank_diff < min(best_rank_match_diff, cfg.RANK_DIFF_MAX):
                best_rank_match_diff = rank_diff
                qCard.rank = Trank.name

        # Same process with suit images
        suit_img = cv2.resize(test_img, (cfg.SUIT_WIDTH, cfg.SUIT_HEIGHT), interpolation=cv2.INTER_CUBIC)
        for Tsuit in train_suits:
            diff_img = cv2.absdiff(suit_img, Tsuit.img)
            suit_diff = int(np.sum(diff_img)/255)
            
            if suit_diff < min(best_suit_match_diff, cfg.SUIT_DIFF_MAX):
                best_suit_match_diff = suit_diff
                qCard.suit = Tsuit.name

        if cfg.DEBUG_MODE:
            print('rank:', qCard.rank, best_rank_match_diff)
            print('suit:', qCard.suit, best_suit_match_diff)
            debug_save_img(rank_img, 'rank{}.jpg'.format(i))
            debug_save_img(suit_img, 'suit{}.jpg'.format(i))

        if i >= 2 and qCard.rank is not None and qCard.suit is not None:
            break

    return qCard


def load_ranks(filepath):
    """Loads rank images from directory specified by filepath. Stores
    them in a list of Train_ranks objects."""

    train_ranks = []
    i = 0
    
    for Rank in ['A','2','3','4','5','6','7','8','9','10','J','Q','K']:
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
    
    for Suit in ['S','D','C','H']:
        train_suits.append(Train_suits())
        train_suits[i].name = Suit
        filename = Suit + '.jpg'
        train_suits[i].img = cv2.imread(os.path.join(filepath, filename), cv2.IMREAD_GRAYSCALE)
        i = i + 1

    return train_suits


def debug_save_img(img, imgname):
    im = Image.fromarray(img)
    im.save(os.path.join('/home/pi/', imgname))