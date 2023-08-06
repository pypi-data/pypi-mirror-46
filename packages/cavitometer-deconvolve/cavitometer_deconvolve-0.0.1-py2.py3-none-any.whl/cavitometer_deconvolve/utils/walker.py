# -*- coding: utf-8 -*-
""" Walk directory structure

This module contains the codes for walking the directory structure.

"""

import numpy
from os import path, walk


def get_raw_files (top, extension='.csv'):
    """Get all raw files including their paths.

    Keyword arguments
    top -- top level directory
    extension -- extension of raw files (default '.csv')
    """
    files_list = []
    for folder, _, files in walk(top, topdown=False):
        for file_ in files:
            if path.splitext(file_)[1] == extension:
                filename = path.join(folder, file_)
                files_list.append(filename)
    return files_list


def get_folders (top, extension='.csv'):
    """Get directory structure for folders containing raw files.
        
    Keyword arguments
    top -- top level directory
    extension -- extension of raw files (default '.csv')
    """
    folders_list = []
    for folder, _, files in walk(top, topdown=False):
        for file_ in files:
            if path.splitext(file_)[1] == extension:
                folders_list.append(folder)
                break
    # Sort folders
    folders = numpy.sort(folders_list)
    return folders
