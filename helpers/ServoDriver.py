__version__ = '0.1.0'

import RPi.GPIO as GPIO
import time

MOVETIME_MULT = 0.1  # Seconds per 1ms pwm dutycycle change, used for move_and_disable function

class RCServo(object):
    def __init__(self, servopin=None, pwm_hz=50):
        if servopin == None:
            raise Exception("Error, no pin specified for RCServo Object.")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servopin, GPIO.OUT)
        self.pwm = GPIO.PWM(servopin, pwm_hz)
        self.pwm.start(0)
        self.dutycycle = 0.

    def move_and_disable(self, duty):
        movetime = abs(self.dutycycle - duty) * MOVETIME_MULT
        self.enable(duty)
        time.sleep(movetime)
        self.disable()

    def update(self, duty):
        self.dutycycle = duty
        self.pwm.ChangeDutyCycle(duty)

    def enable(self, duty=None):
        if duty is None:
            self.pwm.ChangeDutyCycle(self.dutycycle)
        else:
            self.dutycycle = duty
            self.pwm.ChangeDutyCycle(duty)

    def disable(self):
        self.pwm.ChangeDutyCycle(0)