import helpers.Config as cfg
from helpers.Gameplay import Card
import numpy as np
import cv2
import sys
import os
from PIL import Image


class Train_Obj(object):
    """ Stores training image and name for either rank or suit set """
    def __init__(self, img = [], name = None):
        self.img = img
        self.name = name


def Identify_Card(img, train_ranks, train_suits):
    # First process image
    processed_img = preprocess_image(img)
    c = get_card_with_cropped_imgs(processed_img)
    c = match_card(c, train_ranks, train_suits)
    return c


def preprocess_image(img, exp_threshold = None):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    blur_crop = blur[cfg.H_MIN:cfg.H_MAX, cfg.W_MIN:cfg.W_MAX]
    if cfg.USE_CAL_IMAGE:
        # Subtract background white cal image before threshold
        cal_img = cv2.imread('helpers/Card_Imgs/cal.jpg')
        blur_crop = cv2.absdiff(blur_crop, cal_img)
        if cfg.DEBUG_MODE:
            debug_save_img(blur_crop, 'cal_greyscale.jpg')
        
    if exp_threshold is None:
        exp_threshold = cfg.BW_THRESH
    _, proc_img = cv2.threshold(blur_crop, exp_threshold, 255, cv2.THRESH_BINARY)
    return proc_img


def get_card_with_cropped_imgs(img):
    # Then crop out rank and suit
    qCard = Card
    qCard.full_img = img

    if cfg.DEBUG_MODE:
        debug_save_img(qCard.full_img, 'fullimg.jpg')

    # Invert image and find contours
    flipped_img = cv2.bitwise_not(qCard.full_img)
    _, contours, _ = cv2.findContours(flipped_img, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Trim smallest contours if too many found
    if len(contours) > cfg.MAX_CONTOURS_TO_CHECK:
        contours = contours[:cfg.MAX_CONTOURS_TO_CHECK]

    # Crop contour regions and save as image array to card
    def contour_to_bb(contour):
        x,y,w,h = cv2.boundingRect(contour)
        return flipped_img[y:y+h, x:x+w]

    qCard.test_imgs = [contour_to_bb(contour) for contour in contours]

    return qCard


def match_card(qCard, train_ranks, train_suits):
    """ Finds best rank and suit matches for the query card. Differences
    the query card rank and suit images with the train rank and suit images.
    The best match is the rank or suit image that has the least difference."""

    best_rank_match_diff = 10000
    best_suit_match_diff = 10000
    qCard.rank = None
    qCard.suit = None

    # Must find at least 2 to find both rank and suit
    if len(qCard.test_imgs) < 2:
        return qCard

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


def load_calibration_set(filepath, set_names):
    """ Loads calibration rank or suit images to create calibration set. """
    def gen_obj(i):
        img = cv2.imread(os.path.join(filepath, i + '.jpg'), cv2.IMREAD_GRAYSCALE)
        return Train_Obj(img=img, name=i)

    return [gen_obj(i) for i in set_names]


def debug_save_img(img, imgname):
    im = Image.fromarray(img)
    im.save(os.path.join('/home/pi/', imgname))
