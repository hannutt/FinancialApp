from datetime import datetime
import json
import os
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
import requests
 
apk=os.environ.get('apk')
class Apininjas():
      def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dTime=datetime.now().strftime("%d.%m.%Y")
    
      def fetchCryptoData(self,tbox,valuecb,crypto):
        api_url ='https://api.api-ninjas.com/v1/cryptoprice?symbol={}'.format(crypto)
        response = requests.get(api_url, headers={'X-Api-Key': apk})
        if response.status_code == requests.codes.ok:

            #json-vastaus muunnetaan python dictionary objektiksi.
            respDict=json.loads(response.text)
            #unix timestampin muunto luettavaksi päivämääräksi
            utime=respDict.get("timestamp")
            utimeInt=int(utime)
            datetimesSter=datetime.fromtimestamp(utimeInt).strftime('%d-%m-%Y %H:%M:%S')
            tbox.insert("end",datetimesSter)
            tbox.insert("end","\n")
            for r in respDict:
                
                tbox.insert('end',respDict[r])
                tbox.insert('end',"\n")
            #talletetaan muuttujaan sanakirjan price avaimen arvo
            self.price = respDict.get("price")
            self.name=respDict.get("symbol")
            
            valuecb.grid(row=11,column=1)
            valuecb.configure(text=self.name+" Graphics")
        else:
            print("Error:", response.status_code, response.text)  


      def fetchData(self,tbox,ticker,valuecb):
            
            #self.codeEntry.get() = tekstikentän sisältö 
            api_url = 'https://api.api-ninjas.com/v1/stockprice?ticker={}'.format(ticker)
            response = requests.get(api_url, headers={'X-Api-Key': apk})
            if response.status_code == requests.codes.ok:
                self.analystConsensus(ticker)
                #json-vastaus muunnetaan python dictionary objektiksi.
                respDict=json.loads(response.text)
                utime=respDict.get("updated")
                utimeInt=int(utime)
                datetimeStr=datetime.fromtimestamp(utimeInt).strftime('%d-%m-%Y %H:%M:%S')
                self.price = respDict.get("price")
                self.name=respDict.get("name")
                self.currency=respDict.get("currency")
                tbox.insert("end","UPDATED:")
                tbox.insert("end",datetimeStr+"\n" )
                tbox.insert("end",str(self.name)+"\n")
                tbox.insert("end",str(self.price)+"\n")
                tbox.insert("end",str(self.currency)+"\n")
                tbox.insert("end",str(self.data.get_text())+"\n")
                tbox.insert("end","Target price: ")
                tbox.insert("end",str(self.target.get_text()))
            
                valuecb.grid(row=11,column=1,columnspan=3)
                valuecb.configure(text=self.name+" Graphics")
      
      #metodi hakee web-scrapingin ja käyttäjän syöttämän kaupankäyntitunnuksen perusteella
      #osakkeen suosituksen
      def analystConsensus(self,ticker):
          response = requests.get(f'https://stockanalysis.com/stocks/{ticker}/forecast/')
          soup = BeautifulSoup(response.text, 'html.parser')
          self.data = soup.find(class_='-mt-2 text-center text-xl font-semibold')
          self.target=soup.find(class_='whitespace-nowrap px-0.5 py-[1px] text-left text-smaller font-semibold tiny:text-base xs:px-1 sm:py-2 sm:text-right sm:text-small')
        

      def DrawGraphics(self):
        nameAndTime=f'{self.name} {self.dTime}'
        plt.bar(nameAndTime,self.price,width=0.4)
        plt.show()
    
      def fetchOnlyEarnings(self,company):
        self.epsList=[]
        api_url='https://api.api-ninjas.com/v1/earningscalendar?ticker={}'.format(company)
        response = requests.get(api_url, headers={'X-Api-Key': apk})
        if response.status_code == requests.codes.ok:
            #JSON VASTAUKSESTA HAETAAN AINOASTAAN ESTIMATED_EPS KENTÄN ARVOT
            data=json.loads(response.text)
            for e in data:
                eps=e["estimated_eps"]
                self.epsList.append(eps)
            #numeroiden järjestys min-max
            self.epsList.sort()
       
            plt.title(company +' Earnings')
            plt.plot(self.epsList, marker = 'o', ms = 15, mec = '#4CAF50', mfc = '#4CAF50')
            plt.show()

      def fetchEarnings(self,tbox,ticker):

        api_url='https://api.api-ninjas.com/v1/earningscalendar?ticker={}'.format(ticker)
        response = requests.get(api_url, headers={'X-Api-Key': apk})
        if response.status_code == requests.codes.ok:
            tbox.insert("end",response.text)
    