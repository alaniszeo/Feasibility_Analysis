# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 09:51:06 2025

@author: Alanis Zeoli

Objective: Modify the meteorological files to include the spec. humidity
"""

import pandas as pd
import numpy as np
from CoolProp.CoolProp import HAPropsSI

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

# For each file, recreate file name
for zone in cities:
    city = cities[zone]
    city_str = city.replace(' ','_')
    
    for period in TMYs:
        TMY = TMYs[period]
        
        filename = zone + '_' + city_str + '_TMY_' + TMY
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
        
        climate_data.to_csv(filepath, index=False)