from client import CepespClient
from columns import VOTOS, CANDIDATOS, LEGENDAS, TSE_CANDIDATO, TSE_LEGENDA, TSE_COLIGACAO, TSE_DETALHE

client = CepespClient("http://test.cepesp.io")


def get_votes(**args):
    if 'columns' in args and args['columns'] == '*':
        args['columns'] = VOTOS[args['regional_aggregation']]

    return client.get_votes(**args)


def get_candidates(**args):
    if 'columns' in args and args['columns'] == '*':
        args['columns'] = CANDIDATOS

    return client.get_candidates(**args)


def get_coalitions(**args):
    if 'columns' in args and args['columns'] == '*':
        args['columns'] = LEGENDAS

    return client.get_coalitions(**args)


def get_elections(**args):
    if 'columns' in args and args['columns'] == '*':
        reg = args['regional_aggregation']
        pol = args['political_aggregation']
        if pol == CANDIDATO:
            args['columns'] = TSE_CANDIDATO[reg]
        elif pol == PARTIDO:
            args['columns'] = TSE_LEGENDA[reg]
        elif pol == COLIGACAO:
            args['columns'] = TSE_COLIGACAO[reg]
        elif pol == DETALHE:
            args['columns'] = TSE_DETALHE[reg]

    return client.get_elections(**args)


def get_years(cargo):
    if cargo in [PRESIDENTE, VICE_PRESIDENTE, GOVERNADOR, VICE_GOVERNADOR, SENADOR, DEP_FEDERAL, DEP_ESTADUAL,
                 DEP_DISTRITAL, SUPLENTE_1, SUPLENTE_2]:
        return [2018, 2014, 2010, 2006, 2002, 1998]
    elif cargo in [PREFEITO, VEREADOR]:
        return [2016, 2012, 2008, 2004, 2000]


PRESIDENTE = 1
VICE_PRESIDENTE = 2
SENADOR = 5
GOVERNADOR = 3
VICE_GOVERNADOR = 4
VEREADOR = 13
PREFEITO = 11
DEP_FEDERAL = 6
DEP_ESTADUAL = 7
DEP_DISTRITAL = 8
SUPLENTE_1 = 9
SUPLENTE_2 = 10

BRASIL = 0
UF = 2
MUNICIPIO = 6
MUNZONA = 7
ZONA = 8
MACRO = 1
MESO = 4
MICRO = 5

PARTIDO = 1
CANDIDATO = 2
COLIGACAO = 3
DETALHE = 4
