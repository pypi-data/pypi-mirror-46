import json
import requests


class Endpoint(object):
    def __init__(self, url: str, secret: str):
        self.__endpoint = url
        self.__secret = secret

    def execute_query(self, query: str):
        headers = {"X-Hasura-Admin-Secret": self.__secret, "Content-Type": "application/json"}
        result = requests.post(self.__endpoint, json={'query': query}, headers=headers)
        return json.loads(result.content)
