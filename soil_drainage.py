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

    (froot, layer_thickness) = calc_rooting_fraction()
    layered_extraction_model(layer_thickness, froot)

def layered_extraction_model(layer_thickness, froot):

    n_days = 365
    n_layers = 6

    # generate some vaguely sensible rainfall inputs
    np.random.seed(0)
    rainfall_max = 50.0 # arbitary
    rainfall_min = 0.0
    ppt = np.random.beta(0.04, 1.0, n_days) * (rainfall_max - rainfall_min)
    #plt.plot(ppt)
    #plt.show()

    # ignore soil & canopy evap just to make this simple
    soil_evap = 0.0
    canopy_evap = 0.0
    transpiration = 3.0 # mm d-1

    # Coarse sand / Loamy sand
    swilt = 0.072
    sfc = 0.301
    ssat = 0.398

    # initialise layers to max, volumetric water content (mm3 mm-3)
    layer_max = 0.9999 * ssat
    sw = np.zeros(n_layers)
    for i in range(n_layers):
        sw[i] = layer_max

    # just for plotting
    store = np.zeros((n_days, n_layers))

    for i in range(n_days):

        throughfall = ppt[i] - canopy_evap

        # water req from the next layer
        diff = 0.0
        for j in range(n_layers):

            # Update SW layer with draining water

            # Draining water is more than the layer can hold
            if sw[j] + (throughfall / layer_thickness[j]) > layer_max:
                sw[j] = layer_max

            # Fill up the layer with the drained water
            else:
                sw[j] += throughfall / layer_thickness[j]

            # Extract water for transpiration from the layer + water we
            # couldn't extract from the previous layer
            trans_from_layer = (transpiration * froot[j]) + diff
            max_trans_in_layer = max(0.0, sw[j] - swilt) * layer_thickness[j]
            diff = trans_from_layer - max_trans_in_layer

            # There isn't enough water in this layer to meet out layer
            # transpiration demands, so extract the maximum we can and save
            # the missing amount to take from the next layer.
            if diff > 0.0:
                # turn back into volumetric water content (mm3 mm-3)
                sw[j] -= max_trans_in_layer / layer_thickness[j]

            # We can take all the required transpiration from this layer
            else:
                # turn back into volumetric water content (mm3 mm-3)
                sw[j] -= trans_from_layer / layer_thickness[j]
                diff = 0.0

            # store for plotting purposes
            store[i,j] = sw[j]


    fig = plt.figure(figsize=(9,10))
    ax = fig.add_subplot(n_layers+1,1,1)
    ax.plot(ppt, color="red", ls="-")
    ax.set_ylabel("PPT (mm)")
    plt.setp(ax.get_xticklabels(), visible=False)
    count = 2
    for i in range(n_layers):
        ax = fig.add_subplot(n_layers+1,1,count)
        ax.axhline(y=ssat, ls="--", color="k")
        ax.plot(store[:,i], color="royalblue", ls="-")

        ax.set_xlim(0, 365)
        ax.set_ylim(swilt, 0.5)
        ax.locator_params(nbins=5, axis="y")
        ax.set_ylabel("SW layer %d" % (i+1))
        if count < 7:
            plt.setp(ax.get_xticklabels(), visible=False)

        count += 1
    plt.show()


def calc_rooting_fraction():

    m_2_cm = 100.0
    m_2_mm = 1000.0
    n_layers = 6
    root_beta = 0.9 #[0.7-1.0]
    soil_layers = np.zeros(n_layers)

    # Soil layer thickness in CABLE (m)
    #zse = np.array([0.022, 0.058, 0.154, 0.409, 1.085, 2.872])

    # Use CABLE's sizing, but rescaled over 2m as opposed to 4.6m
    #proportions = zse / np.sum(zse)
    #layer_thickness = 2.0 * proportions
    layer_thickness = np.array([ 0.01, 0.025, 0.067, 0.178, 0.472, 1.248])

    # Calculate froot from using rootbeta and soil depth
    # - Jackson et al. (1996) Oceologica, 108:389-411

    # fraction of root in each soil layer
    froot = np.zeros(n_layers)

    total_depth = 0.0
    for i in range(n_layers):
        total_depth += layer_thickness[i] * m_2_cm
        froot[i] = min(1.0, 1.0 - root_beta**total_depth)

    for i in range(n_layers-1, 0, -1):
        #print (i)
        froot[i] -= froot[i-1]

    #plt.plot(froot, np.cumsum(layer_thickness)*-1)
    #plt.ylabel("Depth (m)")
    #plt.xlabel("Fraction of roots [0-1]")
    #plt.show()
    #sys.exit()

    return (froot, layer_thickness * m_2_mm)



if __name__ == "__main__":

    main()
