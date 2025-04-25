import yfinance as yf
import matplotlib.pyplot as plt
from marketStack import MarketStack
class YahooFinance():
     def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ms=MarketStack()

        

     def getOption(self,val,stockcode,tbox):
         self.stockcode=stockcode
         self.tbox=tbox
         self.optionDict={'Recommendations':self.getRecomms,'Major Holders':self.getHolders ,'Mutual fund hold.':self.GetmutualFunds,'Dividends':self.getDividens}
         #käyttäjän valitsema vaihtoehto eli recommendations, holders jne
         self.val=val
         #metodin kutsu sulkeet lisätään tässä, muuten suoritetaan kaikki metodit
         self.optionDict[self.val]()
         self.ticker=yf.ticker(self.stockcode)
    
     def getRecomms(self):
         ticker = yf.Ticker(self.stockcode)
         recommendations=ticker.get_recommendations(proxy=None, as_dict=False)
         self.tbox.insert("end",recommendations)
    
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
         
    
  
    
         
    
       
       
     
  