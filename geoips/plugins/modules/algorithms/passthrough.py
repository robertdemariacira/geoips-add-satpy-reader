import logging

import numpy as np

LOG = logging.getLogger(__name__)

interface = "algorithms"
family = "xarray_to_xarray"
name = "passthrough"


def call(arrays):
    data = np.ones(10, 10)
    breakpoint()
    return data
