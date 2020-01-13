from cepesp.client import AthenaClient, LambdaClient
from cepesp.columns import VOTOS, CANDIDATOS, LEGENDAS, TSE_CANDIDATO, TSE_LEGENDA, TSE_COLIGACAO, TSE_DETALHE, BEM_CANDIDATO


def translate(args):
    options = {'table': args['table'], 'ano': args['year'], 'filters': []}

    if 'position' in args:
        options['cargo'] = args['position']
    elif 'job' in args:
        options['cargo'] = args['job']
    else:
        raise Exception('Position argument is mandatory')

    if 'regional_aggregation' in args:
        options['agregacao_regional'] = args['regional_aggregation']
    elif 'reg' in args:
        options['agregacao_regional'] = args['reg']

    if 'political_aggregation' in args:
        options['agregacao_politica'] = args['political_aggregation']
    elif 'pol' in args:
        options['agregacao_politica'] = args['pol']

    if 'columns' in args:
        if isinstance(args['columns'], list):
            options['c'] = ",".join(args['columns'])
        else:
            options['c'] = args['columns']

    if 'filters' in args and isinstance(args['filters'], dict):
        for column in args['filters']:
            value = args['filters'][column]
            options['filters[' + column + ']'] = value

    if 'uf' in args:
        options['uf_filter'] = args['uf']

    if 'party' in args:
        if args['table'] == "filiados":
            options['party'] = args['party']
        else:
            options['filters[NUMERO_PARTIDO]'] = args['party']

    if 'government_period' in args:
        options['government_period'] = args['government_period']
    elif 'period' in args:
        options['government_period'] = args['period']

    if 'name' in args and args["table"] == "secretarios":
        options['name_filter'] = args['name']

    if 'mun' in args:
        options['mun_filter'] = args['mun']

    if 'candidate_number' in args:
        options['filters[NUMERO_CANDIDATO]'] = args['candidate_number']

    if 'party' in args:
        options['filters[NUMERO_PARTIDO]'] = args['party']

    if 'only_elected' in args:
        options['only_elected'] = args['only_elected']

    if 'offset' in args:
        options['start'] = args['offset']

    if 'limit' in args:
        options['length'] = args['limit']

    options['sep'] = ','
    options['brancos'] = 1
    options['nulos'] = 1
    options['py_ver'] = '1.0.0'

    return options


def get(**args):
    options = translate(args)
    dev = args.get("dev", False)
    fast = args.get("fast", False)

    athena_client = AthenaClient(dev)
    lambda_client = LambdaClient()
    client = lambda_client if fast else athena_client

    return client.get(options)


def get_votes(**args):
    args['table'] = "votos"
    args['columns'] = args.get('columns', '*')
    args['regional_aggregation'] = args.get('regional_aggregation', MUNICIPIO)

    if args['columns'] == '*':
        args['columns'] = VOTOS[args['regional_aggregation']]

    return get(**args)


def get_candidates(**args):
    args['table'] = "candidatos"
    args['columns'] = args.get('columns', '*')

    if args['columns'] == '*':
        args['columns'] = CANDIDATOS

    return get(**args)


def get_coalitions(**args):
    args['table'] = "legendas"
    args['columns'] = args.get('columns', '*')

    if args['columns'] == '*':
        args['columns'] = LEGENDAS

    return get(**args)


def get_elections(**args):
    args['table'] = "tse"
    args['regional_aggregation'] = args.get('regional_aggregation', MUNICIPIO)
    args['political_aggregation'] = args.get('political_aggregation', CANDIDATO)
    args['columns'] = args.get('columns', '*')

    if args['columns'] == '*':
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

    return get(**args)


def get_assets(**args):
    args['table'] = 'bem_candidato'
    args['columns'] = args.get('columns', '*')

    if args['columns'] == '*':
        args['columns'] = BEM_CANDIDATO

    return get(**args)


def get_secretaries(**args):
    args['table'] = 'secretarios'

    if args['columns'] == '*':
        args['columns'] = BEM_CANDIDATO

    return get(**args)


def get_filiates(**args):
    args['table'] = 'filiados'

    if args['columns'] == '*':
        args['columns'] = BEM_CANDIDATO

    return get(**args)


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
VOTSEC = 9

PARTIDO = 1
CANDIDATO = 2
COLIGACAO = 3
DETALHE = 4