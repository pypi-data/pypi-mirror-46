# coding: utf-8
"""Módulo para funciones de interacción con el sistema."""
from pathlib import Path
import random


def crear_directorio(nombre):
    """Crea nuevo directorio si no existe.

    Si no es ruta absoluta será creado relativo al directorio de trabajo.

    Parameters
    -------------
    nombre : str | Path
        Nombre de nuevo directorio a crear.

    Returns
    ---------
    Path
        Ruta absoluta del directorio.
    """
    ruta = Path(nombre).resolve()

    if not ruta.is_dir():
        ruta.mkdir(parents=True, exist_ok=True)

    return ruta


def iterar_rutas(directorio, aleatorio=False):
    """Itera rutas de archivos en directorio, en orden o aleatoriamente.

    Parameters
    ----------
    directorio : str | Path
        Directorio a iterar.
    aleatorio : bool
        Iterar aleatoriamente.

    Yields
    ------
    Path
        Ruta de archivo.
    """
    absoluto = Path(directorio).resolve()
    rutas = (ruta for ruta in absoluto.iterdir() if ruta.is_file())

    todas = sorted(rutas)
    if aleatorio:
        random.shuffle(todas)

    yield from todas
