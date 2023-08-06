import re
import json

import altoshift
import requests
import pandas as pd 

DEV = False
ALTO_UPSERT_PATH = '/api/upsert/products'
ALTO_DELETE_PATH = '/api/delete/products'
ALTO_SYNC_PATH = '/api/mapping/sync'
ALTO_READ_PATH = '/api/mapping/read'
ALTO_SEARCH_PATH = '/v1/search'

class connect():
    args = {}

    @classmethod
    def __init__(self, **kwargs):
        args = kwargs
        self.host = args.get('host','https://search.altoshift.com')
        self.xEngineId = args.get('engineId','5ce3952c2cd48000372c6519')
        self.xUserId = args.get('userId','5ce39510aecc14001c635627')
        self.xToken = args.get('token','scd6eaeec8cd9fbb0a6c4d265845ab164255e24d9fcc6a11c81d55585')
        self.sToken = args.get('sToken','5ce3952c2cd48000372c6519-1558418732584-46452766')

    def requestHandle(self,resp):
        try:
            result =  {'status_code': resp.status_code,
            'response': resp.json() if resp.text else {}}
        except ValueError:
            result =  {'status_code': resp.status_code,
            'response': resp.text}
        return result

    def requestGet(self,**kwargs):
        args = kwargs
        url = args.get('url','')
        headers = args.get('headers','')
        body = args.get('body','')
        resp = requests.get(url,headers=headers)
        result = self.requestHandle(resp)
        return result

    def requestPost(self, **kwargs):
        args = kwargs
        url = args.get('url','')
        headers = args.get('headers','')
        data = args.get('data','')
        resp = requests.post(url,data=json.dumps(data),headers=headers)
        result = self.requestHandle(resp)
        return result

    def mappingSync(self,dt):
        headers = {
            'content-type': 'application/json',
            'Accept-Charset': 'UTF-8',
            'x-engine-id': self.xEngineId,
            'x-user-id': self.xUserId,
            'x-token': self.xToken
        }
        data = {"customFields": dt}
        url = self.host+ALTO_SYNC_PATH
        return self.requestPost(url=url,headers=headers,data=data)

    def upsertItems(self,dt):
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
        url = self.host+ALTO_UPSERT_PATH
        return self.requestPost(url=url,headers=headers,data=data)

    def deleteItems(self,dt):
        headers = {
            'content-type': 'application/json',
            'Accept-Charset': 'UTF-8',
            'x-engine-id': self.xEngineId,
            'x-user-id': self.xUserId,
            'x-token': self.xToken
        }
        data = {
            "ids": dt
        }
        url = self.host+ALTO_DELETE_PATH
        return self.requestPost(url=url,headers=headers,data=data)
    
    def mappingRead(self):
        headers = {
            'content-type': 'application/json',
            'Accept-Charset': 'UTF-8',
            'x-engine-id': self.xEngineId,
            'x-user-id': self.xUserId,
            'x-token': self.xToken
        }
        data = {}
        url = self.host+ALTO_READ_PATH
        return self.requestGet(url=url,headers=headers)

    def getItems(self,query):
        url = self.host+ALTO_SEARCH_PATH
        url+='?query='+query+'&token='+self.sToken
        return self.requestGet(url=url)
    