import time
import pandas as pd
import requests


class QueryFailedException(Exception):
    pass


class CepespClient:

    def __init__(self, base, version='1.0.0'):
        self.base = base
        self.version = version
        self.headers = {
            'Accept': 'application/json'
        }

    def _get_query_id(self, table, args):
        args['table'] = table
        url = self.base + "/api/consulta/athena/query"
        response = requests.get(url, self._translate(args), headers=self.headers).json()
        if 'error' in response:
            raise QueryFailedException(response['error'])

        return response['id']

    def _get_query_status(self, query_id):
        url = self.base + "/api/consulta/athena/status"
        response = requests.get(url, {'id': query_id}, headers=self.headers).json()
        if 'error' in response:
            raise QueryFailedException(response['error'])

        return response['status'], response['message']

    def _get_query_result(self, query_id):
        url = self.base + "/api/consulta/athena/result?id=" + query_id

        try:
            df = pd.read_csv(url, sep=',', dtype=str)
            df.columns = map(str.upper, df.columns)
        except HTTPError as e:
            raise QueryFailedException(str(e))

        return df

    def _request(self, table, args):
        query_id = self._get_query_id(table, args)
        status, message = ("RUNNING", None)
        sleep = 1

        while status in ["RUNNING", "QUEUED"]:
            time.sleep(sleep)
            sleep *= 2

            status, message = self._get_query_status(query_id)

            if status in ["RUNNING", "QUEUED"] and sleep == 2:
                sleep = 32

        if status == "FAILED":
            raise QueryFailedException(message)

        return self._get_query_result(query_id)

    def _translate(self, args):
        options = {'table': args['table'], 'ano': args['year'], 'filters': []}

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
        options['py_ver'] = self.version

        return options

    def get_votes(self, **args):
        return self._request("votos", args)

    def get_candidates(self, **args):
        return self._request("candidatos", args)

    def get_coalitions(self, **args):
        return self._request("legendas", args)

    def get_elections(self, **args):
        return self._request("tse", args)
