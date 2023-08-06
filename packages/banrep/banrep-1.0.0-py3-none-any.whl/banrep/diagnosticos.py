# coding: utf-8
"""Módulo para funciones de diagnóstico de datos usados y modelos generados."""
from collections import Counter
from pathlib import Path

from gensim.models import CoherenceModel
import pandas as pd


def verificar_oov(doc):
    """Encuentra tokens fuera de vocabulario (OOV) en un documento procesado.

   Parameters
   ----------
   doc: spacy.tokens.Doc

   Returns
   -------
   list (str, int)
      Tokens oov en frecuencia decreciente.
   """
    c = Counter(tok.text for tok in doc if tok.is_oov)

    return sorted(c.items(), key=lambda i: i[1], reverse=True)


def calcular_coherencias(modelos, corpus, medida="c_v"):
    """Calcula Coherence Score de modelos de tópicos.

   Parameters
    ----------
   modelos : list (gensim.models.ldamodel.LdaModel)
      Modelos LDA para diferentes números de tópicos.
   corpus : banrep.corpus.MiCorpus
      Corpus previamente inicializado con documentos.
   medida : str
      Medida de Coherencia a usar (u_mass, c_v, c_uci, c_npmi).

   Yields
    ------
    float
      Coherencia calculada.
   """
    textos = [texto for texto in corpus.docs_a_palabras()]
    for modelo in modelos:
        cm = CoherenceModel(
            model=modelo, texts=textos, dictionary=corpus.id2word, coherence=medida
        )

        yield cm.get_coherence()


def docs_topicos(modelo, corpus):
    """Distribución de probabilidad de tópicos en cada documento.

    Parameters
    ----------
    modelo : gensim.models.ldamodel.LdaModel
        Modelo LDA entrenado.
    corpus : banrep.corpus.MiCorpus
       Corpus previamente inicializado con documentos.

    Returns
    -------
    pd.DataFrame
      Documentos X Tópicos.
    """
    return pd.DataFrame(dict(doc) for doc in modelo[corpus])


def topico_dominante(df):
    """Participación de tópicos como dominante en documentos.

   Parameters
   ----------
   df : pd.DataFrame
      Distribución de probabilidad de tópicos en cada documento.

   Returns
   -------
   pd.DataFrame
      Participación de cada tópico como dominante.
   """
    absolutos = df.idxmax(axis=1).value_counts()
    relativos = round(absolutos / absolutos.sum(), 4).reset_index()
    relativos.columns = ["topico", "docs"]

    return relativos


def palabras_probables(modelo, topico, n=15):
    """Palabras más probables en un tópico.

   Parameters
   ----------
   modelo : gensim.models.ldamodel.LdaModel
      Modelo LDA entrenado.
   topico : int
      Número del Tópico
   n : int
      Cuantas palabras obtener.

   Returns
   -------
   pd.DataFrame
      Palabras y sus probabilidades.
   """
    df = pd.DataFrame(
        modelo.show_topic(topico, n), columns=["palabra", "probabilidad"]
    ).sort_values(by="probabilidad")

    df['topico'] = topico

    return df

