import time
from urllib.parse import urlencode

import pandas as pd
import requests


class QueryFailedException(Exception):
    pass


class AthenaClient:

    def __init__(self, dev):
        self.base = "http://cepesp.io"
        if dev:
            self.base = "http://test.cepesp.io"
        self.version = '1.0.0'
        self.headers = {
            'Accept': 'application/json'
        }

    def _get_query_id(self, args):
        url = self.base + "/api/consulta/athena/query"
        response = requests.get(url, args, headers=self.headers).json()
        if 'error' in response:
            raise QueryFailedException(response['error'])

        return response['id']

    def _get_query_status(self, query_id):
        url = self.base + "/api/consulta/athena/status"
        response = requests.get(url, {'id': query_id, 'py_ver': self.version}, headers=self.headers).json()
        if 'error' in response:
            raise QueryFailedException(response['error'])

        return response['status'], response['message']

    def _get_query_result(self, query_id):
        query_string = urlencode({'id': query_id, 'py_ver': self.version})
        url = self.base + "/api/consulta/athena/result?" + query_string
        df = pd.read_csv(url, sep=',', dtype=str)
        df.columns = map(str.upper, df.columns)

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
        self.headers = {
            'Accept': 'application/json'
        }

    def get(self, args):
        url = self.base + "/api/query?" + urlencode(args)
        df = pd.read_csv(url, sep=',', dtype=str)
        df.columns = map(str.upper, df.columns)

        return df
