"""
SphereLoop - Loop Subdivision Sphere Rendering

Este pacote implementa o algoritmo de Loop Subdivision para transformar
um icosaedro inicial em uma esfera suave.
"""

from sphereloop.core.mesh import Malha
from sphereloop.core.loop_subdivision import SubdivisaoLoopEsfera
from sphereloop.visualization.renderer import Visualizador
from sphereloop.utils.metrics import obter_metricas_malha

__version__ = "1.0.0"
