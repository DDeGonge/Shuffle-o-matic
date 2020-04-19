__version__ = '0.1.0'

import random
import os
import time
import sys

from helpers.MotorDriver import DispenseStep, PushStep, BinStep
from helpers.SerialDevice import SerialDevice
from helpers.DispenserDriver import Dispenser
# from helpers.DCMotorDriver import DCMotor
from helpers.CameraDriver import Camera
import helpers.Config as cfg

def main():
    sd = SerialDevice()
    d_motor = DispenseStep(serial_device=sd)
    p_motor = PushStep(serial_device=sd)
    b_motor = BinStep(serial_device=sd)
    dispenser = Dispenser(serial_device=sd)

    try:
        run_shuffle(d_motor, p_motor, b_motor, dispenser)
    finally:
        d_motor.disable()
        p_motor.disable()

    return

def motor_test():
    sd = SerialDevice()
    d_motor = DispenseStep(serial_device=sd)
    p_motor = PushStep(serial_device=sd)
    b_motor = BinStep(serial_device=sd)
    dispenser = Dispenser(serial_device=sd)

    p_motor.enable()
    p_motor.zero()
    v = 520
    a = 12000
    p_motor.relative_move(68, v, a)
    p_motor.relative_move(-68, v, a)
    p_motor.disable()

    return

def cam_test():
    c = Camera()
    while True:
        card = c.read_card()
        print(card.rank, card.suit)

def run_shuffle(d_motor:DispenseStep, p_motor:PushStep, b_motor:BinStep, dispenser:Dispenser):
    b_motor.enable()
    p_motor.disable()
    b_motor.zero()
    p_motor.zero()
    # d_motor.lower_stage()
    for _ in range(cfg.shuffle_loops):
        dispenser.enable_motor()
        dispenser.baseline_motor_cur()
        
        # Distribute N cards to random bins
        for _ in range(cfg.cards_per_shuffle_loop):
            bin_index = random.randint(0, len(cfg.bin_heights_load_mm)-1)
            # TODO add logic to detect bin overflow
            print("Bin",bin_index)
            b_motor.load_bin_pos(bin_index)
            if not dispenser.dispense_card():
                raise Exception("Card Jam")
        dispenser.disable_motor()

        # Then return cards to dispenser
        nBins = len(cfg.bin_heights_load_mm)
        p_motor.enable()
        for bin_index in reversed(range(nBins)):
            b_motor.unload_bin_pos(bin_index)
            time.sleep(0.2)
            p_motor.run()
        p_motor.disable()
    # TODO disable dispenser motor
    # d_motor.raise_stage()
    b_motor.disable()

if __name__ == "__main__":
    main()
    # motor_test()
    # cam_test()
