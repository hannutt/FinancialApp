
import json
import requests
import os

msApk=os.environ.get('msapk')

class MarketStack():
     def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.values=[]

    
     def historicalDividends(self):
         api_url=f"http://api.marketstack.com/v2/eod?access_key={msApk}&symbols=AAPL&date_from = 2025-02-27& date_to = 2025-03-09"
         response=requests.get(api_url)
         print(response.json())

     def showEod(self):
         api_url=f'http://api.marketstack.com/v2/eod?access_key={msApk}&symbols=AAPL'
         response=requests.get(api_url)
         data=json.loads(response.text)
         for d in data['data']:
             low=d['low']
             high=d['high']
         self.values.append(low)
         self.values.append(high)
         print(self.values)
        
         
      
    