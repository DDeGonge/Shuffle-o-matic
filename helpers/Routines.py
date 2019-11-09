__version__ = '0.1.0'

from helpers.MotorDriver import Dispenser, Pusher, Bins
from helpers.ServoDriver import RCServo
from helpers.CameraDriver import Camera

import helpers.Config as cfg
import time

def Dispense_Card(RCServo s):
    s.slow_move_and_disable(cfg.servo_max, cfg.servo_speed_rps)
    time.sleep(cfg.servo_dwell_s)
    s.move_and_disable(cfg.servo_min)

def Dump_Row(row_i):
    if (row_i > len(cfg.bin_heights_mm)) or (row_i < 0):
        raise Exception("Bin does not exist")