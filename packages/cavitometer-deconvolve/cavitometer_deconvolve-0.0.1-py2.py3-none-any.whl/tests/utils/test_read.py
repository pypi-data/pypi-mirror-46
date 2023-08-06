from unittest import TestCase

from os import sep

from cavitometer_deconvolve.utils import read


class TestRead(TestCase):
    UNITS = ['(ms)', '(mV)', '(mV)']
    SIGNAL = [ 0.00000000e+00, -4.48541100e+01, -5.18862200e-01]

    def test_units(self):
        units = read.get_units(f"..{sep}Measurements{sep}Two_Probes.csv")

        self.assertEqual((list(units)), self.UNITS)

    def test_read_signal(self):
        _, signal = read.read_signal(f"..{sep}Measurements{sep}Two_Probes.csv")

        self.assertEqual((list(signal[0])), self.SIGNAL)
