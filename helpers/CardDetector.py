import helpers.Config as cfg
from helpers.Gameplay import Card
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
BW_THRESH = 70

OBJS_TO_CHECK = 5  # Look at up to this many large masses to find suit and rank
BW_POS = [500,700]  # Should be known good location of white pixel, H x W

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
    bkg_level = gray[BW_POS[0]][BW_POS[1]]
    thresh_level = bkg_level + BW_THRESH
    _, proc_img = cv2.threshold(blur,thresh_level,255,cv2.THRESH_BINARY)
    return proc_img

def get_card_with_cropped_imgs(img):
    # Then crop out rank and suit
    c = Card
    c.full_img = img[cfg.H_MIN:cfg.H_MAX, cfg.W_MIN:cfg.W_MAX]
    debug_save_img(c.full_img, 'fullimg.jpg')

    # Find and isolate up to N largest contours in image
    c = isolate_object_with_contour(c)

    return c

# def get_card_with_cropped_imgs(img):
#     # Then crop out rank and suit
#     c = Card
#     img_cropped = img[cfg.H_MIN:cfg.H_MAX, cfg.W_MIN:cfg.W_MAX]
#     Qrank = img_cropped[:cfg.H_SPLIT, :]
#     Qsuit = img_cropped[cfg.H_SPLIT:, :]

#     # Find rank contour and bounding rectangle, isolate and find largest contour
#     c.rank_img = isolate_object_with_contour(Qrank, RANK_WIDTH, RANK_HEIGHT)
#     c.suit_img = isolate_object_with_contour(Qsuit, SUIT_WIDTH, SUIT_HEIGHT)

#     debug_save_img(c.rank_img, 'rank_img.jpg')
#     debug_save_img(c.suit_img, 'suit_img.jpg')

#     return c

def isolate_object_with_contour(QCard):
    """ Returns bounding boxes of N largest contours found """
    Qimg = cv2.bitwise_not(QCard.full_img)
    _, contours, _ = cv2.findContours(Qimg, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    if len(contours) > OBJS_TO_CHECK:
        contours = contours[:OBJS_TO_CHECK]

    def contour_to_bb(contour):
        x,y,w,h = cv2.boundingRect(contour)
        return Qimg[y:y+h, x:x+w]
        # return cv2.resize(roi, (final_width, final_height), interpolation=cv2.INTER_CUBIC)

    if len(contours) != 0:
        QCard.test_imgs = [contour_to_bb(contour) for contour in contours]

    return QCard


# def isolate_object_with_contour(Qimg, final_width, final_height):
#     Qimg = cv2.bitwise_not(Qimg)
#     _, contours, _ = cv2.findContours(Qimg, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#     contours = sorted(contours, key=cv2.contourArea, reverse=True)
#     if len(contours) != 0:
#         contour = contours[0]
#         x,y,w,h = cv2.boundingRect(contour)
#         roi = Qimg[y:y+h, x:x+w]
#         sized = cv2.resize(roi, (final_width, final_height), interpolation=cv2.INTER_CUBIC)
#         return sized
#     return None

def match_card(qCard, train_ranks, train_suits):
    """Finds best rank and suit matches for the query card. Differences
    the query card rank and suit images with the train rank and suit images.
    The best match is the rank or suit image that has the least difference."""

    best_rank_match_diff = 10000
    best_suit_match_diff = 10000
    qCard.rank = None
    qCard.suit = None

    # Must find at least 2 to find both rank and suit
    if len(test_img) < 2:
        return

    for i, test_img in enumerate(qCard.test_imgs):
        # Find best rank match
        rank_img = cv2.resize(roi, (RANK_WIDTH, RANK_HEIGHT), interpolation=cv2.INTER_CUBIC)
        for Trank in train_ranks:
            diff_img = cv2.absdiff(rank_img, Trank.img)
            rank_diff = int(np.sum(diff_img)/255)
            
            if rank_diff < min(best_rank_match_diff, RANK_DIFF_MAX):
                best_rank_match_diff = rank_diff
                qCard.rank = Trank.name

        # Same process with suit images
        suit_img = cv2.resize(roi, (SUIT_WIDTH, SUIT_HEIGHT), interpolation=cv2.INTER_CUBIC)
        for Tsuit in train_suits:
            diff_img = cv2.absdiff(suit_img, Tsuit.img)
            suit_diff = int(np.sum(diff_img)/255)
            
            if suit_diff < min(best_suit_match_diff, SUIT_DIFF_MAX):
                best_suit_match_diff = suit_diff
                qCard.suit = Tsuit.name

        print('rank:', qCard.rank, best_rank_match_diff)
        print('suit:', qCard.suit, best_suit_match_diff)
        debug_save_img(rank_img, 'rank{}.jpg'.format(i))
        debug_save_img(suit_img, 'suit{}.jpg'.format(i))

        if i >= 2 and best_rank_name is not None and best_suit_name is not None:
            break

    return qCard

# def match_card(qCard, train_ranks, train_suits):
#     """Finds best rank and suit matches for the query card. Differences
#     the query card rank and suit images with the train rank and suit images.
#     The best match is the rank or suit image that has the least difference."""

#     best_rank_match_diff = 10000
#     best_suit_match_diff = 10000
#     best_rank_name = None
#     best_suit_name = None
#     i = 0

#     # If no contours were found in query card in preprocess_card function,
#     # the img size is zero, so skip the differencing process
#     # (card will be left as Unknown)
#     if (len(qCard.rank_img) != 0) and (len(qCard.suit_img) != 0):
        
#         # Difference the query card rank image from each of the train rank images,
#         # and store the result with the least difference
#         for Trank in train_ranks:
#                 diff_img = cv2.absdiff(qCard.rank_img, Trank.img)
#                 rank_diff = int(np.sum(diff_img)/255)
                
#                 if rank_diff < best_rank_match_diff:
#                     best_rank_diff_img = diff_img
#                     best_rank_match_diff = rank_diff
#                     best_rank_name = Trank.name

#         # Same process with suit images
#         for Tsuit in train_suits:
#                 diff_img = cv2.absdiff(qCard.suit_img, Tsuit.img)
#                 suit_diff = int(np.sum(diff_img)/255)
                
#                 if suit_diff < best_suit_match_diff:
#                     best_suit_diff_img = diff_img
#                     best_suit_match_diff = suit_diff
#                     best_suit_name = Tsuit.name

#     # Combine best rank match and best suit match to get query card's identity.
#     # If the best matches have too high of a difference value, card identity
#     # is still Unknown
#     if (best_rank_match_diff < RANK_DIFF_MAX):
#         qCard.rank = best_rank_name

#     if (best_suit_match_diff < SUIT_DIFF_MAX):
#         qCard.suit = best_suit_name

#     # print('rank best diff: {}\nsuit best diff: {}'.format(best_rank_match_diff, best_suit_match_diff))

#     # Return the identiy of the card and the quality of the suit and rank match
#     return qCard

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