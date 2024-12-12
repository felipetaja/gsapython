#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# GSA implementation
#
# by Felipe Tajá
# 07 feb 2022

"""
Temperature function.

Reference: 
Tsallis, C., & Stariolo, D. A. (1996). Generalized simulated annealing. 
Physica A: Statistical Mechanics and Its Applications, 233(1–2), 
395–406. https://doi.org/10.1016/S0378-4371(96)00271-3
"""

import numpy as np


def temperature(T0, qT, t):
    """
    A funcao temperatura e valida para os valores de qT in (1, Infinity).
    Quanto maior o valor de qT, mais severa sera a reducao da temperatura.
    
    Retorna um valor que varia entre 0 e T0, decescentemente, conforme os pa-
    rametros abaixo:
        T0 : Temperatura inicial;
        qT : Parametro de reducao da temperatura;
        t  : Tempo.
        
    """
    if qT == 1.0:                            # Especifico para qT = 1
        TqT = T0 * np.log(2) / np.log(1 + t) # log x e ln x
    else:
        qTm = qT - 1                         # So para facilitar a escrita
        num = np.power(2, qTm) - 1           # Numerador
        den = np.power(1 + t, qTm) - 1       # Denominador
        TqT = T0 * num / den                 # Funcao Temperatura
    return TqT
