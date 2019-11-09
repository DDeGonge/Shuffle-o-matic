__version__ = '0.1.0'

import RPi.GPIO as GPIO
import time

class RCServo(object):
    def __init__(self, servopin=None, pwm_hz=50):
        if servopin == None:
            raise Exception("Error, no pin specified for RCServo Object.")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servopin, GPIO.OUT)
        self.pwm = GPIO.PWM(servopin, pwm_hz)
        self.pwm.start(0)
        self.dutycycle = 0.
        self.movespeed = 0.08  # Seconds per 1ms pwm dutycycle change, used for move_and_disable function
        self.minmovetime = 0.03

    def __del__(self):
        self.pwm.stop()
        GPIO.cleanup()

    def move_and_disable(self, duty):
        movetime = abs(self.dutycycle - duty) * self.movespeed
        movetime = self.minmovetime if movetime < self.minmovetime else movetime
        self.move(duty)
        time.sleep(movetime)
        self.disable()

    def move(self, duty):
        self.dutycycle = duty
        self.pwm.ChangeDutyCycle(duty)

    def disable(self):
        # Don't update dutycycle because this doesn't actually move it
        self.pwm.ChangeDutyCycle(0)
