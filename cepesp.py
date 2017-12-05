import pandas as pd
import urllib2
import hashlib
import os

BASE_URL = "http://cepesp.io/api/consulta/"
BASE_DIR = os.path.dirname(__file__)


def add_filters(request, estado=None, numero_candidato=None, numero_partido=None, codigo_municipio=None):
    index = 0
    if estado is not None:
        request = add_uf_filter(request, estado)
    if numero_candidato is not None:
        request = add_filter(request, "NUMERO_CANDIDATO", numero_candidato, index)
        index += 1
    if numero_partido is not None:
        request = add_filter(request, "NUMERO_PARTIDO", numero_partido, index)
        index += 1
    if codigo_municipio is not None:
        request = add_filter(request, "CODIGO_MUNICIPIO", codigo_municipio, index)
        index += 1
    return request


def add_filter(request, column, value, index):
    return request + "&columns[{}][name]={}&columns[{}][search][value]={}".format(index, column, index, value)


def add_uf_filter(request, estado):
    return request + "&uf_filter={}".format(estado)


def warn(function_name):
    print("[WARN] %s function may return some invalid or incorrect results" % function_name)


def query(request):
    filename = hashlib.md5(request).hexdigest() + ".gz"
    response = urllib2.urlopen(BASE_URL + request)
    save_cache(response, filename)
    return pd.read_csv(os.path.join(BASE_DIR, "cache/" + filename), sep=",", dtype=str)


def save_cache(response, filename):
    file_path = os.path.join(BASE_DIR, "cache/" + filename)
    with open(file_path, 'wb') as outfile:
        outfile.write(response.read())


def votos(cargo=1, ano=2014, agregacao_politica=1, agregacao_regional=0, estado=None, numero_candidato=None,
          numero_partido=None, codigo_municipio=None):
    request = "votos?cargo={}&ano={}&agregacao_politica={}&agregacao_regional={}&format=gzip".format(cargo, ano,
                                                                                                     agregacao_politica,
                                                                                                     agregacao_regional)
    request = add_filters(request, estado, numero_candidato, numero_partido, codigo_municipio)
    return query(request)


def candidatos(cargo=1, ano=2014, agregacao_politica=1, agregacao_regional=2, estado=None, numero_candidato=None,
               numero_partido=None, codigo_municipio=None):
    request = "candidatos?cargo={}&ano={}&agregacao_politica={}&agregacao_regional={}&format=gzip".format(cargo, ano,
                                                                                                          agregacao_politica,
                                                                                                          agregacao_regional)
    request = add_filters(request, estado, numero_candidato, numero_partido, codigo_municipio)
    return query(request)


def legendas(cargo=1, ano=2014, agregacao_politica=1, agregacao_regional=2, estado=None, numero_candidato=None,
             numero_partido=None, codigo_municipio=None):
    request = "legendas?cargo={}&ano={}&agregacao_politica={}&agregacao_regional={}&format=gzip".format(cargo, ano,
                                                                                                        agregacao_politica,
                                                                                                        agregacao_regional)
    request = add_filters(request, estado, numero_candidato, numero_partido, codigo_municipio)
    return query(request)


def votos_x_candidatos(cargo=1, ano=2014, agregacao_politica=1, agregacao_regional=2, estado=None,
                       numero_candidato=None):
    warn("votos_x_candidatos")
    vot = votos(cargo, ano, agregacao_politica, agregacao_regional, estado, numero_candidato)
    cand = candidatos(cargo, ano, agregacao_politica, agregacao_regional, estado, numero_candidato)
    return vot.set_index(["NUMERO_CANDIDATO", "SIGLA_UE", "NUM_TURNO", "ANO_ELEICAO"]).merge(
        cand.set_index(["NUMERO_CANDIDATO", "SIGLA_UE", "NUM_TURNO", "ANO_ELEICAO"]), how="left", left_index=True,
        right_index=True, suffixes=["_x", "_y"]).reset_index()


def votos_x_legendas(cargo=1, ano=2014, agregacao_politica=1, agregacao_regional=2, estado=None, numero_candidato=None):
    warn("votos_x_legendas")
    vot = votos(cargo, ano, agregacao_politica, agregacao_regional, estado, numero_candidato)
    leg = legendas(cargo, ano, agregacao_politica, agregacao_regional, estado, numero_candidato)
    leg = leg.rename(columns={"NUMERO_PARTIDO": "NUMERO_CANDIDATO"})
    return vot.set_index(["NUMERO_CANDIDATO", "SIGLA_UE", "NUM_TURNO", "ANO_ELEICAO"]).merge(
        leg.set_index(["NUMERO_CANDIDATO", "SIGLA_UE", "NUM_TURNO", "ANO_ELEICAO"]), how="left", left_index=True,
        right_index=True, suffixes=["_x", "_y"]).reset_index()


def candidato_x_legendas(cargo=1, ano=2014, agregacao_politica=1, agregacao_regional=2, estado=None,
                         numero_candidato=None):
    warn("candidato_x_legendas")
    leg = legendas(cargo, ano, agregacao_politica, agregacao_regional, estado, numero_candidato)
    cand = candidatos(cargo, ano, agregacao_politica, agregacao_regional, estado, numero_candidato)
    return cand.set_index(["NUMERO_PARTIDO", "SIGLA_UE", "ANO_ELEICAO"]).merge(
        leg.set_index(["NUMERO_PARTIDO", "SIGLA_UE", "ANO_ELEICAO"]), how="left", left_index=True, right_index=True,
        suffixes=["_x", "_y"]).reset_index()


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
