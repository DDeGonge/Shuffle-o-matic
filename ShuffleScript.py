__version__ = '0.1.0'

import random
import os
import time
import sys
from typing import List

from helpers.MotorDriver import DispenseStep, PushStep, BinStep
from helpers.SerialDevice import SerialDevice
from helpers.DispenserDriver import Dispenser
from helpers.WebFuncs import check_for_cmd
from helpers.CameraDriver import Camera, debug_save_img
import helpers.Config as cfg


def main():
    sd = SerialDevice()
    d_motor = DispenseStep(serial_device=sd)
    p_motor = PushStep(serial_device=sd)
    b_motor = BinStep(serial_device=sd)
    dispenser = Dispenser(serial_device=sd)
    camera = Camera()

    b_motor.zero()
    p_motor.zero()
    d_motor.zero()

    t_start = time.time()
    d_motor.enable()
    d_motor.raise_stage()

    print('READY')
    try:
        while True:
            try:
                cmd, data = check_for_cmd()
                if cmd is not None:
                    pre_shuffle(d_motor, p_motor, b_motor, dispenser)
                    if 'RAND' in cmd:
                        random_shuffle(d_motor, p_motor, b_motor, dispenser, data)
                    elif 'BJACK' in cmd or 'HOLD' in cmd:
                        planned_shuffle(d_motor, p_motor, b_motor, dispenser, camera, data)
                    post_shuffle(d_motor, p_motor, b_motor, dispenser)
                    print('Shuffle Completed!')
            except Exception as e:
                print('Shuffle Errored!', e)
                pass

            time.sleep(0.1)
    except KeyboardInterrupt:
        post_shuffle(d_motor, p_motor, b_motor, dispenser)
        d_motor.disable()


def pre_shuffle(d_motor:DispenseStep, p_motor:PushStep, b_motor:BinStep, dispenser:Dispenser):
    b_motor.enable()
    p_motor.disable()
    d_motor.enable()
    d_motor.lower_stage()
    dispenser.disable_motor()


def random_shuffle(d_motor:DispenseStep, p_motor:PushStep, b_motor:BinStep, dispenser:Dispenser, params: List[float]):
    shuffle_loops = params[0]
    cards_per_shuffle_loop = params[1]
    for i in range(shuffle_loops):
        print("CYCLE {} / {}".format(i + 1, shuffle_loops))
        dispenser.enable_motor()
        dispenser.baseline_motor_cur()
        
        # Distribute N cards to random bins
        t_last_dispense = time.time()
        last_bin = -1
        cards_in_bin = [0] * len(cfg.bin_heights_load_mm)
        for _ in range(cards_per_shuffle_loop):
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
        return_all_cards(p_motor, b_motor)


def planned_shuffle(d_motor:DispenseStep, p_motor:PushStep, b_motor:BinStep, dispenser:Dispenser, camera:Camera, deck):
    # Initialize vars
    dispenser.enable_motor()
    dispenser.baseline_motor_cur()
    t_last_dispense = time.time()
    n_bins = len(cfg.bin_heights_load_mm)
    cards_in_trash = 0

    camera.start_camera()

    # Generate bin reqs for deck
    deck.break_into_bins(n_bins=n_bins)

    def empty_trash():
        p_motor.enable()
        b_motor.unload_bin_pos(n_bins-1)
        time.sleep(0.1)
        p_motor.run()
        p_motor.disable()

    junk_cards_dispensed = 0
    last_card = camera.read_card()
    while junk_cards_dispensed < cfg.planned_shuffle_timeout:
        card = camera.read_card()

        # Determine where to put card. If it is the same as last, it probs failed to dispense
        if card.rank is None and card.suit is None:
            bin_index = None
        elif last_card.rank is card.rank and last_card.suit is card.suit:
            print('Previous card failed to dispense. Re-dispensing')
            pass
        else:
            bin_index = deck.get_bin(card)
            last_card = card
            print(card.rank, card.suit, ":", bin_index)

            # Handle vars if trash card
            if bin_index is None:
                bin_index = n_bins - 1
                cards_in_trash += 1
                junk_cards_dispensed += 1

            # Move to bin location
            b_motor.load_bin_pos(bin_index)

        # Dispense card
        while time.time() < t_last_dispense + cfg.min_time_between_dispenses_s:
            pass
        if not dispenser.dispense_card():
            raise Exception("Card Jam")
        t_last_dispense = time.time()

        # Check for full trash
        if cards_in_trash >= cfg.max_cards_per_bin:
            empty_trash()
            cards_in_trash = 0

        # Check for shuffle completion
        if deck.is_shuffle_complete:
            return_all_cards(p_motor, b_motor)
            break

    else:
        print("Planned Shuffle Timeout")

    camera.stop_camera()


def post_shuffle(d_motor:DispenseStep, p_motor:PushStep, b_motor:BinStep, dispenser:Dispenser):
    dispenser.disable_motor()
    p_motor.disable()
    b_motor.disable()
    d_motor.enable()
    d_motor.raise_stage()


def return_all_cards(p_motor, b_motor):
    nBins = len(cfg.bin_heights_load_mm)
    p_motor.enable()
    for bin_index in reversed(range(nBins)):
        b_motor.unload_bin_pos(bin_index)
        time.sleep(0.1)
        p_motor.run()

    p_motor.disable()


""" TEMPORARY DEBUGGING FUNCTIONS """

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
        _ = input('Press enter to read card')
        card = c.read_card(enable_and_disable=True)
        print(card.rank, card.suit)

def cap_deck():
    c = Camera()
    sd = SerialDevice()
    dispenser = Dispenser(serial_device=sd)
    count = 0
    for i in range(10):
        _ = input('press enter to start...')
        for j in range(10):
            img = c._capture_image(enable_and_disable=True)
            debug_save_img(img, '/home/pi/pics/{}.jpg'.format(count))
            count += 1
            dispenser.dispense_card()



def gen_random_card():
    import helpers.Gameplay as g
    rank_i = random.randint(0, 12)
    suit_i = random.randint(0, 3)
    return g.Card(rank = g.ALLRANKS[rank_i], suit = g.ALLSUITS[suit_i])

if __name__ == "__main__":
    # main()
    cap_deck()
    # motor_test()
    # cam_test()
