import yfinance as yf
class YahooFinance():
     def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        

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
    
       
       
     
  