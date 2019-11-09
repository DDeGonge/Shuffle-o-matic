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
        self.movespeed = 0.1  # Seconds per 1ms pwm dutycycle change, used for move_and_disable function
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

    def slow_move_and_disable(self, duty, speed_rps):
        self.slow_move(duty, speed_rps)
        self.disable()
    
    def slow_move(self, duty, speed_rps):
        updatefreq_hz = 20
        movedist = duty - self.dutycycle
        movetime = (abs(movedist) / 20) / speed_rps  # Convert from rps to pwm dutycycles
        numsteps = int(movetime * updatefreq_hz)
        stepsize = movedist / numsteps
        for _ in range(numsteps):
            self.dutycycle += stepsize
            self.pwm.ChangeDutyCycle(self.dutycycle)
            time.sleep(1/updatefreq_hz)

        # Set final dutycycle to account for any errors
        self.pwm.ChangeDutyCycle(duty)
        self.dutycycle = duty

    def disable(self):
        # Don't update dutycycle because this doesn't actually move it
        self.pwm.ChangeDutyCycle(0)
