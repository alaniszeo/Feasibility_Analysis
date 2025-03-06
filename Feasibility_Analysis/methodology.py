# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 13:11:48 2025

@author: Alanis Zeoli
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from CoolProp.CoolProp import HAPropsSI

import psychrometric_diagram as psychro
import plot_default

# Definition of a class for the components
class component():
    def __init__(self,type_name,epsilon):
        self.type = type_name
        self.epsilon = epsilon
        
    def get_T_lim(self,T_su,T_ex):
        epsilon = self.epsilon
        
        if self.type != 'DW':
            T_lim = T_su + (T_ex-T_su)/epsilon
        else:
            T_lim = T_su + (T_ex-T_su)*epsilon
        return T_lim
    
    def get_T_su(self,T_lim,T_ex):
        epsilon = self.epsilon
        
        if self.type != 'DW':
            T_su = (T_ex-epsilon*T_lim)/(1-epsilon)
        else:
            T_su = (T_lim-epsilon*T_ex)/(1-epsilon)
        return T_su

# Returns the temperature based on spec. humidity and line coefficients 
def get_T(w,lim):
    m = lim[0]
    p = lim[1]
    
    T = (w-p)/m
    return T

# Returns the spec. humidity based on temperature and line coefficients
def get_w(T,lim):
    m = lim[0]
    p = lim[1]
    
    w = m*T+p
    return w    

# Returns m and p coefficient of the line between (T1,w1) and (T2,w2)
def linear_interp(T1,w1,T2,w2):
    m = (w2-w1)/(T2-T1)
    p = w1 - m*T1
    return [m,p]

# Returns the couple (T,w) at the intersection between 2 lines
def lines_intersection(lim1,lim2):
    if len(lim1)>1:
        m1 = lim1[0]
        p1 = lim1[1]
        
    if len(lim2)>1:
        m2 = lim2[0]
        p2 = lim2[1]
        
    if len(lim1)>1 and len(lim2)>1:
        x = (p2-p1)/(m1-m2)
        y = m1*x + p1
    elif len(lim1)>1:
        x = lim2[0]
        y = m1*x + p1
    elif len(lim2)>1:
        x = lim1[0]
        y = m2*x + p2
    else:
        print("There is no intersection between those 2 lines")
        return
    return x,y

# Intersection between a line and the saturation curve
def curve_intersection(lim):
    T_min = 0
    T_max = 50
    T_dp = 0
    T = -100
    
    while abs(T_dp-T)>1e-2:
        T = (T_min+T_max)/2
        w = get_w(T,lim)
        T_dp = saturation(w)
        
        if T_dp<T:
            T_max = T
        else:
            T_min = T
    return T, w

# Polynomial equation for the saturation curve. Returns T based on w
def saturation(w):
    coef = [7.2356e12, -1.2955e12, 9.5015e10, -3.6881e9, 8.2083e7, -1.0783e6, 9.1033e3, -22.7387]
    N = len(coef)
    T = 0
    for i in range(N):
        T = T + coef[N-i-1]*w**i
    return T

# Definition of a zone based on its limits
def zone_def(T_out,w_out,lim,cooling_zone):
    
    if len(lim)>1:
        m = lim[0]
        p = lim[1]
        
        zone_index = np.where(w_out<m*T_out+p)
        
    else:
        zone_index = np.where(T_out<lim)
          
    new_zone = np.intersect1d(cooling_zone,zone_index)
    new_cooling_zone = np.setdiff1d(cooling_zone,zone_index)
    nb_hours_zone = len(new_zone)
    
    return new_cooling_zone, new_zone, nb_hours_zone
    

def main(components,params,climate_data=None,chart='yes',hum='yes'):
    # Definition of constants
    P_atm = 101325
    to_K = 273.15
    to_C = -273.15
    
    # Initialise plot
    if chart == 'yes':
        color = plot_default.main()
        main_colors = color['main']
        fig, ax = plt.subplots(figsize=(7,7))
        ax = psychro.plot_diagram(ax)
        
        lim_data = {
            'Heating': ['$T_{su,min}$', main_colors['darkblue']],
            'Ventilation': ['$T_{su,max}$', main_colors['teal']],
            'DEC': ['$T_{wb,max}$', main_colors['darkgreen']],
            'DEC (hum)': ['$\epsilon_{wb,DEC}$', main_colors['verydarkgreen']],
            'IEC': ['$\epsilon_{wb,s,IEC}$', main_colors['darkorange']],
            'IEC (hum)': ['$\epsilon_{wb,s,IEC}$ (hum)', main_colors['verydarkorange']],
            'DECS': ['$\epsilon_{h,DW}$', main_colors['darkpink']],
            'DECS pre-cooling': ['$\epsilon_{dp,D-IEC}$', main_colors['black']] 
            }
        limits = pd.DataFrame(data=lim_data,index=['legend','color'])
        
        if climate_data is not None:
            Zone = {}
            marker_size = 6
            mode_colors = {
                'Heating': main_colors['teal'],
                'Ventilation': main_colors['blue'],
                'DEC': main_colors['lightgreen'],
                'DEC (hum)': main_colors['green'],
                'IEC': main_colors['lightsalmon'],
                'IEC (hum)': main_colors['orangesalmon'],
                'DECS': main_colors['pink'],
                'DECS pre-cooling': main_colors['fushia'],
                'Active cooling': main_colors['darkred']
                }
    else:
        ax = []
    
    # Parameters
    if 'w_in' in params.keys(): # Check to compute w_in from T_in and RH_in
        w_in = params['w_in']
    else:
        w_in = 0.009
        print('The value of w_in has not been provided and has been set to the default value of 9 g/kg.')
        
    if 'T_wb_in' in params.keys():
        T_wb_in = params['T_wb_in']
    else:
        if 'T_in' in params.keys():
            T_in = params['T_in']
        else:
            T_in = 24
            print('The value of T_in has not been provided and has been set to the default value of 24°C.')
                
        T_wb_in = HAPropsSI('B','T',T_in+to_K,'W',w_in,'P',P_atm)+to_C
    
    if 'T_su_min' in params.keys():
        T_su_min = params['T_su_min']
    else:
        T_su_min = 16 # Default value
        print('The value of T_su_min has not been provided and has been set to the default value of 16°C.')
        
    if 'T_su_max' in params.keys():
        T_su_max = params['T_su_max']
    else:
        T_su_max = 20 # Default value
        print('The value of T_su_max has not been provided and has been set to the default value of 20°C.')
        
    if 'T_reg' in params.keys():
        T_reg = params['T_reg']
    else:
        T_reg = 60 # Default value
        print('The value of T_reg has not been provided and has been set to the default value of 60°C.')
    T_max = T_reg # Make sure to compute max values for the regerantion temperature
    w_min = 0
    
    # Include calculation of w_out here instead of main
    if climate_data is not None:
        T_out = climate_data['T_dry'].to_numpy()
        w_out = climate_data['w'].to_numpy()
        nb_data = len(T_out)
        
        # Define hours during which passive operation is possible
        all_hours = np.arange(0,nb_data,1)
        if hum == 'yes':
            cooling_zone = all_hours
        else:
            cooling_zone = np.where(w_out<w_in)[0]
            
        active_zone = np.setdiff1d(all_hours,cooling_zone)
    
    nb_hours = {} # Dictionnary containing the number of operating hours in each mode
    mode_list = []
    lim = {} # Dictionnary containing the values of m and p to determine the limits of each operation mode
    T_lim = {} # Values of limit temperatures used to plot limits
    w_lim = {} # Values of limit spec. humidities used to plot limits
    
    " ------------- Step 1 - Heating ---------------- "
    mode = 'Heating'
    mode_list.append(mode)
    
    lim[mode] = np.array([T_su_min]) # Vertical line
    T_lim[mode] = np.array([T_su_min, T_su_min]) 
    w1 = w_min
    w2 = HAPropsSI('W','T',T_su_min+to_K,'RH',1,'P',P_atm)
    w_lim[mode] = np.array([w1, w2])
        
    if chart == 'yes':
        limits.loc['legend',mode] = limits[mode]['legend']+" = "+str(T_su_min)+"°C"
    
    " ------------- Step 2 - Ventilation ---------------- "
    mode = 'Ventilation'
    mode_list.append(mode)
    
    lim[mode] = np.array([T_su_max]) # Vertical line
    T_lim[mode] = np.array([T_su_max, T_su_max]) 
    w1 = w_min
    w2 = HAPropsSI('W','T',T_su_max+to_K,'RH',1,'P',P_atm)
    w_lim[mode] = np.array([w1, w2])
        
    if chart == 'yes':
        limits.loc['legend',mode] = limits[mode]['legend']+" = "+str(T_su_max)+"°C"
        
    " ------------- Step 3 - DEC ---------------- "
    if 'DEC' in components.keys():
        # Part 1 - No humidification of the building
        mode = 'DEC'
        mode_list.append(mode)
        
        w1 = w_in
        w2 = w_min

        T1 = T_su_max
        T_wb_max = HAPropsSI('B','T',T1+to_K,'W',w1,'P',P_atm)+to_C
        T2 = HAPropsSI('T','B',T_wb_max+to_K,'W',w2,'P',P_atm)+to_C

        m, p = linear_interp(T1,w1,T2,w2)
        lim[mode] = np.array([m, p])
        
        T1, w1 = lines_intersection(lim['Ventilation'],lim['DEC'])
        w_lim[mode] = np.array([w1, w2])
        T_lim[mode] = np.array([T1, T2])
            
        # Part 2 - Humidification of th building accepted
        if hum == 'yes':
            mode = 'DEC (hum)'
            mode_list.append(mode)
            DEC = components['DEC']
            
            T1 = T_su_max
            w1 = max(w_lim['Ventilation'])
            
            T2 = T1+5
            T_wb_max = DEC.get_T_lim(T2,T_su_max)
            w2 = HAPropsSI('W','B',T_wb_max+to_K,'T',T2+to_K,'P',P_atm)
            
            m, p = linear_interp(T1,w1,T2,w2)
            lim[mode] = np.array([m, p])
            
            T2, w2 = lines_intersection(lim['DEC (hum)'],lim['DEC'])
            w_lim[mode] = np.array([w1, w2])
            T_lim[mode] = np.array([T1, T2])
                
            if chart == 'yes':
                limits.loc['legend',mode] = limits[mode]['legend']+" = "+str(DEC.epsilon)
                
        " ------------- Step 4 - IEC ---------------- "
        if 'IEC' in components.keys(): # In the future change for IEC and IEC+DEC
            # Part 1 - No humidification of the building
            mode = 'IEC'
            mode_list.append(mode)
            IEC = components['IEC']
            
            w1 = w_in
            T1 = T_su_max
            
            # The evolution inside the IEC is sensible before arriving to the DEC inlet
            w2 = w_min
            T_ex = get_T(w2,lim['DEC'])
            T2 = IEC.get_T_su(T_wb_in,T_ex)
    
            m, p = linear_interp(T1,w1,T2,w2)
            lim[mode] = np.array([m, p])
            
            T1, w1 = lines_intersection(lim['IEC'],lim['DEC (hum)'])
            w_lim[mode] = np.array([w1, w2])
            T_lim[mode] = np.array([T1, T2])
            
            if chart == 'yes':
                limits.loc['legend',mode] = limits[mode]['legend']+" = "+str(IEC.epsilon)
                
            # Part 2 - Humidification of th building accepted
            if hum == 'yes':
                mode = 'IEC (hum)'
                mode_list.append(mode)
                
                T1 = T_su_max
                w1 = max(w_lim['Ventilation'])
                
                # The evolution inside the IEC is sensible before arriving to the DEC inlet
                w2 = w_min
                T_ex = get_T(w2,lim['DEC (hum)'])
                T2 = IEC.get_T_su(T_wb_in,T_ex) # The minimum reachable temperature is T_wb_in because
                
                m, p = linear_interp(T1,w1,T2,w2)
                lim[mode] = np.array([m, p])
                
                w_lim[mode] = np.array([w1, w2])
                T_lim[mode] = np.array([T1, T2])
                    
                if chart == 'yes':
                    limits.loc['legend',mode] = limits[mode]['legend']+" = "+str(IEC.epsilon)
             
            " ------------- Step 5 - DECS ---------------- "
            if 'DW' in components.keys():
                mode = 'DECS'
                mode_list.append(mode)
                DW = components['DW']
                
                T_ex = T_reg - 10 # Fix a constant pinch point in the DW
                
                T1 = T_ex
                w1 = get_w(T1,lim['IEC (hum)'])
                
                T2 = T1-10
                T2h = DW.get_T_lim(T2, T_ex)
                h2 = HAPropsSI('H','T',T2h+to_K,'W',w1,'P',P_atm) # By definition of T2h
                w2 = HAPropsSI('W','T',T2+to_K,'H',h2,'P',P_atm) # By definition of the isenthalpic efficiency
                
                m, p = linear_interp(T1,w1,T2,w2)
                lim[mode] = np.array([m, p])
                
                T2, w2 = curve_intersection(lim[mode])
                w_lim[mode] = np.array([w1, w2])
                T_lim[mode] = np.array([T1, T2])
                
                if chart == 'yes':
                    limits.loc['legend',mode] = limits[mode]['legend']+" = "+str(DW.epsilon)
                
                " ------------- Step 6 - DECS with pre-cooling ---------------- "
                if 'D-IEC' in components.keys():
                    mode = 'DECS pre-cooling'
                    mode_list.append(mode)
                    D_IEC = components['D-IEC']
                    
                    T1 = min(T_lim['DECS'])
                    w1 = max(w_lim['DECS'])
                    
                    w2 = w_in # Arbitrary
                    T_ex = get_T(w2,lim['DECS']) # Temperature at the inlet of the DW
                    T_dp = HAPropsSI('D','W',w2,'T',T_ex+to_K,'P',P_atm)+to_C # Minimum achievable temperature
                    T2 = D_IEC.get_T_su(T_dp, T_ex)
                    
                    m, p = linear_interp(T1,w1,T2,w2)
                    lim[mode] = np.array([m, p])
                    
                    w_lim[mode] = np.array([w1, w2])
                    T_lim[mode] = np.array([T1, T2])
                    
                    if chart == 'yes':
                        limits.loc['legend',mode] = limits[mode]['legend']+" = "+str(D_IEC.epsilon)
    
    " ------------- Active cooling ---------------- "
    mode = 'Active cooling'
    mode_list.append(mode)
    
    lim[mode] = np.array([0,0.05]) # Arbitrary but makes sure that all points are in it
    
    " ------------- Summary of operation mode hours ---------------- "
    if climate_data is not None:
        for mode in mode_list:
            cooling_zone, mode_zone, nb_hours_mode = zone_def(T_out,w_out,lim[mode],cooling_zone)
            Zone[mode] = mode_zone
            nb_hours[mode] = nb_hours_mode
            
            result = mode + ": " + str(nb_hours[mode]) + " hours"
            print(result)
    else:
        nb_hours = 0                
    
    " ------------- Plot (if asked) ---------------- "
    if chart == 'yes':
        if climate_data is not None:
            for mode in mode_list:
                ax.plot(T_out[Zone[mode]],w_out[Zone[mode]],label=mode,color=mode_colors[mode],marker='.',ms=marker_size,ls='none')
            ax.legend(loc='lower right',bbox_to_anchor=(1.6,0.15),frameon=False)
            
        ax2 = ax.twinx()
        for mode in mode_list[0:-1]:
            ax2.plot(T_lim[mode],w_lim[mode],label=limits[mode]['legend'],color=limits[mode]['color'],lw=3)
        
        ax_ylim = ax.get_ylim()
        ax2.set_ylim(ax_ylim[0],ax_ylim[1])
        ax2.get_yaxis().set_visible(False)
        ax2.legend(loc='upper left',frameon=False,fontsize=16)
        
        plt.show()
    
    return nb_hours, ax

        