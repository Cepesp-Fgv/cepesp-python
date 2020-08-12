import time
import io
import pandas as pd
import requests


class QueryFailedException(Exception):
    pass


def _request_json(url, params):
    response = requests.get(url, params, headers={
        'Accept': 'application/json'
    })
    response_data = response.json()

    return response_data


def _request_csv(url, params):
    response = requests.get(url, params, headers={
        'Accept': 'text/csv'
    })
    response_data = io.StringIO(response.content.decode('utf-8'))
    df = pd.read_csv(response_data, sep=',', dtype=str)
    df.columns = map(str.upper, df.columns)

    return df


class AthenaClient:

    def __init__(self, dev):
        self.base = "https://cepespdata.io"
        if dev:
            self.base = "https://test.cepesp.io"
        self.version = '1.0.0'

    def _get_query_id(self, args):
        url = self.base + "/api/consulta/athena/query"
        data = _request_json(url, args)

        if 'error' in data:
            raise QueryFailedException(data['error'])

        return data['id']

    def _get_query_status(self, query_id):
        url = self.base + "/api/consulta/athena/status"
        data = _request_json(url, {'id': query_id, 'py_ver': self.version})

        if 'error' in data:
            raise QueryFailedException(data['error'])

        return data['status'], data['message']

    def _get_query_result(self, query_id):
        url = self.base + "/api/consulta/athena/result"
        df = _request_csv(url, {'id': query_id, 'py_ver': self.version})

        return df

    def get(self, args):
        query_id = self._get_query_id(args)
        status, message = ("RUNNING", None)
        sleep = 2

        while status in ["RUNNING", "QUEUED"]:
            time.sleep(sleep)
            status, message = self._get_query_status(query_id)

            if sleep == 2 and (status == "RUNNING" or status == "QUEUED"):
                sleep = 16
            else:
                sleep = sleep + 2

        if status == "FAILED":
            raise QueryFailedException(message)

        return self._get_query_result(query_id)


class LambdaClient:

    def __init__(self):
        self.base = "https://api.cepespdata.io"

    def get(self, args):
        url = self.base + "/api/query" 
        df = _request_csv(url, args)

        return df
