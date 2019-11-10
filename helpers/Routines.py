__version__ = '0.1.0'

import helpers.Config as cfg
import time

def Dispense_Card(servo):
    servo.move_and_disable(cfg.servo_max)
    servo.slow_move_and_disable(cfg.servo_min, cfg.servo_speed_rps)
    time.sleep(cfg.servo_dwell_s)
    servo.move_and_disable(cfg.servo_max)

