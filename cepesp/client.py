import pandas as pd
from urllib import urlencode


class CepespClient:

    def __init__(self, base):
        self.base = base

    def _request_url(self, table, args):
        query = urlencode(self._translate(args))
        return "{base}/api/consulta/{table}?{query}".format(base=self.base, table=table, query=query)

    def _request(self, table, args):
        url = self._request_url(table, args)
        df = pd.read_csv(url, sep=',', dtype=str)
        df.columns = map(str.upper, df.columns)

        return df

    def _translate(self, args):
        options = {'ano': args['year'], 'filters': []}

        if 'position' in args:
            options['cargo'] = args['position']
        elif 'job' in args:
            options['cargo'] = args['job']
        else:
            raise Exception('Position argument is mandatory')

        if 'regional_aggregation' in args:
            options['agregacao_regional'] = args['regional_aggregation']

        if 'political_aggregation' in args:
            options['agregacao_politica'] = args['political_aggregation']

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

        if 'mun' in args:
            options['mun_filter'] = args['mun']

        if 'candidate_number' in args:
            options['filters[NUMERO_CANDIDATO]'] = args['candidate_number']

        if 'party' in args:
            options['filters[NUMERO_PARTIDO]'] = args['party']

        if 'only_elected' in args:
            options['only_elected'] = args['only_elected']

        options['sep'] = ','
        options['brancos'] = 1
        options['nulos'] = 1

        return options

    def get_votes(self, **args):
        return self._request("votos", args)

    def get_candidates(self, **args):
        return self._request("candidatos", args)

    def get_coalitions(self, **args):
        return self._request("legendas", args)

    def get_elections(self, **args):
        return self._request("tse", args)