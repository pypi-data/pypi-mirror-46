# coding: utf-8
"""Modulo para extraer texto de archivos binarios."""
from pathlib import Path

from tika import parser

from banrep.io import guardar_texto
from banrep.utils import crear_directorio, iterar_rutas


def extraer_info(archivo):
    """Extrae texto y metadata de archivo.

    Parameters
    -------------
    archivo : str | Path
        Ruta del archivo del cual se quiere extraer texto y metadata.

    Returns
    ---------
    tuple (str, dict)
        Texto y Metadata.
    """
    ruta = Path(archivo)
    if ruta.is_file():
        try:
            info = parser.from_file(str(ruta))

        except Exception:
            print(f"No pudo extraerse información de {ruta.name}.")
            info = dict()
    else:
        print(f"{ruta.name} no es un archivo.")
        info = dict()

    texto = info.get("content")
    metadata = info.get("metadata")

    return texto, metadata


def extraer_archivos(dir_docs, dir_textos, aleatorio=False):
    """Extrae y guarda texto de cada archivo en directorio si no existe.

    Parameters
    -------------
    dir_docs : str | Path
        Directorio donde están los documentos originales.
    dir_textos : str | Path
        Directorio donde se quiere guardar texto extraído.

    Returns
    ---------
    int
        Número de documentos procesados.
    """
    dirdocs = Path(dir_docs)
    dirtextos = crear_directorio(nombre=dir_textos)

    n = 0
    for ruta in iterar_rutas(dirdocs, aleatorio=aleatorio):
        archivo = dirtextos.joinpath(f"{ruta.stem}.txt")
        if not archivo.exists():
            texto, metadata = extraer_info(ruta)
            if texto:
                guardar_texto(texto, archivo)
                n += 1

    return n


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="""Extrae y guarda texto de cada archivo en entrada."""
    )

    parser.add_argument(
        "entrada", help="Directorio en el que están los archivos originales."
    )
    parser.add_argument(
        "--salida",
        default="textos",
        help="Directorio para guardar texto extraído (si no se especifica: %(default)s)",
    )
    args = parser.parse_args()

    entrada = args.entrada
    salida = args.salida

    n = extraer_archivos(entrada, salida)
    full = Path(salida).resolve()
    print(f"{n} nuevos archivos guardados en directorio {str(full)}")


if __name__ == "__main__":
    main()
