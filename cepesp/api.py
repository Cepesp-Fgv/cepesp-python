from columns import VOTOS, CANDIDATOS, LEGENDAS, TSE_CANDIDATO, TSE_LEGENDA, TSE_COLIGACAO, TSE_DETALHE
from client import CepespClient

client = CepespClient("http://cepesp.io")


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
    if cargo in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        return [2018, 2014, 2010, 2006, 2002, 1998]
    elif cargo in [11, 13]:
        return [2016, 2012, 2008, 2004, 2000]


PRESIDENTE = 1
SENADOR = 5
GOVERNADOR = 3
VEREADOR = 13
PREFEITO = 11
DEPUTADO_FEDERAL = 6
DEPUTADO_ESTADUAL = 7
DEPUTADO_DISTRITAL = 8


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
