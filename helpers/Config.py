""" SERVO PINS """
servo0_pwm = 18 # PI pin 12

""" STEPPER """
# Dispense stepper
d_stepper_dir = 0
d_stepper_step = 0
d_stepper_lim = 0
d_step_per_mm = 80
d_stepper_reverse = 1 # change to -1 to reverse direction

# Pusher stepper
p_stepper_dir = 0
p_stepper_step = 0
p_stepper_lim = 0
p_step_per_mm = 80
p_stepper_reverse = 1 # change to -1 to reverse direction

# Bins stepper
b_stepper_dir = 0
b_stepper_step = 0
b_stepper_lim = 0
b_step_per_mm = 80
b_stepper_reverse = 1 # change to -1 to reverse direction

""" OTHER VARIABLES """
servo_min = 20
servo_max = 80

disp_move_mm = 120
disp_vel_mmps = 30
disp_acc_mmps2 = 100

pusher_move_mm = 120
pusher_vel_mmps = 30
pusher_acc_mmps2 = 100

step_len_s = 0.000001 # 1us is normal
bin_vel_mmps = 90
bin_acc_mmps2 = 500
bin_heights_load_mm = [10,20,30,40,50,60,70] # bin 0 (bottom) to bin n (top)
bin_unload_shift_mm = 50 # bin 0 (bottom) to bin n (top)