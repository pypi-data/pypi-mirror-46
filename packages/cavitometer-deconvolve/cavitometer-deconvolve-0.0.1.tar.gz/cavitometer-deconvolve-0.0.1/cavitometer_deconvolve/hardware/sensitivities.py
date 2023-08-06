# -*- coding: utf-8 -*-
""" Sensitivities of hydrophones and amplification factors

This file contains the classes for the probes (hydrophones) and pre-amplifiers.

"""

from numpy import genfromtxt, ndarray


class Probe:
    """Contains the probe sensitivity values.

    Probes are calibrated when resting vertically (i = 0) or at 45 deg (i = 1).
    """
    def __init__(self, filename: str) -> None:
        """Initializes the frequency and sensitivity arrays from file

        :param filename: the name of the probe sensitivity values csv file
        :rtype: None
        """
        self._filename = filename
        _file_array = genfromtxt(filename,
                                 delimiter=',',
                                 skip_header=1,
                                 usecols=None,
                                 unpack=False,
                                 )
        self._frequencies = _file_array[:, 0]
        self._sensitivities = _file_array[:, 1:]

    @property
    def frequencies(self) -> ndarray:
        """Return frequencies

        :rtype: ndarray
        """
        return self._frequencies

    def get_sensitivities(self, i: int = 0) -> ndarray:
        """Return get_sensitivities.

        :param i:  0 = vertical probe, 1 = probe inclined at 45 deg.
        :rtype: ndarray
        """
        return self._sensitivities[:, i]

    def __repr__(self):
        return self._filename

    def __unicode__(self):
        return self._filename

    def __str__(self):
        return self._filename


class PreAmplifier(Probe):
    def get_sensitivities(self) -> ndarray:
        """Return get_sensitivities. No orientation.

        :rtype: ndarray
        """
        return self._sensitivities[:, 0]
