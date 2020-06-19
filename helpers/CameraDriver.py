__version__ = '0.1.0'

from picamera.array import PiRGBArray
from picamera import PiCamera
import scipy.misc
import helpers.CardDetector as Cards
import helpers.Config as cfg
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
        self.train_ranks = Cards.load_ranks(self.TRAIN_PATH)
        self.train_suits = Cards.load_suits(self.TRAIN_PATH)

    def read_card(self):
        image = self._capture_image()
        card = Cards.Identify_Card(image, self.train_ranks, self.train_suits)
        return card

    def _capture_image(self, enable_and_disable: bool = True):
        if enable_and_disable:
            self.start_camera()
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
        self.camera.rotation = cfg.IMAGE_ROTATION_DEGS
        self.rawCapture = PiRGBArray(self.camera)

    def stop_camera(self):
        self.rawCapture.truncate()
        self.camera.close()

if __name__=='__main__':
	c = Camera()
	c.read_card()