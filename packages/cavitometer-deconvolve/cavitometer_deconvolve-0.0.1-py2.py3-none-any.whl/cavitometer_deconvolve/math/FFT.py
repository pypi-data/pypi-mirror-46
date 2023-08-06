# -*- coding: utf-8 -*-
""" FFT module

This module contains the FFT codes.

"""

from __future__ import division

from numpy import fft, empty, ndarray
from pyfftw import interfaces


def fast_fourier_transform(time: ndarray, signal: ndarray, units: list) -> tuple:
    """Performs the Fast Fourier Transform on the time signal.

    :param time: the time numpy array
    :param signal: the signal numpy array
    :param units: the SI units for the time and signal arrays
    :return: frequency, fourier transform
    :rtype: tuple
    """
    # If units in ms, multiply step time by 1e-3
    step = (time[1] - time[0])
    if 'ms' in units[0]:
        step *= 1.0e-3
    # Convert voltage to volts if mV
    if 'mV' in units[1]:
        signal = signal * 1.0e-3

    # N0 = len(s)
    # w = blackman(N0)
    fourier = interfaces.numpy_fft.fft(signal, norm="ortho")
    # fourier = fft.fft(s, norm="ortho")
    freq = fft.fftfreq(len(fourier), step)

    return freq, fourier


def two_sided_to_one(two_sided: ndarray) -> ndarray:
    """Two sided FFT to one.

    numpy/scipy FFT functions yield two sided spectra while calibration is on one
    sided spectra. Conversion is required before deconvolution process.

    :param two_sided: two sided FFT
    :rtype: ndarray
    """
    one_sided = empty(len(two_sided) // 2 + 1)
    one_sided[1:len(two_sided) // 2 + 1] = 2 * two_sided[0:len(two_sided) // 2]
    one_sided[0] = two_sided[len(two_sided) // 2]
    return one_sided


def one_sided_to_two(one_sided: ndarray) -> ndarray:
    """One sided FFT to two.

    Revert to two sided FFT before inverse fourier transform.

    :param one_sided: one sided FFT
    :rtype: ndarray
    """
    two_sided = empty(2 * len(one_sided) - 1)
    two_sided[0:len(one_sided) - 1] = 0.5 * one_sided[1:]
    two_sided[len(one_sided) - 1] = one_sided[0]
    two_sided[len(one_sided):] = 0.5 * one_sided[1:]
    return two_sided
