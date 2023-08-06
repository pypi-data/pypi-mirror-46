import re
import json

import requests

VERSION = '0.0.1'

DEV = False
API_URL = 'https://search.altoshift.com'
UPSERT_PATH = '/api/upsert/products'
SEARCH_PATH = '/v1/search'
search_token = '5ce3952c2cd48000372c6519-1558418732584-46452766'
print("Altoshift : " + VERSION)

class SearchEngine():
    @classmethod
    def __init__(self, engineId='5ce3952c2cd48000372c6519', userId='5ce39510aecc14001c635627', token='scd6eaeec8cd9fbb0a6c4d265845ab164255e24d9fcc6a11c81d55585', **kwargs):
        self.xEngineId = engineId
        self.xUserId = userId
        self.xToken = token
        
    def version(self):
        return VERSION
    
    def upsert_products(self,dt):
        headers = {
            'content-type': 'application/json',
            'Accept-Charset': 'UTF-8',
            'x-engine-id': self.xEngineId,
            'x-user-id': self.xUserId,
            'x-token': self.xToken
        }
        data = {
            "items": dt
        }
        url = API_URL+UPSERT_PATH
        resp = requests.post(url,data=json.dumps(data),headers=headers)
        try:
            result =  {'status_code': resp.status_code,
            'response': resp.json() if resp.text else {}}
        except ValueError:
            result =  {'status_code': resp.status_code,
            'response': resp.text}
        return result

    def get_items(self,query):
        url = API_URL+SEARCH_PATH+'?query='+query+'&token='+search_token
        resp = requests.get(url)
        try:
            result =  {'status_code': resp.status_code,
            'response': resp.json() if resp.text else {}}
        except ValueError:
            result =  {'status_code': resp.status_code,
            'response': resp.text}
        return result