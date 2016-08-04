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

    m_2_cm = 100.0
    n_layers = 6
    soil_layers = np.zeros(n_layers)

    # Soil layer thickness in CABLE (m)
    zse = np.array([0.022, 0.058, 0.154, 0.409, 1.085, 2.872])

    # Use CABLE's sizing, but rescale over 2m as opposed to 4.6m
    proportions = zse / np.sum(zse)
    soil_layer_thickness = 2.0 * proportions
    print(soil_layer_thickness)
    # Calculate froot from using rootbeta and soil depth
    # - Jackson et al. (1996) Oceologica, 108:389-411

    # fraction of root in each soil layer
    froot = np.zeros(n_layers)

    root_beta = 0.95 #[0.7-1.0]
    total_depth = 0.0
    for i in range(n_layers):
        total_depth += soil_layer_thickness[i] * m_2_cm
        froot[i] = min(1.0, 1.0 - root_beta**total_depth)


    #plt.plot(np.cumsum(soil_layer_thickness), froot)
    #plt.xlabel("Depth (m)")
    #plt.ylabel("Fraction of roots [0-1]")
    #plt.show()





if __name__ == "__main__":

    main()
