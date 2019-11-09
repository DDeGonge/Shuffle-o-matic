__version__ = '0.1.0'

from helpers.MotorDriver import Dispenser, Pusher, Bins
from helpers.ServoDriver import RCServo
#from helpers.CameraDriver import Camera

import helpers.Routines as routine
import helpers.Config as cfg

import os
import time

def main():
    s = RCServo(cfg.servo0_pwm)

    for _ in range(10):
        routine.Dispense_Card(s)
        time.sleep(0.5)

    del s
    return

if __name__ == "__main__":
    main()