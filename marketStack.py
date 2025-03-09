
import json
import requests
import os
import matplotlib.pyplot as plt

msApk=os.environ.get('msapk')

class MarketStack():
     def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.values=[]

    
     def historicalData(self,ticker,tbox,fromDate,toDate):
         api_url=f"http://api.marketstack.com/v2/eod?access_key={msApk}&symbols={ticker}&date_from={fromDate}&date_to={toDate}"
         response=requests.get(api_url)
         respDict=json.loads(response.text)
         for r in respDict: 
            tbox.insert("end",respDict[r])
            tbox.insert("end","\n")

     def showEod(self,stockname):
         labels=['Lowest','Highest','Open','Close']
         
         api_url=f'http://api.marketstack.com/v2/eod/latest?access_key={msApk}&symbols={stockname}'
         response=requests.get(api_url)
         data=json.loads(response.text)
         #data hakasuluissa json-tuloksen taulukon nimi low ja high ovat avain-arvo pareja
         for d in data['data']:
             low=d['low']
             high=d['high']
             openVal=d['open']
             close=d['close']
             name=d['symbol']
             dtime=d['date']
             dtimerep=dtime.replace("T"," ")
         nameStr=name+' Stock '+dtimerep
         self.values.append(low)
         self.values.append(high)
         self.values.append(openVal)
         self.values.append(close)
         
         plt.title(nameStr)
         plt.barh(labels,self.values)
         plt.show()

     
       

        
         
      
    