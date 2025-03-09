
import json
import requests
import os
import matplotlib.pyplot as plt

msApk=os.environ.get('msapk')

class MarketStack():
     def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.values=[]

    
     def historicalDividends(self):
         api_url=f"http://api.marketstack.com/v2/eod?access_key={msApk}&symbols=AAPL&date_from = 2025-02-27& date_to = 2025-03-09"
         response=requests.get(api_url)
         print(response.json())

     def showEod(self,stockname):
         labels=['Lowest','Highest','Open','Close']
         
         api_url=f'http://api.marketstack.com/v2/eod?access_key={msApk}&symbols={stockname}'
         response=requests.get(api_url)
         data=json.loads(response.text)
         #data hakasuluissa json-tuloksen taulukon nimi low ja high ovat avain-arvo pareja
         for d in data['data']:
             low=d['low']
             high=d['high']
             openVal=d['open']
             close=d['close']
             name=d['symbol']
         nameStr=name+' Stock'
         self.values.append(low)
         self.values.append(high)
         self.values.append(openVal)
         self.values.append(close)
         
         plt.title(nameStr)
         plt.barh(labels,self.values)
         plt.show()
        
         
      
    