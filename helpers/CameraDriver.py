__version__ = '0.1.0'

from picamera.array import PiRGBArray
from picamera import PiCamera
import scipy.misc
import helpers.CardDetector as Cards
import helpers.Config as cfg
from helpers.Gameplay import ALLRANKS, ALLSUITS
import sys
import time
import os
import cv2

class Camera(object):
    # TRAINING VALS
    TRAIN_PATH = 'helpers/Card_Imgs'
    def __init__(self, resolution=cfg.IMAGE_RESOLUTION):
        self.camera = None
        self.rawCapture = None
        self.resolution = resolution
        self.train_ranks = Cards.load_calibration_set(self.TRAIN_PATH, ALLRANKS)
        self.train_suits = Cards.load_calibration_set(self.TRAIN_PATH, ALLSUITS)

    def read_card(self, enable_and_disable: bool = False):
        image = self._capture_image(enable_and_disable)
        card = Cards.Identify_Card(image, self.train_ranks, self.train_suits)
        return card

    def exposure_sweep(self, exposures):
        img = self._capture_image(enable_and_disable=True)
        return [Cards.preprocess_image(img, int(exp)) for exp in exposures]

    def _capture_image(self, enable_and_disable):
        if enable_and_disable:
            self.start_camera()
        self.rawCapture = PiRGBArray(self.camera)
        self.camera.capture(self.rawCapture, format="bgr")
        if enable_and_disable:
            self.stop_camera()
        return self.rawCapture.array

    @staticmethod
    def _display_image(img):
        cv2.imshow("Image", img)
        cv2.waitKey(0)

    @staticmethod
    def _save_image(img, path):
        scipy.misc.toimage(img, cmin=0.0, cmax=...).save('path')

    def start_camera(self):
        self.camera = PiCamera()
        self.configure_camera()

    def configure_camera(self):
        self.camera.rotation = cfg.IMAGE_ROTATION_DEGS
        self.camera.resolution = self.resolution
        self.camera.exposure_mode = 'off'

    def stop_camera(self):
        self.camera.close()

if __name__=='__main__':
    c = Camera()
    card = c.read_card()
    print(card.rank, card.suit)
