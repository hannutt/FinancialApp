import yfinance as yf
class YahooFinance():
     def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        

     def getOption(self,val,stockcode,tbox):
         self.stockcode=stockcode
         self.tbox=tbox
         self.optionDict={'Recommendations':self.getRecomms,'Major Holders':self.getHolders}
         #käyttäjän valitsema vaihtoehto eli recommendations, holders jne
         self.val=val
         #metodin kutsu sulkeet lisätään tässä, muuten suoritetaan kaikki metodit
         self.optionDict[self.val]()

         

    
     def getRecomms(self):
         ticker = yf.Ticker(self.stockcode)
         recommendations=ticker.get_recommendations(proxy=None, as_dict=False)
         self.tbox.insert("end",recommendations)
    
     def getHolders(self):
         ticker = yf.Ticker(self.stockcode)
         holders=ticker.get_major_holders(proxy=None, as_dict=False)
         self.tbox.insert("end",holders)
   
       
       
     
  