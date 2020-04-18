__version__ = '0.1.0'

from picamera.array import PiRGBArray
from picamera import PiCamera
import helpers.CardDetector as Cards
import helpers.Config as cfg
import time
import os
import cv2

class Camera(object):
    # TRAINING VALS
    TRAIN_PATH = 'Card_Imgs'
    def __init__(self, resolution=(1280,720)):
        self.camera = None
        self.rawCapture = None
        self.train_ranks = Cards.load_ranks(self.TRAIN_PATH)
        self.train_suits = Cards.load_suits(self.TRAIN_PATH)

    def read_card(self):
        image = self._capture_image()
        card = Cards.Identify_Card(image)
        print(card)
        return card

    def _capture_image(self, enable_and_disable: bool = True):
        if enable_and_disable:
            self.start_camera()
        self.camera.capture(self.rawCapture, format="bgr")
        if enable_and_disable:
            self.stop_camera()
        return self.rawCapture.array

    def _display_image(self, img):
        cv2.imshow("Image", img)
        cv2.waitKey(0)

    def start_camera(self):
        self.camera = PiCamera()
        self.rawCapture = PiRGBArray(self.camera)

    def stop_camera(self):
        self.rawCapture.truncate()
        self.camera.close()

if __name__=='__main__':
	c = Camera()
	c.read_card()