#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# GSA implementation
#
# by Felipe Tajá
# 07 feb 2022

"""
Acceptance function.

Reference: 
Tsallis, C., & Stariolo, D. A. (1996). Generalized simulated annealing. 
Physica A: Statistical Mechanics and Its Applications, 233(1–2), 
395–406. https://doi.org/10.1016/S0378-4371(96)00271-3
"""

import numpy as np


def acceptance(E_t, E_0, T, qa):
    """ A probabilidade de aceitacao e valida para os valores de
    qa in (-Infinity, Infinity).
    
    A funcao acceptance retorna um valor entre 0 e 1, conforme os pa-
    rametros discriminados abaixo:
    E_t : funcao custo no ponto atual.
    E_0 : ultimo valor aceito da funcao custo;
    T   : Temperatura atual;
    qa  : Parametro modificador da funcao aceitacao.
    
    """
    dif = (E_t - E_0) / T
    if qa == 1.0:          # Caso especifico para qa = 1.
        Pqa = np.exp(-dif)
    else:
        pqa1 = (qa - 1.0) * dif + 1.0
        if  pqa1 <= 0.0: # Garantia que a base seja sempre positiva.
            Pqa = 0.0
        else:
            Pqa = np.exp(np.log(pqa1) / (1.0 - qa))
    return Pqa

