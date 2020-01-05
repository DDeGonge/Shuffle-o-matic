__version__ = '0.1.0'

import RPi.GPIO as GPIO
import time

class DCMotor(object):
    def __init__(self, motorpin=None, sensepin=None):
        self.motorpin = motorpin
        self.sensepin = sensepin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(motorpin, GPIO.OUT)
        # GPIO.setup(sensepin, GPIO.IN)
        self.disable()

    def __del__(self):
        self.disable()
        GPIO.cleanup()

    def enable(self):
        GPIO.output(self.motorpin, GPIO.LOW)

    def disable(self):
        GPIO.output(self.motorpin, GPIO.HIGH)