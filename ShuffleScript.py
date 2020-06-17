__version__ = '0.1.0'

import random
import os
import time
import sys

from helpers.MotorDriver import DispenseStep, PushStep, BinStep
from helpers.SerialDevice import SerialDevice
from helpers.DispenserDriver import Dispenser
from WebFuncs import check_for_cmd
# from helpers.DCMotorDriver import DCMotor
# from helpers.CameraDriver import Camera
import helpers.Config as cfg

CMD_FILE = '/var/www/html/data.txt'

def main():
    sd = SerialDevice()
    d_motor = DispenseStep(serial_device=sd)
    p_motor = PushStep(serial_device=sd)
    b_motor = BinStep(serial_device=sd)
    dispenser = Dispenser(serial_device=sd)

    t_start = time.time()
    try:
        while True:
            cmd, data = check_for_cmd()
            print(cmd)
            print(data + "/n/n")
            time.sleep(0.2)
        # run_shuffle(d_motor, p_motor, b_motor, dispenser)
    finally:
        # d_motor.raise_stage()
        b_motor.disable()
        d_motor.disable()
        p_motor.disable()
        dispenser.disable_motor()
    
    return

def motor_test():
    sd = SerialDevice()
    # motor = DispenseStep(serial_device=sd)
    # motor = PushStep(serial_device=sd)
    motor = BinStep(serial_device=sd)
    # dispenser = Dispenser(serial_device=sd)

    motor.enable()
    motor.zero()
    v = 10
    a = 50
    d = 5
    for _ in range(2):
        motor.relative_move(d, v, a)
        motor.relative_move(-d, v, a)
    motor.disable()

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
    dispenser.disable_motor()
    
    for i in range(cfg.shuffle_loops):
        print("CYCLE {} / {}".format(i + 1, cfg.shuffle_loops))
        dispenser.enable_motor()
        dispenser.baseline_motor_cur()
        
        # Distribute N cards to random bins
        t_last_dispense = time.time()
        last_bin = -1
        cards_in_bin = [0] * len(cfg.bin_heights_load_mm)
        for _ in range(cfg.cards_per_shuffle_loop):
            # Select bin index, ugly brute force but it's fine shutup
            while True:
                bin_index = random.randint(0, len(cfg.bin_heights_load_mm) - 1)
                if cards_in_bin[bin_index] < cfg.max_cards_per_bin and bin_index is not last_bin:
                    last_bin = bin_index
                    cards_in_bin[bin_index] += 1
                    break

            # Move to bin location
            b_motor.load_bin_pos(bin_index)

            # Dispense card
            while time.time() < t_last_dispense + cfg.min_time_between_dispenses_s:
                pass
            if not dispenser.dispense_card():
                raise Exception("Card Jam")
            t_last_dispense = time.time()

        # Shutdown dispenser motor and servo
        dispenser.disable_motor()
        time.sleep(cfg.dc_motor_spin_down_dwell_s)

        # Return cards from bins to dispenser
        nBins = len(cfg.bin_heights_load_mm)
        p_motor.enable()
        for bin_index in reversed(range(nBins)):
            b_motor.unload_bin_pos(bin_index)
            time.sleep(0.1)
            p_motor.run()

        p_motor.disable()

if __name__ == "__main__":
    main()
    # motor_test()
    # cam_test()
