# coding: utf-8
"""Módulo para crear modelos de tópicos."""
import warnings

from gensim.models.ldamodel import LdaModel


def crear_ldas(corpus, numeros, params):
    """Crea modelos LDA para diferente número de tópicos.

    Parameters
    ----------
    corpus : banrep.corpus.MiCorpus
       Corpus previamente inicializado con documentos.
    numeros: list (int)
        Diferentes #'s de tópicos.
    params: dict
        Parámetros requeridos en modelos LDA.

    Yields
    ------
    gensim.models.ldamodel.LdaModel
        Modelo LDA para un número de tópicos.
    """
    for n in numeros:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            yield LdaModel(corpus, num_topics=n, id2word=corpus.id2word, **params)
