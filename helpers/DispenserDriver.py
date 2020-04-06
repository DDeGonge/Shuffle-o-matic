__version__ = '0.1.0'

class Dispenser(object):
    def __init__(self, serial_device):
        self.sd = serial_device

    def dispense_card(self):
        resp = self.sd.command('c')
        if "JAM" in resp:
            return False
        return True

    def baseline_motor_cur(self):
        self.sd.command('b')

    def enable_motor(self):
        print('Enabling dispense motor')

    def disable_motor(self):
        print('Disabling dispense motor')
