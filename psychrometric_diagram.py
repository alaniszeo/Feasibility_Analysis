# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 08:58:47 2025

@author: Alanis Zeoli

Objective:
    Draw a psychrometric chart

/!\ The function figure.default should be launched before launching a
psychrometric chart

Inputs:
    The number of inputs can be modified depending on what is needed
    'AxesValue' is a 1x4 vector
    'Units' specifies the units of the specific humidity (default = [kg/kg])
    'Type' is a string with is either 'Carrier' or 'Mollier' (default =
    'Carrier'
    'IsoB' is a 'yes'/'no' string stating if iso-wet bulb lines should be
    drawn
"""

import numpy as np
import matplotlib.pyplot as plt
from CoolProp.CoolProp import HAPropsSI

def plot_diagram(ax=None,**kwargs):
    if ax is None:
        fig, ax = plt.subplots()
       
    ax.grid(False)
    
    grey = (0.6, 0.6, 0.6)
    darkgrey = (0.4, 0.4, 0.4)

    # Default values
    units = 1
    w_label = r'Humidity Ratio [kg/kg]'
    chart_type = 'Carrier'

    # Parse keyword arguments
    if 'Units' in kwargs:
        if 'k' in kwargs['Units']:
            units = 1
            w_label = 'Humidity Ratio [kg/kg]'
        else:
            units = 1000
            w_label = 'Humidity Ratio [g/kg]'

    if 'Type' in kwargs:
        chart_type = kwargs['Type']

    if 'AxesValue' in kwargs:
        axes_value = kwargs['AxesValue']
    else:
        if chart_type == 'Carrier':
            axes_value = [0, 50, 0, 0.05*units]
        else:
            axes_value = [0, 0.05*units, 0, 50]

    # Determine temperature limits
    if chart_type == 'Carrier':
        T_min, T_max = axes_value[0], axes_value[1]
        ax.set_xlabel('Temperature [°C]')
        ax.set_xlim(T_min, T_max)
        ax.set_ylabel(w_label)
        ax.set_ylim(axes_value[2], axes_value[3])
    else:
        T_min, T_max = axes_value[2], axes_value[3]
        ax.set_ylabel('Temperature [°C]')
        ax.set_ylim(T_min, T_max)
        ax.set_xlabel(w_label)
        ax.set_xlim(axes_value[0], axes_value[1])

    T_plot = np.arange(T_min, T_max+1, 1)

    # Check if iso-wet bulb should be drawn
    isoB = kwargs.get('IsoB', 'yes')

    RH = np.arange(0.1, 1.1, 0.1)
    
    P = 101325  # Pressure in Pa

    for i in range(len(RH)):
        w_RH = [HAPropsSI('W', 'T', T + 273.15, 'RH', RH[i], 'P', P) for T in T_plot]

        linewidth = 3 if RH[i] == 1 else 0.5
        linecolor = darkgrey if RH[i] == 1 else grey
        linestyle = '-' if RH[i] == 1 else '--'

        if chart_type == 'Carrier':
            ax.plot(T_plot, np.array(w_RH)*units, linestyle=linestyle, color=linecolor, linewidth=linewidth)
        else:
            ax.plot(np.array(w_RH)*units, T_plot, linestyle=linestyle, color=linecolor, linewidth=linewidth)

    if isoB == 'yes':
        T_wb = np.arange(0, T_plot[-1] + 1, 5)
        for T_w in T_wb:
            # Calculate wet bulb line
            w_wb = [HAPropsSI('W', 'T', T_w + 273.15, 'RH', 1, 'P', P)]
            T_db = [T_w]

            method = 'w_min'
            T_max = T_plot[-1]

            for _ in range(2):
                if method == 'w_min':
                    w_wb.append(0.0005)
                    T_db.append(HAPropsSI('T', 'B', T_w + 273.15, 'W', w_wb[-1], 'P', P) - 273.15)

                    if T_db[-1] > T_max - 10:
                        method = 'T_max'
                else:
                    T_db.append(T_max)
                    w_wb.append(HAPropsSI('W', 'T', T_db[-1] + 273.15, 'B', T_w + 273.15, 'P', P))

            if chart_type == 'Carrier':
                ax.plot(T_db, np.array(w_wb)*units, color=grey, linewidth=1)
            else:
                ax.plot(np.array(w_wb)*units, T_db, color=grey, linewidth=1)
                
    return ax