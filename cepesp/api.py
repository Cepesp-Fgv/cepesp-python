import urllib as urllib

import pandas as pd

from columns import VOTOS, CANDIDATOS, LEGENDAS

BASE_URL = "http://test.cepesp.io/api/consulta/"


def build_filters(filters):
    q = ""

    if 'UF' in filters.keys():
        uf = filters.pop('UF')
        q += "&uf_filter={}".format(uf)

    for k, v in filters.items():
        q += "&filters[{}]={}".format(k, v)

    return q


def build_columns(columns):
    q = ""
    for column in columns:
        q += "&c[]={}".format(column)

    return q


def query(request, filters, columns):
    if filters is not None:
        request += build_filters(filters)

    if columns is not None:
        request += build_columns(columns)

    response = urllib.urlopen(BASE_URL + request)
    df = pd.read_csv(response, sep=",", dtype=str)
    df.columns = map(str.upper, df.columns)

    return df

def tse(ano, cargo, agregacao_regional, agregacao_politica, estado=None, numero_candidato=None, filtros=None,
          colunas=None):
    request = "tse?cargo={}&ano={}&agregacao_regional={}&agregacao_politica={}&format=csv".format(cargo, ano, agregacao_regional, agregacao_politica)
    if filtros is None:
        filtros = dict()

    if estado is not None:
        filtros['UF'] = estado

    if numero_candidato is not None:
        filtros['NUMERO_CANDIDATO'] = numero_candidato

    return query(request, filtros, colunas)

def votos(ano, cargo, agregacao_regional, estado=None, numero_candidato=None, filtros=None,
          colunas=None):
    request = "votos?cargo={}&ano={}&agregacao_regional={}&format=csv".format(cargo, ano, agregacao_regional)
    if filtros is None:
        filtros = dict()

    if estado is not None:
        filtros['UF'] = estado

    if numero_candidato is not None:
        filtros['NUMERO_CANDIDATO'] = numero_candidato

    return query(request, filtros, colunas)


def candidatos(ano, cargo, filtros=None, colunas=None):
    request = "candidatos?cargo={}&ano={}&format=csv".format(cargo, ano)
    return query(request, filtros, colunas)


def legendas(ano, cargo, filtros=None, colunas=None):
    request = "legendas?cargo={}&ano={}&format=csv".format(cargo, ano)
    return query(request, filtros, colunas)


def get_elections(cargo):
    if cargo in [1, 3, 5, 6, 7, 8]:
        return [2014, 2010, 2006, 2002, 1998]
    elif cargo in [11, 13]:
        return [2016, 2012, 2008, 2004, 2000]


class CARGO:
    PRESIDENTE = 1
    SENADOR = 5
    GOVERNADOR = 3
    VEREADOR = 13
    PREFEITO = 11
    DEPUTADO_FEDERAL = 6
    DEPUTADO_ESTADUAL = 7
    DEPUTADO_DISTRITAL = 8


class AGR_REGIONAL:
    BRASIL = 0
    UF = 2
    MUNICIPIO = 6
    MUNZONA = 7
    ZONA = 8
    MACRO = 1
    MESO = 4
    MICRO = 5


class AGR_POLITICA:
    CANDIDATO = 1
    PARTIDO = 2
    COLIGACAO = 3
