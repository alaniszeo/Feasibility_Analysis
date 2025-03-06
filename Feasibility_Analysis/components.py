# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 13:18:55 2025

@author: Alanis Zeoli

Objective: Create classes for the comonents considered in the feasibility 
    analysis methodology

Considered classes:
    DEC = direct evaporative cooler
        Attributes:
        * epsilon_wb = wet bulb efficiency
    IEC = indirect evaporative cooler
        Attributes:
        * epsilon_s_wb = secondary wet bulb efficiency
    D_IEC = dew point indirect evaporative cooler
        Attributes:
        * epsilon_dp = dew point efficiency
    DW = desiccant wheel
        Attributes:
        * epsilon_h = isenthalpic efficiency
        * T_reg = regeneration temperature
"""

class component():
    def __init__(self,type_name,epsilon):
        self.type = type_name
        self.epsilon = epsilon
