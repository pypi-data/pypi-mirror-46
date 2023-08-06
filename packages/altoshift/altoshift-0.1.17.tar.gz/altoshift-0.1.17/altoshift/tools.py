import json
import pandas as pd

class Tools(object):
    def readXlsToJson(self,file):
        df = pd.read_excel(file)
        result = df.to_json(orient='records', lines=False)
        result = json.loads(result.decode('latin-1'))
        return result

    def readCsvToJson(self,file,xdelimiter=None):
        df = pd.read_csv(file,delimiter=xdelimiter)
        result = df.to_json(orient='records', lines=False)
        result = json.loads(result.decode('latin-1'))
        return result

    def filterJson(self,dt,xfilter=None):
        df = pd.DataFrame(dt)
        df = df[xfilter] if xfilter else df
        result = df.to_json(orient='records', lines=False)
        result = json.loads(result.decode('latin-1'))
        return result