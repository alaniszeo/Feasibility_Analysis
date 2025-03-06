# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 08:59:38 2025

@author: AZ
"""

import colors
import matplotlib.pyplot as plt

def main():
    # Load colors
    # Define new colors
    color = colors.main()
    new_colors = [color['main']['teal'], color['main']['green'], color['main']['orange'], color['main']['fushia'], color['main']['blue'], color['main']['purple'], color['main']['red']]
    
    # Set default parameters
    plt.rcParams['font.family'] = 'Times New Roman'     # Default font
    plt.rcParams['font.size'] = 18                      # Default font size
    plt.rcParams['axes.facecolor'] = 'white'            # Background color of the axes
    plt.rcParams['axes.edgecolor'] = 'k'                # Color of the axes box
    plt.rcParams['axes.grid'] = True                    # Enable grid
    plt.rcParams['figure.figsize'] = (5,5)            # Default figure size
    plt.rcParams['lines.linewidth'] = 2                 # Default line width
    plt.rcParams['axes.titlesize'] = 'large'            # Default title size
    plt.rcParams['axes.labelsize'] = 'medium'           # Default label size
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=new_colors) # Default line colors
    
    return color
