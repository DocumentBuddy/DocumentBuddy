import json

import requests
from requests.auth import HTTPBasicAuth


class TextAnalyzerWatson:

    __base_url = "https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze"
    __headers = {'content-type': 'application/json'}
    __username = ''
    __password = ''
    __params = ''

    def __init__(self, username, password, version):
        self.__username = username
        self.__password = password
        self.__params = {'version': version}

    def send_post_request(self, payload):
        response = requests.post(self.__base_url,
                                 auth=HTTPBasicAuth(self.__username, self.__password),
                                 headers=self.__headers,
                                 params=self.__params,
                                 data=json.dumps(payload))
        return response.json()

    def get_entities(self, text, limit):
        payload = {"text": text,
                   "features": {
                       "entities": {
                           "emotion": "true",
                           "sentiment": "true",
                           "limit": limit},
                       }
                   }
        return self.send_post_request(payload)

    def get_keywords(self, text, limit):
        payload = {"text": text,
                   "features": {
                       "keywords": {
                           "emotion": "true",
                           "sentiment": "true",
                           "limit": limit},
                       }
                   }
        return self.send_post_request(payload)

    def get_sentiment(self, text, limit):
        payload = {"text": text,
                   "features": {
                       "sentiment": {
                           "document": "true",
                           "limit": limit},
                   }
                   }
        return self.send_post_request(payload)
