from electionsBR.backend.client import AthenaClient, LambdaClient
from electionsBR.columns import VOTES, CANDIDATES, PARTIES, CANDIDATE_VOTES, COALITION_VOTES, PARTY_VOTES, \
    ELECTION_DETAILS, CANDIDATE_ASSETS, SECRETARIES, FILIATES


def _parse_position(position):
    if isinstance(position, int):
        return position
    else:
        position = position.lower()
        if position == "presidente" or position == "president":
            return PRESIDENTE
        elif position == "governador" or position == "governor":
            return GOVERNADOR
        elif position == "senador" or position == "senator":
            return SENADOR
        elif position == "deputado federal" or position == "federal deputy":
            return DEP_FEDERAL
        elif position == "deputado estadual" or position == "state deputy":
            return DEP_ESTADUAL
        elif position == "prefeito" or position == "mayor":
            return PREFEITO
        elif position == "vereador" or position == "councillor":
            return VEREADOR
        else:
            raise Exception("Invalid 'position' argument provided")


def _parse_regional_aggregation(aggregation):
    if isinstance(aggregation, int):
        return aggregation
    else:
        aggregation = aggregation.lower()
        if aggregation == "brasil" or aggregation == "brazil":
            return BRASIL
        elif aggregation == "macro":
            return MACRO
        elif aggregation == "estado" or aggregation == "state":
            return UF
        elif aggregation == "meso":
            return MESO
        elif aggregation == "micro":
            return MICRO
        elif aggregation == "municipio" or aggregation == "municipality":
            return MUNICIPIO
        elif aggregation == "municipio-zona" or aggregation == "municipality-zone":
            return MUNZONA
        elif aggregation == "zona" or aggregation == "zone":
            return ZONA
        elif aggregation == "votação seção" or aggregation == "electoral section":
            return VOTSEC
        else:
            raise Exception("Invalid 'regional_aggregation' argument provided")


def _parse_political_aggregation(aggregation):
    if isinstance(aggregation, int):
        return aggregation
    else:
        aggregation = aggregation.lower()
        if aggregation == "candidato" or aggregation == "candidate":
            return CANDIDATO
        elif aggregation == "partido" or aggregation == "party":
            return PARTIDO
        elif aggregation == "coaligacao" or aggregation == "coalition":
            return COLIGACAO
        elif aggregation == "consolidado" or aggregation == "consolidated":
            return DETALHE
        else:
            raise Exception("Invalid 'political_aggregation' argument provided")


def _parse_arguments(args):
    options = {'table': args['table'], 'ano': args['year'], 'filters': []}

    if 'position' in args:
        options['cargo'] = _parse_position(args['position'])
    elif 'job' in args:
        options['cargo'] = _parse_position(args['job'])
    else:
        raise Exception('Position argument is mandatory')

    if 'regional_aggregation' in args:
        options['agregacao_regional'] = _parse_regional_aggregation(args['regional_aggregation'])
    elif 'reg' in args:
        options['agregacao_regional'] = _parse_regional_aggregation(args['reg'])

    if 'political_aggregation' in args:
        options['agregacao_politica'] = _parse_political_aggregation(args['political_aggregation'])
    elif 'pol' in args:
        options['agregacao_politica'] = _parse_political_aggregation(args['pol'])

    if 'columns' in args:
        if isinstance(args['columns'], list):
            options['c'] = ",".join(args['columns'])
        else:
            options['c'] = args['columns']

    if 'filters' in args and isinstance(args['filters'], dict):
        for column in args['filters']:
            value = args['filters'][column]
            options['filters[' + column + ']'] = value

    if 'state' in args:
        options['uf_filter'] = args['state']
    elif 'uf' in args:
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

    if args.get('null_votes', False):
        options['nulos'] = 1

    if args.get('blank_votes', False):
        options['brancos'] = 1

    options['sep'] = ','
    options['py_ver'] = '1.0.0'

    return options


def _get(args):
    options = _parse_arguments(args)
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
        reg = _parse_regional_aggregation(args['regional_aggregation'])
        args['columns'] = VOTES[reg]

    return _get(args)


def get_candidates(**args):
    args['table'] = "candidatos"
    args['columns'] = args.get('columns', '*')

    if args['columns'] == '*':
        args['columns'] = CANDIDATES

    return _get(args)


def get_coalitions(**args):
    args['table'] = "legendas"
    args['columns'] = args.get('columns', '*')

    if args['columns'] == '*':
        args['columns'] = PARTIES

    return _get(args)


def get_elections(**args):
    args['table'] = "tse"
    args['regional_aggregation'] = args.get('regional_aggregation', MUNICIPIO)
    args['political_aggregation'] = args.get('political_aggregation', CANDIDATO)
    args['columns'] = args.get('columns', '*')

    if args['columns'] == '*':
        reg = _parse_regional_aggregation(args['regional_aggregation'])
        pol = _parse_political_aggregation(args['political_aggregation'])
        if pol == CANDIDATO:
            args['columns'] = CANDIDATE_VOTES[reg]
        elif pol == PARTIDO:
            args['columns'] = PARTY_VOTES[reg]
        elif pol == COLIGACAO:
            args['columns'] = COALITION_VOTES[reg]
        elif pol == DETALHE:
            args['columns'] = ELECTION_DETAILS[reg]

    return _get(args)


def get_assets(**args):
    args['table'] = 'bem_candidato'
    args['columns'] = args.get('columns', '*')

    if args['columns'] == '*':
        args['columns'] = CANDIDATE_ASSETS

    return _get(args)


def get_secretaries(**args):
    args['table'] = 'secretarios'

    if args['columns'] == '*':
        args['columns'] = SECRETARIES

    return _get(args)


def get_filiates(**args):
    args['table'] = 'filiados'

    if args['columns'] == '*':
        args['columns'] = FILIATES

    return _get(args)


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
