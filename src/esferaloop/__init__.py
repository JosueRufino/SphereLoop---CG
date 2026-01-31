"""
Pacote principal do Simulador de Esfera com Subdivisão de Loop.
Contém os módulos de núcleo, visualização e utilitários.
"""

from .nucleo.malha import Malha
from .nucleo.subdivisao_loop import SubdivisaoLoopEsfera
from .visualizacao.renderizador import Visualizador
from .utilitarios.metricas import obter_metricas_malha

__version__ = "1.0.0"
