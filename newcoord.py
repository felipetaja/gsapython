#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# GSA implementation
#
# by Felipe Tajá
# 07 feb 2022

"""
A correction for random visiting.
"""

import numpy as np

from .visita import visita


def newcoord(X_A, lim_min, lim_max, qv, Tqv, icm, NCycles):
    """
    A partir do sorteio conforme a distribuiÃ§Ã£o de Tsallis, gera a nova 
    coordenada e corrige para um valor dentro do intervalo 
    lim_min-lim_max.
    """
    # Neste contexto, o "icm" Ã© o Ã­ndice dentro de uma Cadeia de Markov.

    D = len(X_A)
    limites = lim_max - lim_min
    X_t = X_A.copy()
    if NCycles >= D:
        if icm + 1 <= D:
        # Sorteia 1 variÃ¡vel de cada vez, calculando a funÃ§Ã£o objetivo.
            X_t[icm] = X_A[icm] + visita(qv, Tqv, 1)
        else:
        # Quando terminar, sorteia todas as outras ao mesmo tempo.
            X_t = X_A + visita(qv, Tqv, D)
    else:
        # Caso o tamanho da cadeia de Markov seja menor que D, sorteia 
        # tudo ao mesmo tempo.
        X_t = X_A + visita(qv, Tqv, D)

    # CorreÃ§Ã£o das coordenadas.
    for i in range(D):
        # Abaixo do limite mÃ­nimo.
        if X_t[i] < lim_min[i]:
            X_t[i] = lim_min[i] + np.mod(X_t[i] - lim_min[i], limites[i])
        # Acima do limite mÃ¡ximo
        if X_t[i] > lim_max[i]:
            X_t[i] = lim_max[i] - np.mod(lim_max[i] - X_t[i], limites[i])

    # np.set_printoptions(precision = 4)
    # print(X_t)
    return X_t
# *******************************************************************
