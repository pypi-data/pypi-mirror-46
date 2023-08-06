# coding: utf-8
"""Módulo para visualización de datos usados y modelos generados."""
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go


def figura_coherencias(numeros, scores, colores):
    """Genera figura para gráfica de Coherence Score.

    Parameters
    ----------
    numeros : list (int)
        Número de tópicos para cada modelo .
    scores : list (float)
        Coherencia calculada para cada modelo LDA.
    colores : tuple
        Colores a usar.
    """
