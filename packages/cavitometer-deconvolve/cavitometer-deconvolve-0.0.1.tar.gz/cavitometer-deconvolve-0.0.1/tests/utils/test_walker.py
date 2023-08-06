from unittest import TestCase

from os import sep

from cavitometer_deconvolve.utils import walker


class TestWalker(TestCase):
    FOLDERS = [f"..{sep}Measurements"]
    FILES = [f"..{sep}Measurements{sep}Two_Probes.csv"]

    def test_folders(self):
        folders = walker.get_folders(f"..{sep}")

        self.assertEqual((list(folders)), self.FOLDERS)

    def test_files(self):
        files = walker.get_raw_files(f"..{sep}")

        self.assertEqual((list(files)), self.FILES)
