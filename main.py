# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 13:19:33 2025

@author: Alanis Zeoli

Objective: perform a feasibility analysis on given climate conditions
    
Inputs:
    meteo_file_path: Path where the meteorological data can be found. The meteorological file can contain the following columns:
        T_dry = Dry temperature [°C] (mandatory)
        w = Specific humidity [kg/kg] (not mandatory but recommended for faster results)
        T_wb = Wet bulb temperature [°C] (optional)
        T_dp = Dew point temperature [°C] (optional)
        RH = Relative humidity [-] (optional)
            
    climate: Alternative way to specify the climate zone, it can be chosen in the following list:
        '0A' = Extremely hot humd (Singapore)
        '0B' = Extremely hot dry (Abu Dhabi)
        '1A' = Very hot humid (Guayaquil)
        '2A' = Hot humid (Sao Paulo)
        '3A' = Warm humid (Buenos Aires)
        '3B' = Warm dry (Los Angeles)
        '4A' = Mixed humid (Brussels)
        '4C' = Mixed marine (Vancouver)
        '5A' = Cool humid (Copenhagen)
        '6A' = Cold humid (Montreal)
        
    period: Period at which we want to  perofrm the feasibisibility analysis, it should be coupled with a climate zone.
        'present' = TMY 2001-2020 (default)
        'future' = TMY 2041-2060
        
    climate_data: The meteorological data can be given directly as inputs in the form of a dataframe including the same columns as in the meteorological file.
        
    components: Dictionnary containing the system components (based on methodology.component class) with their nominal effectiveness.
    
    params: Dictionnary containing values for the system operational parameters:
        T_su_min = Minimum supply temperature [°C] (default = 16°C)
        T_su_max = Maximum supply temperature [°C] (default = 20°C)
        T_reg = regeneration temperature [°C] (default = 60°C)
        T_in = indoor temperature [°C] (default = 24°C)
        RH_in = indoor relative humidity [-] (default = 0.5)
        w_in = indoor specific humidity [kg/kg] (default = computed with T_in and RH_in)
        T_wb_in = indoor wet bulb temperature [°C] (default = computed with T_in and RH_in)
"""

import pandas as pd
import numpy as np
from CoolProp.CoolProp import HAPropsSI

# Import own functions
import methodology

def feasibility_analysis(meteo_file_path=None,climate=None,period='present',climate_data=None,components=None,params=None):
    # Definition of constants
    P_atm = 101325
    to_K = 273.15
    to_C = -273.15
    
    # Climate data
    if meteo_file_path is None:   
        if climate is not None:
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
    
            # Recreate file name based on information
            try:
                city = cities[climate]
            except:
                print("Error: "+climate+" is not a valid climate zone yet.")
                return
                
            city_str = city.replace(' ','_')
             
            try:
                TMY = TMYs[period]
            except:
                print("Error: "+period+" is not a valid time period.")
                return
                
            filename = climate + '_' + city_str + '_TMY_' + TMY
            meteo_file_path = 'Meteo/' + filename + '.csv'
            
    if meteo_file_path is not None:
        try:
            climate_data = pd.read_csv(meteo_file_path)
        except:
            print("Error: File "+meteo_file_path+" cannot be found.")
            return
    
    if climate_data is not None:
        if 'T_dry' not in climate_data.columns:
            print("Error: There is no column T_dry in the given data file")
        else:
            nb_data = len(climate_data['T_dry'])
            
        if 'w' not in climate_data.columns:
            print("Computation of specific humidity using HAPropsSI")
            w = np.zeros((nb_data,1))
            humidity = ['RH','T_wb','T_dp']
            
            for var in humidity:
                if var in climate_data.columns:
                    for h in range(nb_data):
                        w[h] = HAPropsSI('W','T',climate_data['T_dry'][h]+to_K,var,climate_data[var][h],'P',P_atm)
                     
                    T_index = climate_data.columns.get_loc('T_dry')
                    climate_data.insert(T_index+1,'w',w)
                    break
                    
    # Components
    if components is None: # Definition of the default set of components
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
    else:
        valid_types = ['DEC','IEC','D-IEC','DW']
        for name in components:
            if components[name].type not in valid_types:
                print("Error: "+components[name].type+" is not a valid component type")
            else:
                if components[name].epsilon is None:
                    default_epsilon = 0.85
                    if components[name].type == 'IEC':
                        default_epsilon = 0.75
                        
                    print("No value has been set for the "+components[name].type+" efficiency, default value is"+default_epsilon)
                    
    # Parameters
    default_params = {'T_reg': 60,
                   'T_su_min': 16,
                   'T_su_max': 20
                   }
    
    if params is None:
        params = {}
    
    for key in default_params:
        if key not in params.keys():
            params[key] = default_params[key]
            
    default_indoor_data = {'T_in': ['T', 24, 'C'],
                           'RH_in': ['RH', 0.5, '-'],
                           'w_in': ['W', None, 'kg/kg'],
                           'T_wb_in': ['B', None, 'C']
                    }
    default_indoor = pd.DataFrame(data=default_indoor_data,index=['var','value','units'])
    known_indoor = []
    unknown_indoor = []
    
    for col in default_indoor.columns:
        if col in params.keys():
            known_indoor.append(col)
        else:
            unknown_indoor.append(col)

    for hum in ['w_in','T_wb_in']:
        if hum not in params.keys():
            if len(known_indoor) < 2:
                new_known = []
                for key in unknown_indoor:
                    default_value = default_indoor[key]['value']
                    if default_value is not None:
                        params[key] = default_value
                        new_known.append(key)
                        
                for key in new_known:
                    known_indoor.append(key)
                    unknown_indoor.remove(key)
            
            var = []
            val = []
            var.append(default_indoor[hum]['var'])
            val.append(0)
            
            for i in range(2):
                key = known_indoor[i]
                var.append(default_indoor[key]['var'])
                val.append(default_indoor[key]['value'])
                if default_indoor[key]['units'] == 'C':
                    val[i+1] = val[i+1]+to_K
            
            val[0] = HAPropsSI(var[0],var[1],val[1],var[2],val[2],'P',P_atm)
            
            if default_indoor[hum]['units'] == 'C':
                val[0] = val[0]+to_C
                
            params[hum] = val[0]
            known_indoor.append(hum)
            unknown_indoor.remove(hum)
    
    # Feasiblity analysis
    nb_hours_modes, component_dict, ax = methodology.main(components,params,climate_data)
    
    if nb_hours_modes != 0:
        # Choice of recommended system
        comfort_hours = 0
        min_comfort_hours = 0.98*nb_data # Arbitrary for now, system should guarantee indoor thermal comfort 98% of the time
        
        for mode in component_dict:
            comfort_hours = comfort_hours+nb_hours_modes[mode]
            
            if comfort_hours > min_comfort_hours:
                break
        
        if mode == "Active cooling":
            print("Active cooling is necessary to guarantee indoor thermal comfort.")
        else:
            print("The components that are recommended to be added in the system are "+str(component_dict[mode])+" to guarantee a 98% thermal comfort.")
        
    return nb_hours_modes, ax

nb_hours_modes, ax = feasibility_analysis(meteo_file_path='Meteo/2A_Sao_Paulo_TMY_2001-2020.csv')

# Definition of components
# DEC = methodology.component('DEC',0.85)
# IEC = methodology.component('IEC',0.75)
# D_IEC = methodology.component('D_IEC',0.85)
# DW = methodology.component('DW',0.85)

# components = {
#     'DEC':DEC,
#     'IEC':IEC,
#     'D-IEC':D_IEC,
#     'DW':DW
#     }

# # Set parameters
# params = {}
# params['T_su_min'] = 16
# params['T_su_max'] = 20
# params['T_reg'] = 60
# params['T_in'] = 24
# params['RH_in'] = 0.5

# params['w_in'] = HAPropsSI('W','T',params['T_in']+273.15,'RH',params['RH_in'],'P',P_atm)
# params['T_wb_in'] = HAPropsSI('B','T',params['T_in']+273.15,'RH',params['RH_in'],'P',P_atm)-273.15