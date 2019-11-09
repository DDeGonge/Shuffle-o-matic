__version__ = '0.1.0'

from picamera.array import PiRGBArray
from picamera import PiCamera
import CardDetector.CardDetector.Cards as Cards
import time
import os
import cv2

imagepath = os.path.join('CardDetector','Card_Imgs')

class Camera(object):
    def __init__(self, resolution=(1280,720)):
        self.camera = None
        self.rawCapture = None
        self.train_ranks = Cards.load_ranks(imagepath)
        self.train_suits = Cards.load_suits(imagepath)

    def read_card(self):
        image = self._capture_image()
        cards = self._detect_card(image)
        print(cards)

    def _capture_image(self):
        self._start_camera()
        self.camera.capture(self.rawCapture, format="bgr")
        self._stop_camera()
        return self.rawCapture.array

    def display_image(self, img):
        cv2.imshow("Image", img)
        cv2.waitKey(0)

    def _start_camera(self):
        self.camera = PiCamera()
        self.rawCapture = PiRGBArray(self.camera)
        time.sleep(0.1)

    def _stop_camera(self):
        self.rawCapture.truncate()
        self.camera.close()

    def _detect_card(self, img):
        pre_proc = Cards.preprocess_image(img)
        cnts_sort, cnt_is_card = Cards.find_cards(pre_proc)
        cardset = []
        if len(cnts_sort) != 0:
            for i in range(len(cnts_sort)):
                if (cnt_is_card[i] == 1):
                    card = Cards.preprocess_card(cnts_sort[i],img)
                    cardset.append(Cards.match_card(card,self.train_ranks,self.train_suits))
        return cardset

if __name__=='__main__':
	c = Camera()
	c.read_card()