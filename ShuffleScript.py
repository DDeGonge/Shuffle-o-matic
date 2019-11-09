__version__ = '0.1.0'

from helpers.MotorDriver import Dispenser, Pusher, Bins
from helpers.ServoDriver import RCServo
from helpers.CameraDriver import Camera

import helpers.Config as cfg

import os

def Dump_Row(row):
    if (row > len(cfg.bin_heights_mm)) or (row < 0):
        raise Exception("Bin does not exist")

def main():
    s_obj = RCServo(cfg.servo0_pwm)
    disp_obj = Dispenser()
    push_obj = Pusher()
    bins_obj = Bins()
    return

if __name__ == "__main__":
    main()