import json

import requests
import yaml
from requests.auth import HTTPBasicAuth
from pprint import pprint


def get_data_from_watson(payload):
    ibm_basic_url = "https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze"
    ibm_user = "056eeb40-a7d6-40e8-bede-3de64d73f623"
    ibm_pass = "nIHKCzohLVSV"
    headers = {'content-type': 'application/json'}

    params = {'version': '2017-02-27'}
    response = requests.post(ibm_basic_url,
                             auth=HTTPBasicAuth(ibm_user, ibm_pass),
                             headers=headers,
                             params=params,
                             data=json.dumps(payload))
    return response.json()


if __name__ == "__main__":
    global ibm_username
    global ibm_password
    with open('settings.yaml', 'r') as f:
        data = yaml.load(f)
    ibm_username = data['ibm-username']
    ibm_password = data['ibm-password']

    payload = {"text": "IBM is an American multinational technology company headquartered in Armonk, New York, "
                       "United States, with operations in over 170 countries.",
               "features": {
                   "entities": {
                       "emotion": "true",
                       "sentiment": "true",
                       "limit": 10},
                   "keywords": {
                       "emotion": "true",
                       "sentiment": "true",
                       "limit": 10}
               }
               }
    json = get_data_from_watson(payload)
    pprint(json)
