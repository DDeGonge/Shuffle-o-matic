__version__ = '0.1.0'

from gpiozero import LED
import math

class Motor(object):
    def __init__(self, step_pin, dir_pin, limit_pin, stepspermm):
    	self.pos_mm = 0
    	self.steppin = LED(step_pin)
    	self.dirpin = LED(dir_pin)
    	self.steps_per_mm = stepspermm
    	self.error = 0.

    def home(self):
    	print()

   	def relative_move(self, distance_mm, velocity_mmps, accel_mmps2):
   		steps = self._calc_steps(distance_mm)
   		minPause = 1 / (velocity_mmps * self.steps_per_mm)
   		rampSlope = 0
   		rampLen = 0

   	def absolute_move(self, position_mm, velocity_mmps, accel_mmps2):
   		return self.relative_move(position_mm - self.pos_mm, velocity_mmps, accel_mmps2)

    def pos_mm(self):
    	return pos_mm

    def _calc_steps(self, dist_mm):
    	steps_tot = (dist_mm + self.error) * self.steps_per_mm
    	steps = math.floor(steps_tot)
    	self.error = steps_tot - steps
    	return steps