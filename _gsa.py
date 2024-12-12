#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# GSA implementation
# by Felipe Tajá
# 13 feb 2022

"""
A Generalizad Simulated Annealing global algorithm.
"""

import numpy as np

from .temperature import temperature
from .newcoord import newcoord
from .acceptance import acceptance


def gsa(func, lim_min, lim_max, 
        X_0=None, qv=2.0, qa=1.0, T0=100.0, 
        NCycles=1, NStopMax=10000, 
        cvg=None, seed=None):
    """
    Minimizacao de funcao de varias variaveis via Generalized 
    Simulated Annealing.
    
    Usa-se como dados de ENTRADA os seguintes parametros:
    
    func     : Funcao objetivo.
    lim_min  : Limite minimo das variaveis de busca;
    lim_max  : Limite maximo das variaveis de busca;
    X_0      : Coordenada inicial. Caso nao incluido, X_0 e sorteado 
               aleatoriamente entre lim_min e lim_max;
    qv       : Parametro controlador função distribuição (visita) - 
               Padrao 2.0 (Distribuição de Cauchy-Lorentz);
    qa       : Parametro controlador da funcao aceitacao (accepetance) - 
               Padrao 1.0 (Critério de Bolzmann);
    T0       : Temperatura inicial - Padrão 100.0, mas recomenda-se que 
               seja maior ou igual ao dobro do maximo valor da funcao a 
               ser otimizada dentro do dominio;
    NCycles  : Quantidade de ciclos a temperatura constante (tamanho da 
               cadeia de Markov - Padrao 1, mas recomenda-se que seja o 
               dobro da quantidade de variáveis;
    NStopMax : Quantidade de ciclos com temperatura decrescente ou número 
               de cadeias de Markov - Padrao 1000;
    cvg      : Valor no qual considera-se a convergência - Padrão None;
    seed     : Semente do gerador de numero aleatorio - Padrão None.
        
    Como SAIDA, obtem-se, em ordem,
    
    [0] X_Min    : Coordenadas do minimo encontrado;
    [1] func_Min : Valor minimo encontrado da funcao objetivo;
    [2] trac_mat : Lista contendo a progressão da busca. Sao 4 elementos
                   com (NStopMax x NCycles) linhas cada. Cada elemento
                   representa, em ordem, 
                   [0] numero do passo;
                   [1] temperatura;
                   [2] valor da funcao;
                   [3] valor do minimo da funcao;
    [3] n        : Lista com:
                   [0] numero de pontos de decida;
                   [1] numero de pontos aceitos de subida;
                   [2] numero de pontos rejeitados;
                   Lembrando-se que o numero total de passos e igual a 
                   ndescida + nsubidaA + nsubidaR;
    [4] func_plot: Lista com o valor da funcao somente para as coordenadas aceitas.
    """
    # Inclui a semente dos números aleatórios
    if seed is not None:
        np.random.seed(seed)
        
    # Dimensão da busca
    D = len(lim_min)
    
    # Conversions
    lim_min = np.array(lim_min)
    lim_max = np.array(lim_max)
    
    # Avisos para parametros errados
    # Incluir todos os testes dos parametros de entrada
    # Criterio de convergencia, exceto para nmax
    
    # Sorteia o ponto inicial -> X_0
    # Sorteio conforme distribuiçao uniforme entre lim_min e lim_max.
    if X_0 is None:
        X_0 = (lim_max - lim_min) * np.random.random(D) + lim_min
    else:
        X_0 = np.array(X_0)

    # Convenção utilizada para as coordenadas (X) e a função objetivo (func).
    # _0    - Ponto inicial
    # _Min  - Mínimo encontrado
    # _t    - Ponto corrente (tempo t)
    # _A    - Ponto aceito anterior (tempo t-1).
    #
    X_Min = X_0.copy()
    X_A   = X_0.copy()
    X_t = np.empty(D)

    func_0   = func(X_0)
    func_Min = func_0.copy()
    func_t   = func_0.copy()
    func_A   = func_0.copy()

    # Contadores
    # nvisita = 0  #  Funcao visita
    ndescida = 0 #  Aceitos por movimentos de descida
    nsubidaA = 0 #  Aceitos por movimentos de subida
    nsubidaR = 0 #  Rejeitados por movimentos de subida
    nsn = 0      #  Numeros de calculos realizados (step number)
    #  Lista da temperatura
    tp = np.array([])   
    tp = np.append(tp, np.array(T0))
    # Lista da funcao objetivo calculada em todos os pontos
    lcofv = np.array([])
    lcofv = np.append(lcofv, np.array(func_t))
    #  Lista do minimo atual
    lcMofv = np.array([])
    lcMofv = np.append(lcMofv, np.array(func_Min))
    # Lista do valor da função somente para as coordenadas aceitas.
    func_plot = np.array([])
    func_plot = np.append(func_plot, np.array(func_A))
        
    # Loop principal do GSA.
    for i in range(1, NStopMax + 1): # Reduz a temperatura conforme o valor de qv.
        T = temperature(T0, qv, i)   # Calcula a temperatura corrente
        print("   ")
        print('Concluindo: {:6.2f} %'.format(100 * i / NStopMax))
        print("   ")
        # Loop com temperatura constante.
        # print(" ")
        for j in range(NCycles):
            nsn += 1
            tp = np.append(tp, T) # Lista da temperatura
            
            # Sorteio das novas coordenadas
            X_t = newcoord(X_A, lim_min, lim_max, qv, T, j, NCycles)

            # Calcula a função objetivo para a nova variável
            func_t = func(X_t)
            lcofv  = np.append(lcofv, np.array(func_t))
                            
            # Critério de aceitação
            if func_t <= func_A: # Movimento de descida (automaticamente aceito)
                ndescida += 1 # Conta quantos movimentos de decida.

                # Modifica a coordenada t para t-1.
                # _A sao os movimentos aceitos
                X_A = X_t.copy()
                func_A = func_t.copy()

                # Atualiza o minimo encontrado
                if func_t <= func_Min:
                    X_Min = X_t.copy()
                    func_Min = func_t.copy()
            else:
            # Movimento de subida (conforme o critério de aceitação)
                a = np.random.random()
                b = acceptance(E_t=func_t, E_0=func_A, T=T/i, qa=qa)
                if a < b:
                    nsubidaA += 1
                    X_A = X_t.copy()
                    func_A = func_t.copy()
                else:
                    nsubidaR += 1
            func_plot = np.append(func_plot, np.array(func_A)) # minimos aceitos
            lcMofv = np.append(lcMofv, np.array(func_Min))
#        #*************************
#        # Se a função for menor que este limite 
#        # isto representa a convergência.
        if cvg is not None:
            if func_Min < cvg:
                print("  ")
                print("*******************")
                print("*** CONVERGENCE ***")
                print("*******************")
                print("  ")
                break
        
    # trace_mat = np.matrix((np.arange(nsn + 1), tp, lcofv, lcMofv)).T
    trace_mat = list((np.arange(nsn + 1), tp, lcofv, lcMofv))
    # n = [nvisita, ndescida, nsubidaA, nsubidaR, (t_f - t_0)]
    n = [ndescida, nsubidaA, nsubidaR]
    #******************************************************
    
    return X_Min, func_Min, trace_mat, n, func_plot
