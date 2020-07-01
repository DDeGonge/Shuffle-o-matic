""" MOTOR PARAMETERS """
b_step_per_mm = 80
d_step_per_mm = 80
p_step_per_mm = 80

step_len_us = 1  # NOT CURRENTLY USED

disp_move_mm = 94
disp_vel_mmps = 50
disp_acc_mmps2 = 100

pusher_move_mm = 68
pusher_vel_mmps = 520
pusher_acc_mmps2 = 12500

bin_vel_mmps = 400
bin_acc_mmps2 = 3500

bin_heights_load_mm = [0.5, 8.2, 15.9, 23.6, 31.3, 39.0, 46.7, 54.4]  # bin 0 (bottom) to bin n (top)
bin_unload_shift_mm = 31


""" DISPENSE PARAMETERS """
dc_motor_spin_down_dwell_s = 0.4
min_time_between_dispenses_s = 0.3
servo_min_pwm = 25
servo_max_pwm = 160
dispense_timeout_ms = 600
current_detect_freq_hz = 500
current_detect_window_ms = 100
current_threshold_factor = 1500  # Multiply by 1000, must be int
servo_return_time_ms = 500
dispense_max_attempts = 3


""" SHUFFLING PARAMETERS """
cards_per_shuffle_loop = 20  # Too many and it may fail to dispense
shuffle_loops = 4
max_cards_per_bin = 10
planned_shuffle_timeout = 80 # If this many cards were trashed and deck still isn't in order, give up


""" CAMERA PARAMETERS """
# Cropped region of card window
H_MIN = 50
H_MAX = 700
W_MIN = 610
W_MAX = 875
IMAGE_RESOLUTION = (1920,1080)
IMAGE_ROTATION_DEGS = 0


""" DETECTION PARAMETERS """
RANK_DIFF_MAX = 2000
SUIT_DIFF_MAX = 1000
RANK_WIDTH = 70
RANK_HEIGHT = 125
SUIT_WIDTH = 70
SUIT_HEIGHT = 100
MAX_CONTOURS_TO_CHECK = 5

USE_CAL_IMAGE = True
BW_THRESH = 10


""" FEATHER COMM PARAMETERS """
# Chars used for setting parameters on feather. All vars here must be int
Feather_Parameter_Chars = {
    'a': step_len_us,
    'b': servo_min_pwm,
    'c': servo_max_pwm,
    'd': dispense_timeout_ms,
    'e': current_detect_freq_hz,
    'f': current_detect_window_ms,
    'g': current_threshold_factor,
    'h': servo_return_time_ms,
    'i': dispense_max_attempts
}

""" DEBUG PARAMS """
DEBUG_MODE = True
