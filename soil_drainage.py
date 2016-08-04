#!/usr/bin/env python

"""
Implement a simple multi-layer soil layer scheme to test I have implemented
the Richards' equation correctly
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

__author__  = "Martin De Kauwe"
__version__ = "1.0 (04.08.2016)"
__email__   = "mdekauwe@gmail.com"


def main():

    n_layers = 10
    soil_layers = np.zeros(n_layers)

    # soil layer thickness in CABLE (m)
    zse = np.array([0.022, 0.058, 0.154, 0.409, 1.085, 2.872])

    # Use CABLE's sizing, but rescale over 2m as opposed to 4.6m
    proportions = zse / np.sum(zse)
    soil_layer_thickness = 2.0 * proportions



    # fraction of root in each soil layer
    #froot


if __name__ == "__main__":

    main()
