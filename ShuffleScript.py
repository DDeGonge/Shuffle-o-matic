__version__ = '0.1.0'

from helpers.MotorDriver import Dispenser, Pusher, Bins
from helpers.ServoDriver import RCServo
from helpers.DCMotorDriver import DCMotor
#from helpers.CameraDriver import Camera

import helpers.Config as cfg

import random
import os
import time

def testloop():
    servo = RCServo(cfg.servo0_pwm)
    disp_motor = DCMotor(cfg.motor0_enable)
    d_motor = Dispenser()
    p_motor = Pusher()
    b_motor = Bins()

    run_shuffle(servo, disp_motor, d_motor, p_motor, b_motor)

    del servo
    del d_motor
    del p_motor
    del b_motor

    return

def main():
    servo = RCServo(cfg.servo0_pwm)
    disp_motor = DCMotor(cfg.motor0_enable)
    d_motor = Dispenser()
    p_motor = Pusher()
    b_motor = Bins()

    # TODO Home all motors here

    try:
        run_shuffle(servo, disp_motor, d_motor, p_motor, b_motor)
    except KeyboardInterrupt:
        del servo
        del d_motor
        del p_motor
        del b_motor

    return

def run_shuffle(servo:RCServo, disp_motor:DCMotor, d_motor:Dispenser, p_motor:Pusher, b_motor:Bins):
    d_motor.lower_stage()
    for _ in range(cfg.shuffle_loops):
        # First distribute cards
        disp_motor.enable()
        for _ in range(cfg.cards_per_shuffle_loop):
            bin_index = random.randint(0, len(cfg.bin_heights_load_mm)-1)
            # TODO add logic to detect bin overflow
            print("Bin",bin_index)
            b_motor.load_bin_pos(bin_index)
            servo.dispense_card()
        disp_motor.disable()

        # Then return cards to bin
        nBins = len(cfg.bin_heights_load_mm)
        for bin_index in reversed(range(nBins)):
            b_motor.unload_bin_pos(bin_index)
            p_motor.run()
    # TODO disable dispenser motor
    d_motor.raise_stage()

if __name__ == "__main__":
    testloop()
    # main()
