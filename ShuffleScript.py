__version__ = '0.1.0'

from helpers.MotorDriver import Dispenser, Pusher, Bins
from helpers.ServoDriver import RCServo
from helpers.CameraDriver import Camera

import helpers.Routines as routine
import helpers.Config as cfg

import os

def main():
    s = RCServo(cfg.servo0_pwm)
    routine.Dispense_Card(s)
    return

if __name__ == "__main__":
    main()