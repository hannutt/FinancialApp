import yfinance as yf
import matplotlib.pyplot as plt
from marketStack import MarketStack
import numpy as np
import customtkinter as ctk
class YahooFinance():
     def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ms=MarketStack()

        self.barValues=[]
        self.tickerlist=[]

        

     def getOption(self,val,stockcode,tbox,valuecb,tickerbtn,tickerEntry,multiple):
         self.tickerbtn=tickerbtn
         self.stockcode=stockcode
         self.tbox=tbox
         self.valuecb=valuecb
         self.tickerEntry=tickerEntry
         self.multiple=multiple
         self.optionDict={'Select':self.clearFields,'Recommendations':self.getRecomms,'Major Holders':self.getHolders ,'Mutual fund hold.':self.GetmutualFunds,'Dividends':self.getDividens,'Multiple tickers':self.multipleTickers,'General':self.stockGeneral}
         #käyttäjän valitsema vaihtoehto eli recommendations, holders jne
         self.val=val
         #metodin kutsu sulkeet lisätään tässä, muuten suoritetaan kaikki metodit
         self.optionDict[self.val]()
         #self.ticker=yf.ticker(self.stockcode)
     def clearFields(self):
         self.tickerbtn.grid_forget()
         self.multiple.grid_forget()
         
    
     def stockGeneral(self):
         stock = yf.Ticker(self.stockcode)
         info = stock.info
         self.tbox.insert("end",info['longName'])
         self.tbox.insert("end","\n")
         self.tbox.insert("end",info['sector'])
         self.tbox.insert("end","\n")
         self.tbox.insert("end",info['industry'])
         self.tbox.insert("end","\n")
         self.tbox.insert("end",info['marketCap'])
         self.tbox.insert("end","\n")
         self.tbox.insert("end",info['trailingPE'])

    
     def multipleTickers(self):
        
         self.tickerbtn.grid(row=5,column=1,sticky="E")
         self.multiple.grid(row=6,column=1,sticky="W")

     def setTickerToList(self):
         self.tickerlist.append(self.tickerEntry.get())

         self.tickerEntry.delete(0,"end")
    
     def getMultipleTickers(self):
         self.tbox.insert("end",yf.download(self.tickerlist, period='1d'))
         
         
    
     def getRecomms(self):
         ticker = yf.Ticker(self.stockcode)
         info=ticker.info
         
         recommendations=ticker.get_recommendations(proxy=None, as_dict=False)
         #buy,sell yms dict-objekteissa on 3 avainta jokaisessa 0-1-2
         #talletetaan vain avaimen 0 arvot.
         self.barValues.append(recommendations['buy'][0])
         self.barValues.append(recommendations['strongBuy'][0])
         self.barValues.append(recommendations['sell'][0])
         self.barValues.append(recommendations['strongSell'][0])
         self.barValues.append(recommendations['hold'][0])
         self.tbox.insert("end",recommendations)
         #configurella voi muuttaa toisessa luokassa määritellyn komponentin metodin uudelleen
         self.valuecb.configure(command=lambda:self.createBar(self.stockcode,info['longName']))
         self.valuecb.grid(row=11,column=1,sticky="E")
        
        
     def createBar(self,stockcode,name):
         fig, ax = plt.subplots()
         lbl = ["Buy", "Strong buy", "Sell", "Strong sell", "Hold"]
        
         bar_colors = ['tab:green', 'tab:cyan', 'tab:red','tab:orange','tab:brown']
         ax.bar(lbl,self.barValues,color=bar_colors)
         ax.set_title(name)
         plt.show()
     
    
     def getHolders(self):
         ticker = yf.Ticker(self.stockcode)
         holders=ticker.get_major_holders(proxy=None, as_dict=False)
         self.tbox.insert("end",holders)
    
     def GetmutualFunds(self):
         ticker = yf.Ticker(self.stockcode)
         funds=ticker.get_mutualfund_holders(proxy=None, as_dict=False)
         self.tbox.insert("end",funds)
         self.tbox.insert("end","\n")
    
     def getDividens(self):
         ticker = yf.Ticker(self.stockcode)
         dividends=ticker.get_dividends(proxy=None, period='max')
         self.tbox.insert("end",dividends)
    
     def yfHistory(self,sel,startdate,enddate,stockname,tbox):
         if sel=="History graph":
             
            stock = yf.Ticker(stockname)
            data = stock.history(start=startdate, end=enddate)

            fig, ax1 = plt.subplots(figsize=(14, 7))

            ax1.set_xlabel('Date')
            ax1.set_ylabel('Close Price', color='tab:red')
            ax1.plot(data.index, data['Close'], color='tab:red', label='Close Price')
            ax1.tick_params(axis='y', labelcolor='tab:red')

            ax2 = ax1.twinx()
            ax2.set_ylabel('Volume', color='tab:orange')
            ax2.bar(data.index, data['Volume'], color='tab:cyan', alpha=0.3, label='Volume')
            ax2.tick_params(axis='y', labelcolor='tab:cyan')

            plt.title(f'{stockname} Stock Price and Volume from {startdate} to {enddate}')
            fig.tight_layout()
            fig.legend(loc='upper left', bbox_to_anchor=(0.1,0.9))
            plt.grid(True)
            plt.show()
         elif sel=='Intraday':
             self.stockIntraday(stockname,tbox)
         elif sel=='Get history':
             self.ms.historicalData(stockname,tbox,startdate,enddate)
    
     def getComboBoxValue(self,combovalue):
         print(combovalue)
         self.combovalue=combovalue

     def stockIntraday(self,stockname,tbox):
         interval = self.combovalue
         stock = yf.Ticker(stockname)
         intraday_data = stock.history(period='1d', interval=interval)
        
         tbox.insert("end",intraday_data)
         
    
  
    
         
    
       
       
     
  