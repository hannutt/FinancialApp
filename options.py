import base64
import time
import customtkinter as ctk
import os
import mailtrap as mt
from reportlab.pdfgen import canvas 
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.pdfbase import pdfmetrics 
from reportlab.lib import colors
import requests 
from pathlib import Path
import pandas as pd

apk=os.environ.get('apk')
mailtrap=os.environ.get('mailtrap')

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
    
    def zoomInText(self,fontParam,fsize):
        fsize+=2
        fontParam.configure(size=fsize)
    
    def zoomOutText(self,fontParam,fsize):
        fsize-=2
        fontParam.configure(size=fsize)
    

    def createPdf(self,txtparam,cbparam):
        fileName = 'data.pdf'
        documentTitle = 'Data'
        title = 'Saved Data'
       
        textLines = []
        textLines.append(txtparam)
        pdf = canvas.Canvas(fileName) 
        pdf.setTitle(documentTitle) 
        pdf.setFont("Courier-Bold", 24) 
        #otsikon asemointi
        pdf.drawCentredString(300, 770, title) 
        # piirtää viivan otsikon alapuolelle.
        pdf.line(30, 710, 550, 710) 
  
        #tekstin lisääminen pdf-tiedostoon
        text = pdf.beginText(40, 680) 
        text.setFont("Courier", 18) 
        text.setFillColor(colors.black) 
  
        for line in textLines: 
            text.textLine(line) 
      
        pdf.drawText(text) 
        pdf.save()
        #poistetaan checkboksin valinta 5 sekunnin jälkeen 
        time.sleep(5)
        cbparam.deselect()
    
   
    def changeSendBtnText(self):
        newtext=self.emailEntry.get()
        print(newtext)
        #self.sendBtn.configure(text="Send to "+newtext)
      
        #self.sendBtn.configure(text="send to "+newtext)
       

    def sendEmailPdf(self):
        #tiedostodialogi, valittu tiedosto polkuineen talletetaan pdfFile muuttujaan.
        pdfFile=ctk.filedialog.askopenfilename()
        #tiedoston muunto biteiksi
        datafile = Path(__file__).parent.joinpath(pdfFile).read_bytes()
        mail = mt.Mail(
            sender=mt.Address(email="hello@demomailtrap.com", name="Mailtrap Test"),
            to=[mt.Address(email=self.emailEntry.get())],
            subject="Data you saved",
            text="pdf is in attachment!",
            category="Finance app function",
        attachments=[

        mt.Attachment(
            content=base64.b64encode(datafile),
            filename=pdfFile,
            disposition=mt.Disposition.INLINE,
            mimetype="application/pdf",
            content_id=pdfFile,
        )
    ],    
    )
        client = mt.MailtrapClient(token=mailtrap)
        response = client.send(mail)
        print(response)
        
      

    def emailOption(self):
        self.inputField=ctk.StringVar()
        self.mainComponents()
        self.emailEntry=ctk.CTkEntry(self.topWIn,placeholder_text="email address",textvariable=self.inputField)
        self.emailEntry.grid(row=2,sticky="ew")
        self.sendBtn=ctk.CTkButton(self.topWIn,text="Send",command=self.sendEmailPdf)
        self.sendBtn.grid(row=3, sticky="ew")
        #self.emailEntry.bind('<FocusOut>',self.changeSendBtnText)
      

    #haeetaan apista kaikki krypto tunnukset ja talletetaan ne csv-tiedostoon muodossa yksi symboli/rivi + symbols ja timestamp
    #otsikoilla.
    def getCryptos(self):
        api_url = "https://api.api-ninjas.com/v1/cryptosymbols"
        response = requests.get(api_url, headers={'X-Api-Key': 'PaxMyj61EqrhOiBgI7yCHg==BDWXkkNweuTES9sM'})
        if response.status_code == requests.codes.ok:
            df=pd.read_json(response.text)
            df.to_csv('crypto.csv')
            
        else:
            print("Error:", response.status_code, response.text)
   
   

       
    
   
    


        
        
    
      
