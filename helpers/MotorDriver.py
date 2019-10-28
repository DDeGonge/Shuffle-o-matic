__version__ = '0.1.0'

from gpiozero import LED
import Config as cfg
import time
import math

class Motor:
    def __init__(self, step_pin, dir_pin, limit_pin, stepspermm, invert):
        self.pos_mm = 0.
        self.steppin = LED(step_pin)
        self.dirpin = LED(dir_pin)
        self.steps_per_mm = stepspermm
        self.error = 0.
        self.invert = invert

    def home(self):
        print('homed')

    def update_defaults(self, vel, acc):
        self.def_vel = vel
        self.def_acc = acc

    def relative_move(self, distance_mm, velocity_mmps=None, accel_mmps2=None):
        # Pull defaults if vel or acc not specified
        if velocity_mmps is None:
            velocity_mmps = self.def_vel
        if accel_mmps2 is None:
            accel_mmps2 = self.def_acc

        # Set direction
        stepsize_mm = 1 / self.steps_per_mm
        if (self.invert * distance_mm) < 0:
            self.dirpin.on()
            distance_mm *= -1
            stepsize_mm *= -1
        else:
            self.dirpin.off()

        # Calculate move
        steps = self._calc_steps(distance_mm)
        move_delays = self._calc_move(steps, velocity_mmps, accel_mmps2)

        # Execute move
        movestart = time.time()
        nextstep = movestart
        for stepdel in move_delays:
            nextstep += stepdel
            while time.time() < nextstep:
                pass
            self._step()
            self.pos_mm += stepsize_mm
        return True

    def absolute_move(self, distance_mm, velocity_mmps=None, accel_mmps2=None):
         return self.relative_move(position_mm - self.pos_mm, velocity_mmps, accel_mmps2)

    def _calc_steps(self, dist_mm):
        steps_tot = (dist_mm + self.error) * self.steps_per_mm
        steps = math.floor(steps_tot)
        self.error = steps_tot - steps
        return steps

    def _calc_move(self, steps, vel_mmps, acc_mmps2):
        vel_delay_s = (1 / (vel_mmps * self.steps_per_mm))
        return [vel_delay_s]*steps

        # TODO create acceleration and jerk ramping
        acc_delay_ms = (1 / (acc_mmps2 * self.steps_per_mm))
        ramp = range(vel_delay_ms, 5000, acc_delay_ms)
        movebuffer = []

    def _step(self):
        print(self.pos_mm)
        self.steppin.on()
        time.sleep(cfg.step_len_s)
        self.steppin.off()

class Dispenser(Motor):
    def __init__(self):
        super().__init__(step_pin = cfg.d_stepper_step,
                        dir_pin = cfg.d_stepper_dir,
                        limit_pin = cfg.d_stepper_lim,
                        stepspermm = cfg.d_step_per_mm,
                        invert = cfg.d_stepper_reverse)
        self.update_defaults(cfg.disp_vel_mmps, cfg.disp_acc_mmps2)
        self.home()

    def raise_stage(self):
        self.absolute_move(cfg.disp_move_mm, cfg.disp_vel_mmps, cfg.disp_acc_mmps2)

    def lower_stage(self):
        self.absolute_move(0.2, cfg.disp_vel_mmps, cfg.disp_acc_mmps2)


class Pusher(Motor):
    def __init__(self):
        super().__init__(step_pin = cfg.p_stepper_step,
                        dir_pin = cfg.p_stepper_dir,
                        limit_pin = cfg.p_stepper_lim,
                        stepspermm = cfg.p_step_per_mm,
                        invert = cfg.p_stepper_reverse)
        self.update_defaults(cfg.pusher_vel_mmps, cfg.pusher_acc_mmps2)
        self.home()

    def run(self):
        self.absolute_move(cfg.pusher_move_mm, cfg.pusher_vel_mmps, cfg.pusher_acc_mmps2)
        self.absolute_move(0.2, cfg.pusher_vel_mmps, cfg.pusher_acc_mmps2)


class Bins(Motor):
    def __init__(self):
        super().__init__(step_pin = cfg.b_stepper_step,
                        dir_pin = cfg.b_stepper_dir,
                        limit_pin = cfg.b_stepper_lim,
                        stepspermm = cfg.b_step_per_mm,
                        invert = cfg.b_stepper_reverse)
        self.update_defaults(cfg.bin_vel_mmps, cfg.bin_acc_mmps2)
        self.home()

    def load_bin_pos(self, bin_num):
        self.absolute_move(cfg.bin_heights_load_mm[bin_num], cfg.bin_vel_mmps, cfg.bin_acc_mmps2)

    def unload_bin_pos(self, bin_num):
        self.absolute_move(cfg.bin_heights_unload_mm[bin_num] + cfg.bin_unload_shift_mm, cfg.bin_vel_mmps, cfg.bin_acc_mmps2)