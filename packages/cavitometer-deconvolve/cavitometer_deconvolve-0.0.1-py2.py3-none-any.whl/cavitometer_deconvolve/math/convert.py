# -*- coding: utf-8 -*-
""" Conversion module

This module contains the codes for converting between different dB types.

"""

from numpy import log10


def dBu_to_dBV(dBu):
    """Converts dBu to dBV."""
    return dBu + 20*log10(0.775)


def V_to_dBu(V):
    """Converts V to dBu."""
    return 20*log10(V/0.775)


def V_to_dBV(V):
    """Converts V to dBu."""
    return 20*log10(V/1.0)


def dBu_to_V (dBu):
    """Converts dBu to V."""
    return 0.775 * 10**(dBu/20.)


def dBV_to_V (dBV):
    """Converts dBV to V."""
    return 1.0 * 10**(dBV/20.)


def dB_to_V(dB):
    """Converts dB to V."""
    return 1e9 * 10**(dB / 20)
