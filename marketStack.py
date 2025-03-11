
from datetime import datetime
import json
import requests
import os
import matplotlib.pyplot as plt

msApk=os.environ.get('msapk')
apk=os.environ.get('apk')

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
     
     def getInflation(self,country,tbox):
          api_url="https://api.api-ninjas.com/v1/inflation?country={}".format(country)
          response = requests.get(api_url, headers={'X-Api-Key': apk})
          if response.status_code == requests.codes.ok:
              tbox.insert("end",response.text)
              
          else:
            print("Error:", response.status_code, response.text)

     def getDividends(self,ticker,tbox):
        dNow=datetime.today().strftime('%Y-%m-%d')
        api_url=f"https://api.marketstack.com/v2/dividends?access_key={msApk}&symbols={ticker}&date_from=2025-01-01"
        response=requests.get(api_url)
        data=json.loads(response.text)
        for d in data['data']:
            Divdate=d['date']
            symbol=d['symbol']
            dividend=d['dividend']
          
        tbox.insert("end",symbol)
        tbox.insert("end","\n")
        tbox.insert("end",dividend)
        tbox.insert("end","\n")
        tbox.insert("end",Divdate)
     
     
       

        
         
      
    