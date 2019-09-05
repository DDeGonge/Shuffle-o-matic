__version__ = '0.1.0'

import RPi.GPIO as GPIO

class RCServo(object):
    def __init__(self, servopin, pwm_hz=50):
        if servopin == None:
            raise Exception("Error, no pin specified for RCServo Object.")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servopin, GPIO.OUT)
        self.pwm = GPIO.PWM(servopin, pwm_hz)
        self.enable()

    def update(self, duty):
        self.pwm.ChangeDutyCycle(duty)

    def enable(self, duty=5):
        self.pwm.start(duty)

    def disable(self):
        self.pwm.stop()