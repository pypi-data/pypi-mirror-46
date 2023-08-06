# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utility functions for memory related operations."""
from typing import Any, Optional

import logging

import re
import sys
import subprocess

import numpy as np
import scipy
import pandas as pd

from .exceptions import ConfigException, ClientException


def get_all_ram(logger: Optional[logging.Logger] = None) -> int:
    """
    Get all RAM in bytes.

    :returns: The RAM on the machine.
    """
    try:
        if sys.platform == 'win32':
            from automl.client.core.common.win32_helper import Win32Helper
            return Win32Helper.get_all_ram()
        elif sys.platform == 'linux':
            memory_in_kb = int(subprocess
                               .check_output(("vmstat -s -S k | grep 'total memory' | grep -o '[[:digit:]]*'"),
                                             shell=True).strip())
            return memory_in_kb * 1000
        elif sys.platform == 'darwin':
            return int(subprocess.check_output(['sysctl', '-n', 'hw.memsize']).strip())
    except Exception as e:
        raise ClientException.from_exception(
            e, "Failed to get total memory on platform '{}': {}".format(sys.platform, e))

    raise ConfigException("{}: Unsupported platform. Cannot determine the total memory on the machine."
                          .format(sys.platform))


def get_available_physical_memory(logger: Optional[logging.Logger] = None) -> int:
    """
    Get available physical memory in bytes.

    :returns: The available physical memory on the machine.
    """
    try:
        if sys.platform == 'win32':
            from automl.client.core.common.win32_helper import Win32Helper
            return Win32Helper.get_available_physical_memory()
        elif sys.platform == 'linux':
            memory_in_kb = int(subprocess.check_output("vmstat -s -S k | grep 'free memory' | grep -o '[[:digit:]]*'",
                                                       shell=True).strip())
            return memory_in_kb * 1000
        elif sys.platform == 'darwin':
            """
            Returns output like this. Use regex to get all numbers and
            add all page counts. First value is page size.
            Available memory = page size * free page count
            Mach Virtual Memory Statistics: (page size of 4096 bytes)
            Pages free:                             1442394.
            Page size , Free page count.
            ['4096', '1442394']
            """
            output = re.findall(
                r'\d+', str(subprocess.check_output("vm_stat | grep -e 'Pages free' -e 'page size of'", shell=True)))
            available_memory = int(output[0]) * int(output[1])
            return available_memory
    except Exception as e:
        raise ClientException.from_exception(
            e, "Failed to get total memory on platform '{}': {}".format(sys.platform, e))

    raise ConfigException("{}: Unsupported platform. Unable to findout available memory.".format(sys.platform))


def get_data_memory_size(data: Any) -> int:
    """
    Return the total memory size of this object.

    This utility function currently supports approximate sizes of numpy ndarray,
    sparse matrix and pandas DataFrame.

    :param data: data object primarily for training
    :type data: numpy.ndarray or scipy.sparse or pandas.DataFrame or some python object
    :return: estimated memory size of the python object in bytes.
    """
    if scipy.sparse.issparse(data):
        memory = data.data.nbytes + data.indptr.nbytes + data.indices.nbytes            # type: int
    elif isinstance(data, pd.DataFrame):
        memory = data.memory_usage(index=True, deep=True).sum()
    elif isinstance(data, np.ndarray):
        if sys.getsizeof(data) > data.nbytes:
            memory = sys.getsizeof(data)
        else:
            memory = data.nbytes
    else:
        # For ndarrays and other object types, return memory size by sys.getsizeof()
        memory = sys.getsizeof(data)

    return memory
