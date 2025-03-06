# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 13:19:33 2025

@author: Alanis Zeoli

Objective : perform a feasibility analysis methodology
"""

import pandas as pd
import numpy as np
from CoolProp.CoolProp import HAPropsSI

# Import own functions
import methodology


# Choose a location
climate = '0B'
period = 'present'

# From the location determine the file to be read
cities = {
    '0A': 'Singapore',
    '0B': 'Abu Dhabi',
    '1A': 'Guayaquil',
    '2A': 'Sao Paulo',
    '3A': 'Buenos Aires',
    '3B': 'Los Angeles',
    '4A': 'Brussels',
    '4C': 'Vancouver',
    '5A': 'Copenhagen',
    '6A': 'Montreal'    
    }

TMYs = {
    'present': '2001-2020',
    'future': '2041-2060'
    }

city = cities[climate]
city_str = city.replace(' ','_')

TMY = TMYs[period]

filename = climate + '_' + city_str + '_TMY_' + TMY
filepath = 'Meteo/' + filename + '.csv'

climate_data = pd.read_csv(filepath,sep=';')
climate_data['RH'] = climate_data['RH']/100
nb_data = len(climate_data['T_dry'])

# Compute specific humidity
P_atm = 101325
w_out = np.zeros((nb_data,1))


for h in range(nb_data):
    w_out[h] = HAPropsSI('W','T',climate_data['T_dry'][h]+273.15,'RH',climate_data['RH'][h],'P',P_atm)
    
climate_data.insert(6,'w',w_out)

# Definition of components
DEC = methodology.component('DEC',0.85)
IEC = methodology.component('IEC',0.75)
D_IEC = methodology.component('D_IEC',0.85)
DW = methodology.component('DW',0.85)

components = {
    'DEC':DEC,
    'IEC':IEC,
    'D-IEC':D_IEC,
    'DW':DW
    }

# Set parameters
params = {}
params['T_su_min'] = 16
params['T_su_max'] = 20
params['T_reg'] = 60
params['T_in'] = 24
params['RH_in'] = 0.5

params['w_in'] = HAPropsSI('W','T',params['T_in']+273.15,'RH',params['RH_in'],'P',P_atm)
params['T_wb_in'] = HAPropsSI('B','T',params['T_in']+273.15,'RH',params['RH_in'],'P',P_atm)-273.15

nb_hours_modes = methodology.main(components,params,climate_data)
