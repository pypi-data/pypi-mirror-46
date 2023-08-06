# coding: utf-8
"""Módulo para funciones de procesamiento de documentos."""


def token_cumple(token, filtros=None):
    """Determina si token pasa los filtros.

    Parameters
    ----------
    token : spacy.tokens.Token
        Token a evaluar.
    filtros : dict, optional
        (stopwords, postags, entities)

    Returns
    -------
    bool
        Si token pasa los filtros o no.
    """
    cumple = (
        (token.is_alpha)
        and (not token.like_url)
        and (not token.like_num)
        and (not token.like_email)
        and (token.lower_ not in filtros.get("stopwords"))
        and (token.pos_ not in filtros.get("postags"))
        and (token.ent_type_ not in filtros.get("entities"))
    )

    return cumple


def filtrar_tokens(contenedor, filtros=None):
    """Filtra tokens del contenedor según filtros.

    Parameters
    ----------
    contenedor : spacy.tokens.Doc | spacy.tokens.Span
        Estructura de la cual se filtran tokens.
    filtros : dict, optional
        (alpha, stopwords, postags, entities)

    Returns
    -------
    list (spacy.tokens.Token)
        Los tokens no descartados por los filtros.
    """
    return (tok for tok in contenedor if token_cumple(tok, filtros=filtros))


def filtrar_frases(doc, n_tokens=0):
    """Filtra frases en doc que no tienen un mínimo de tokens.

    Parameters
    ----------
    doc: spacy.tokens.Doc
    n_tokens: int

    Yields
    ------
    spacy.tokens.Span
        Frase no descartada por el filtro.
    """
    yield from (frase for frase in doc.sents if len(frase) > n_tokens)


def token_presente(token, wordlist):
    """Determina si token está en un grupo de palabras.

    Parameters
    ----------
    token : spacy.tokens.Token
        Token a evaluar.
    wordlist : set
        Grupo de palabras.

    Returns
    -------
    bool
        Si token está en el grupo de palabras o no.
    """
    return token.lower_ in wordlist
