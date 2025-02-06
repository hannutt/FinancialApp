import customtkinter as ctk
import os


import requests
apk=os.environ.get('apk')

class Options(ctk.CTk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

    def mainComponents(self):
        self.topWIn=ctk.CTkToplevel()
        self.textbox=ctk.CTkTextbox(self.topWIn)
        self.topWIn.geometry('250x250')
    
        

        
    def currencyWidgets(self):
        self.mainComponents()
        self.curLbl=ctk.CTkLabel(self.topWIn,text="Currency convert")
        self.cur1=ctk.CTkEntry(self.topWIn, placeholder_text="FROM")
        self.cur2=ctk.CTkEntry(self.topWIn, placeholder_text="TO")
        self.amount=ctk.CTkEntry(self.topWIn,placeholder_text="AMOUNT")
        self.curBtn=ctk.CTkButton(self.topWIn,text="Set",command=self.currencyExchange)
      
        self.curLbl.grid(row=1)
        self.cur1.grid(row=2)
        self.cur2.grid(row=3)
        self.amount.grid(row=4)
        self.curBtn.grid(row=5)
        self.textbox.grid(row=6)
       
     
    
    def createExcWidgets(self):
        self.mainComponents()
        self.optMenu = ctk.CTkOptionMenu(self.topWIn,values=['CNY_GBP','CHF_NZD','AUD_KRW','PLN_DKK','TRY_HKD'],command=self.rates_callback)
        self.optMenu.grid(row=2,pady=8)
        self.rateBtn=ctk.CTkButton(self.topWIn,text="Show rate",command=self.rates_callback)
        self.textbox.grid(row=3)
    
    
    def rates_callback(self,pairs):
        api_url=f"https://api.api-ninjas.com/v1/exchangerate?pair={pairs}"
        response = requests.get(api_url, headers={'X-Api-Key': apk})
        if response.status_code == requests.codes.ok:
            self.textbox.insert("end",response.text)
    
    def currencyExchange(self):
        api_url=f'https://api.api-ninjas.com/v1/convertcurrency?have={self.cur1.get()}&want={self.cur2.get()}&amount={self.amount.get()}'
        response = requests.get(api_url, headers={'X-Api-Key': apk})
        if response.status_code == requests.codes.ok:
            self.textbox.insert("end",response.text)
        else:
             print("Error:", response.status_code, response.text)
    
   
    


        
        
    
      
