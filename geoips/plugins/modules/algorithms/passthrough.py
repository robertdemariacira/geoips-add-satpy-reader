"""Just passes data through as a test."""

import logging

import numpy as np

LOG = logging.getLogger(__name__)

interface = "algorithms"
family = "xarray_dict_to_xarray"
name = "passthrough"


def call(xarray_dict):
    data = np.arange(10)
    breakpoint()
    return data
