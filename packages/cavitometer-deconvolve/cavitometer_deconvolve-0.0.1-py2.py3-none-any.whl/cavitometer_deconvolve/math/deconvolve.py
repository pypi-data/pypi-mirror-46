# -*- coding: utf-8 -*-
""" Deconvolution module

This module contains the codes for deconvolution of time signals.

"""

from numpy import vectorize, linspace, sqrt, ndarray
# from scipy.signal import blackman
from scipy.interpolate import interp1d

from pyfftw import interfaces

from cavitometer_deconvolve.math.FFT import fast_fourier_transform, two_sided_to_one, one_sided_to_two
from cavitometer_deconvolve.math.convert import dB_to_V
from cavitometer_deconvolve.hardware.sensitivities import Probe, PreAmplifier


def deconvolution(time: ndarray, signal: ndarray, units: list,
                  probe: Probe, pre_amp: PreAmplifier = None) -> tuple:
    """Converts the voltage signal to pressures.

    1. Interpolate the get_sensitivities and amplification factors in the FFT frequency range.
    2. Apply deconvolution formula

    :param time: the time numpy array
    :param signal: the signal numpy array
    :param units: the SI units for the time and signal arrays
    :param probe: Probe instance containing the sensitivity values
    :param pre_amp: PreAmplifier instance containing the pre-amp factors
    :rtype: tuple
    """
    # For zero padding, uncomment concatenate lines if required
    # N0 = len(x1)

    # w = blackman(len(y1))
    frequency, fourier = fast_fourier_transform(time, signal, units)

    decibel_to_volts = vectorize(dB_to_V)
    # order = 3 # spline order, 1 = linear, 2 = quad, 3 = cubic ...
    # smooth = 0.0

    # 1. Interpolation
    sensitivity_function = interp1d(probe.frequencies,
                                    decibel_to_volts(probe.get_sensitivities()),
                                    kind='nearest',
                                    fill_value="extrapolate",
                                    )
    # Numerator of convolution operation
    # sensitivity_function.set_smoothing_factor(smooth)

    if pre_amp:
        amplification_factor = interp1d(pre_amp.frequencies,
                                        pre_amp.get_sensitivities(),
                                        kind='nearest',
                                        fill_value="extrapolate",
                                        )

        # 2. Numerator of deconvolution formula
        numerator = sensitivity_function(frequency[:len(frequency)//2+1]) \
                    / (amplification_factor(frequency[:len(frequency)//2+1]) * 1.1)
    else:
        numerator = sensitivity_function(frequency[:len(frequency)//2+1])/1.1

    pressure_fft = 1e3*two_sided_to_one(fourier.real)/numerator
    pressure_frequency = linspace(0, frequency[len(frequency)//2-1], len(pressure_fft))
    pressure_signal = interfaces.scipy_fftpack.ifft(one_sided_to_two(pressure_fft))\
                         * sqrt(len(one_sided_to_two(pressure_fft)))

    return pressure_frequency, pressure_fft, pressure_signal
