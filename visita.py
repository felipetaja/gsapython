#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# GSA implementation
#
# by Felipe Tajá
# 07 feb 2022

"""
Random numbers generator from Tsallis distribution.

Reference: 
Schanze, T. (2006). An exact D-dimensional Tsallis random number 
generator for generalized simulated annealing. Computer Physics 
Communications, 175(11–12), 708–712. 
https://doi.org/10.1016/j.cpc.2006.07.012
"""

import numpy as np


def visita(qv, Tqv, D):
    """
    Funcao visita D-Dimensional, conforme referencia
    T. Schanze / Computer Physics Communications 175 (2006) 708-712.
    
    Utiliza-se um gerador de numero aleatorio D-Dimensional com distri-
    buicao normal de media 0 e desvio padrao 1 e um outro gerador de 
    numero aleatório com distribuicao gama, com fator de forma p(qv) e 
    escala 1.
    
    qv   : Parametro de abertura da distribuicao e qv in (1, 3);
    Tqv  : Temperatura;
    D    : Dimensao do problema.
    """
    p = (3.0 - qv)/(2.0 * (qv - 1.0))
    s = np.sqrt(2.0 * (qv - 1.0)) / np.power(Tqv, 1 / (3.0 - qv))
    
    # x =  NORMAL RANDOM NUMBERS N(1,0) D-dimensional
    x = np.random.standard_normal(D)
    # u = GAMMA RANDOM NUMBER gama(1,p) 1-dimmensional
    u = np.random.gamma(p)
    y = s * np.sqrt(u)
    z = x / y
    return z
