__version__ = '0.1.0'

import helpers.Config as cfg
import time
import math

DEBUG = True

class Motor:
    def __init__(self, serial_device, stepspermm, stepper_index):
        self.steps_per_mm = stepspermm
        self.serial_device = serial_device
        self.stepper_index = stepper_index
        self.error = 0.
        self.configure()

    def home(self):
        self.relative_move(-300)
        if self.is_homed:
        	self.relative_move(3)
        	self.relative_move(-5,1,50)
        if not self.is_homed:
        	raise('Error: Failed to home')
        print('homed')

    def zero(self):
        self.serial_device.command('z,' + str(self.stepper_index) + ',0')

    def enable(self):
        self.serial_device.command('s,' + str(self.stepper_index))

    def disable(self):
        self.serial_device.command('x,' + str(self.stepper_index))

    def update_defaults(self, vel, acc):
        self.def_vel = vel
        self.def_acc = acc

    def configure(self, steps_per_mm=None):
        if not steps_per_mm:
            steps_per_mm = self.steps_per_mm

        self.serial_device.command('f,' + str(self.stepper_index) + ',' + str(1000 * steps_per_mm))

    def absolute_move(self, distance_mm, velocity_mmps=None, accel_mmps2=None):
        # Pull defaults if vel or acc not specified
        if velocity_mmps is None:
            velocity_mmps = self.def_vel
        if accel_mmps2 is None:
            accel_mmps2 = self.def_acc

        # Calculate move
        command = 'm,' + str(self.stepper_index) + ',' + str(self._calc_steps(distance_mm)) + ',' + str(velocity_mmps) + ',' + str(accel_mmps2)
        self.serial_device.command(command)

    def relative_move(self, distance_mm, velocity_mmps=None, accel_mmps2=None):
         return self.absolute_move(self.pos_mm + distance_mm, velocity_mmps, accel_mmps2)

    @property
    def is_homed(self):
        return True

    @property
    def pos_mm(self):
        resp = self.serial_device.command('p').strip('\n').split(',')
        return int(resp[self.stepper_index + 1]) / self.steps_per_mm

    def _calc_steps(self, dist_mm):
        steps_tot = (dist_mm + self.error) * self.steps_per_mm
        steps = math.floor(steps_tot)
        self.error = steps_tot - steps
        return steps

class DispenseStep(Motor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, stepspermm = cfg.d_step_per_mm, stepper_index = 2)
        self.update_defaults(cfg.disp_vel_mmps, cfg.disp_acc_mmps2)

    def raise_stage(self):
        self.absolute_move(cfg.disp_move_mm, cfg.disp_vel_mmps, cfg.disp_acc_mmps2)

    def lower_stage(self):
        self.absolute_move(0.2, cfg.disp_vel_mmps, cfg.disp_acc_mmps2)


class PushStep(Motor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, stepspermm = cfg.p_step_per_mm, stepper_index = 1)
        self.update_defaults(cfg.pusher_vel_mmps, cfg.pusher_acc_mmps2)

    def run(self, dwell_s=0.1):
        self.absolute_move(cfg.pusher_move_mm, cfg.pusher_vel_mmps, cfg.pusher_acc_mmps2)
        time.sleep(dwell_s)
        self.absolute_move(0.2, cfg.pusher_vel_mmps, cfg.pusher_acc_mmps2)


class BinStep(Motor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, stepspermm = cfg.b_step_per_mm, stepper_index = 0)
        self.update_defaults(cfg.bin_vel_mmps, cfg.bin_acc_mmps2)

    def load_bin_pos(self, bin_num):
        self.absolute_move(cfg.bin_heights_load_mm[bin_num], cfg.bin_vel_mmps, cfg.bin_acc_mmps2)

    def unload_bin_pos(self, bin_num):
        self.absolute_move(cfg.bin_heights_load_mm[bin_num] + cfg.bin_unload_shift_mm, cfg.bin_vel_mmps, cfg.bin_acc_mmps2)