__version__ = '0.1.0'

from helpers.MotorDriver import Motor
from helpers.ServoDriver import Servo
from helpers.CameraDriver import RCServo

import helpers.Config as cfg

import os

def main():
	s_obj = RCServo(cfg.servo0_pwm)
    return

if __name__ == "__main__":
    main()