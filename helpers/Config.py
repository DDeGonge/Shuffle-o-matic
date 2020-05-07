# Stepper parameters
b_step_per_mm = 80
d_step_per_mm = 80
p_step_per_mm = 80

# Pins
servo_min = 4.5
servo_max = 10

# Dispense Parameters
servo_speed_rps = 0.75
servo_dwell_s = 0.2

# Shuffle Parameters
cards_per_shuffle_loop = 20  # Too many and it may fail to dispense
shuffle_loops = 4
max_cards_per_bin = 20

# Camera Parameters
# Cropped region of card window
H_MIN = 245
H_MAX = 570
W_MIN = 475
W_MAX = 610
# Split line between card number and suit, from top
H_SPLIT = 185

# Other Junk
step_len_s = 0.000001  # 1us is normal

disp_move_mm = 120
disp_vel_mmps = 30
disp_acc_mmps2 = 100

pusher_move_mm = 68
pusher_vel_mmps = 520
pusher_acc_mmps2 = 12000

bin_vel_mmps = 400
bin_acc_mmps2 = 4000

# bin_heights_load_mm = [0.1, 6, 13.5, 21, 28.5, 36, 43.5, 52]  # bin 0 (bottom) to bin n (top)
bin_heights_load_mm = [0.1, 9, 16, 24, 32, 39, 47, 54]
bin_unload_shift_mm = 32  # bin 0 (bottom) to bin n (top)
