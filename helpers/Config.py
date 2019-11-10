""" SERVO PINS """
servo0_pwm = 18 # PI pin 12

""" DC MOTOR PINS """
motor0_enable = 0

""" STEPPER """
# Dispense stepper
d_stepper_dir = 17
d_stepper_step = 27
d_stepper_lim = 22
d_step_per_mm = 80
d_stepper_reverse = 1  # change to -1 to reverse direction

# Pusher stepper
p_stepper_dir = 5
p_stepper_step = 6
p_stepper_lim = 13
p_step_per_mm = 80
p_stepper_reverse = 1  # change to -1 to reverse direction

# Bins stepper
b_stepper_dir = 16
b_stepper_step = 20
b_stepper_lim = 21
b_step_per_mm = 80
b_stepper_reverse = 1  # change to -1 to reverse direction

""" OTHER VARIABLES """
# Pins
servo_min = 4
servo_max = 10

# Dispense Parameters
servo_speed_rps = 0.75
servo_dwell_s = 0.1

# Shuffle Parameters
cards_per_shuffle_loop = 30  # Too many and it may fail to dispense cards
shuffle_loops = 3
max_cards_per_bin = 20

# Other Junk

disp_move_mm = 120
disp_vel_mmps = 30
disp_acc_mmps2 = 100

pusher_move_mm = 120
pusher_vel_mmps = 30
pusher_acc_mmps2 = 100

step_len_s = 0.000001  # 1us is normal
bin_vel_mmps = 90
bin_acc_mmps2 = 500
bin_heights_load_mm = [10,20,30,40,50,60,70]  # bin 0 (bottom) to bin n (top)
bin_unload_shift_mm = 50  # bin 0 (bottom) to bin n (top)