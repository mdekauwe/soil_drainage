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

    (froot, soil_layer_max) = calc_rooting_fraction()
    #tipping_bucket_model(soil_layer_max, froot)
    layered_extraction_model(soil_layer_max, froot)

def layered_extraction_model(soil_layer_max, froot):

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

    # Coarse sand/Loamy sand
    swilt = 0.072
    sfc = 0.301
    ssat = 0.398


    # initialise layers to max
    sw = np.zeros(n_layers)
    for i in range(n_layers):
        sw[i] = 0.9999 * ssat



    # just for plotting
    store = np.zeros((n_days, n_layers))

    for i in range(n_days):

        throughfall = ppt[i] - canopy_evap
        delta = throughfall - transpiration #- soil_evap

        drainage = 0.0
        extracted = 0.0

        diff = 0.0
        xxd = 0.0
        for j in range(n_layers):

            xx = transpiration * froot[j] + diff
            diff = max(0.0, sw[j] - swilt) * soil_layer_max[j]

            xxd = xx - diff


            if xxd > 0.0:

                sw[j] -= diff / soil_layer_max[j]
                diff = xxd

            else:

                sw[j] -= xx / soil_layer_max[j]
                diff = xxd



            """
            print(xx, diff, sw[j]/soil_layer_max[j])
            sys.exit()
            # if we need more water than we have available, only offer up what
            # the layer held
            if sw[j] + delta < 0.0:
                extracted += sw[j]
                sw[j] = 0.0

            # if we have more water than we can store, tip excess into the
            # next layer
            elif sw[j] + delta > soil_layer_max[j]:
                drainage += (sw[j] + delta) - soil_layer_max[j]
                sw[j] = soil_layer_max[j]

            # the layer can meet the demands for water comfortably
            else:
                extracted += delta
                sw[j] += delta
                delta = 0.0
            """

            # store for plotting purposes
            store[i,j] = sw[j]


    fig = plt.figure(figsize=(9,10))
    ax = fig.add_subplot(n_layers+1,1,1)
    ax.plot(ppt, color="red", ls="-")
    ax.set_ylabel("PPT (mm)")
    count = 2
    for i in range(n_layers):
        ax = fig.add_subplot(n_layers+1,1,count)
        #ax.axhline(y=soil_layer_max[i], ls="--", color="k")
        ax.plot(store[:,i], color="royalblue", ls="-")

        ax.set_xlim(0, 365)
        #ax.set_ylim(0, soil_layer_max[i]+(soil_layer_max[i]*0.1))
        ax.set_ylabel("SW layer %d" % (i+1))
        if count < 6:
            plt.setp(ax.get_xticklabels(), visible=False)

        count += 1
    plt.show()

def tipping_bucket_model(soil_layer_max, froot):

    n_days = 365
    n_layers = 6

    # initialise layers to max
    sw = soil_layer_max.copy()

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

    # just for plotting
    store = np.zeros((n_days, n_layers))

    for i in range(n_days):

        throughfall = ppt[i] - canopy_evap
        delta = throughfall - transpiration #- soil_evap

        drainage = 0.0
        extracted = 0.0

        for j in range(n_layers):

            # if we need more water than we have available, only offer up what
            # the layer held
            if sw[j] + delta < 0.0:
                extracted += sw[j]
                sw[j] = 0.0

            # if we have more water than we can store, tip excess into the
            # next layer
            elif sw[j] + delta > soil_layer_max[j]:
                drainage += (sw[j] + delta) - soil_layer_max[j]
                sw[j] = soil_layer_max[j]

            # the layer can meet the demands for water comfortably
            else:
                extracted += delta
                sw[j] += delta
                delta = 0.0

            # store for plotting purposes
            store[i,j] = sw[j]


    fig = plt.figure(figsize=(9,10))
    ax = fig.add_subplot(n_layers+1,1,1)
    ax.plot(ppt, color="red", ls="-")
    ax.set_ylabel("PPT (mm)")
    count = 2
    for i in range(n_layers):
        ax = fig.add_subplot(n_layers+1,1,count)
        ax.axhline(y=soil_layer_max[i], ls="--", color="k")
        ax.plot(store[:,i], color="royalblue", ls="-")

        ax.set_xlim(0, 365)
        ax.set_ylim(0, soil_layer_max[i]+(soil_layer_max[i]*0.1))
        ax.set_ylabel("SW layer %d" % (i+1))
        if count < 6:
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

    # Use CABLE's sizing, but rescale over 2m as opposed to 4.6m
    #proportions = zse / np.sum(zse)
    #soil_layer_thickness = 2.0 * proportions
    #soil_layer_thickness = np.array([ 0.01, 0.025, 0.067, 0.178, 0.472, 1.248])
    soil_layer_thickness = np.array([0.022, 0.058, 0.154, 0.409, 1.085, 2.872])

    # Calculate froot from using rootbeta and soil depth
    # - Jackson et al. (1996) Oceologica, 108:389-411

    # fraction of root in each soil layer
    froot = np.zeros(n_layers)

    total_depth = 0.0
    for i in range(n_layers):
        total_depth += soil_layer_thickness[i] * m_2_cm
        froot[i] = min(1.0, 1.0 - root_beta**total_depth)

    for i in range(n_layers-1, 0, -1):
        #print (i)
        froot[i] -= froot[i-1]

    #plt.plot(froot, np.cumsum(soil_layer_thickness)*-1)
    #plt.ylabel("Depth (m)")
    #plt.xlabel("Fraction of roots [0-1]")
    #plt.show()
    #sys.exit()

    return (froot, soil_layer_thickness * m_2_mm)



if __name__ == "__main__":

    main()
