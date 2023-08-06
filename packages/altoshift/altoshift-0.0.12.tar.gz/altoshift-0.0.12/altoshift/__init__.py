import re
import json
import time
import requests
import altoshift
import pandas as pd 

DEV = False
ALTO_SYNC_PATH = '/api/mapping/sync'
ALTO_READ_PATH = '/api/mapping/read'
ALTO_UPSERT_PATH = '/api/upsert/products'
ALTO_DELETE_PATH = '/api/delete/products'
ALTO_SEARCH_PATH = '/v1/search'

if(__name__ == "__main__"):
    print('Believe in Future.')

class connect():
    args = {}

    @classmethod
    def __init__(self, **kwargs):
        args = kwargs
        if(DEV):
            self.host = args.get('host','https://search.altoshift.com')
            self.xEngineId = args.get('engineId','5ce3952c2cd48000372c6519')
            self.xUserId = args.get('userId','5ce39510aecc14001c635627')
            self.xToken = args.get('token','scd6eaeec8cd9fbb0a6c4d265845ab164255e24d9fcc6a11c81d55585')
            self.sToken = args.get('sToken','5ce3952c2cd48000372c6519-1558418732584-46452766')
        else:
            self.host = args.get('host','https://api.altoshift.com')
            self.xEngineId = args.get('engineId','')
            self.xUserId = args.get('userId','')
            self.xToken = args.get('token','')
            self.sToken = args.get('sToken','')

    def readXlsToJson(self,file):
        df = pd.read_excel(file)
        result = df.to_json(orient='records', lines=False)
        return result

    def readCsvToJson(self,file):
        df = pd.read_csv(file)
        result = df.to_json(orient='records', lines=False)
        return result

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
    
    def slice_per(self, source, step):
        return [source[i::step] for i in range(step)]
    
    def dataSlicer(self,dt):
        limit=500
        step=((len(dt)/limit)+1)
        result=self.slice_per(dt,step)
        return result

    def altoUpsert(self,file):
        datas = []
        datas_total = 0
        datas_runned = 0
        inserted = 0
        failed = 0
        if(file.lower().endswith('.csv')):
            datas = self.readCsvToJson(file)
        elif(file.lower().endswith('.xlsx')):
            datas = self.readXlsToJson(file)
        datas_total = len(json.loads(datas))
        datas = self.dataSlicer(json.loads(datas))
        for data in datas:
            datas_runned += len(data)
            print("Upsert Altoshift : {}/{} row(s) | progress {}%".format(datas_runned,datas_total,int(round((float(datas_runned)/float(datas_total))*100))))
            resp = self.upsertItems(data)
            inserted += len(resp.get('inserted',[]))
            failed += len(resp.get('failed',[]))
            print('Upsert Status : %s ' % resp.get('success','None') +' | Inserted : %s '%str(inserted)+ ' | Failed : %s '%str(failed))
            time.sleep(3)

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
        resp = self.requestPost(url=url,headers=headers,data=data)
        return resp

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
        result = self.requestGet(url=url,headers=headers)
        return json.dumps(result, indent = 3, sort_keys=False)

    def getItems(self,query):
        url = self.host+ALTO_SEARCH_PATH
        url+='?query='+query+'&token='+self.sToken
        return self.requestGet(url=url)
    
    