#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# GSA implementation
#
# by Felipe Tajá
# 07 feb 2022

from ._gsa import gsa
# from .acceptance import acceptance
# from .newcoord import newcoord
# from .temperature import temperature
# from .visita import visita


__version__ = "2023.06.30"
__all__ = ["gsa"]

# Versão 2023.06.30
# variaval __all__
#
# Versão 2022.02.13
# Inclusão de um mostrador de percentagem de progresso.
#
# Versão 2022.02.08
# Eliminação do contador de chamadas da função visita.
# Substituição da matriz de evolução da busca trace_mat por uma lista
# Retirada do tempo de processamento dentro do código da função _gsa

# Versão 2022.02.07
# Adequação ao PEP 8 o máximo que meu conhecimento permite. 
# Separação das funções em arquivos distintos.
# Agora é possível chamar a função como um módulo independente.
