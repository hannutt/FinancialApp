import base64
from datetime import datetime
import json
import time
from bs4 import BeautifulSoup
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
from textwrap import wrap
from pathlib import Path
from openai import OpenAI
import vlc
from databaseConnection import DatabaseConnection
from tkinter import *
from tkcalendar import Calendar
apk=os.environ.get('apk')
mailtrap=os.environ.get('mailtrap')
oakey=os.environ.get('oakey')

class Options(ctk.CTk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fontChanged=False
        self.dbconn=DatabaseConnection()

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

    def deliveryFont(self,font):
        self.fontChanged=True
        self.fontname=font
        
    
    def deliveryFontSize(self,fsize):
        fsize=int(fsize)
        self.fsize=fsize
        self.dbconn.getFontSize(fsize)
       

    def createPdf(self,txtparam,cbparam):
        
        now=datetime.now()
        current_time = now.strftime("%H%M%S")
        fileName = 'data'+current_time+'.pdf'
        documentTitle = 'Data'
        title = 'Saved Data'
       
        pdf = canvas.Canvas(fileName) 
        pdf.setTitle(documentTitle) 
        pdf.setFont("Courier-Bold", 24) 
        #otsikon asemointi
        pdf.drawCentredString(300, 770, title) 
        # piirtää viivan otsikon alapuolelle.
        pdf.line(30, 710, 550, 710) 
  
        #tekstin lisääminen pdf-tiedostoon
        text = pdf.beginText(40, 680)
        if self.fontChanged:
            text.setFont(self.fontname,self.fsize)
        else:
            text.setFont("Courier",14)
      
        text.setFillColor(colors.black)
        #wrapilla saadaan koko teksti tiedostoon wrap myös pilkkoo tekstin riveiksi. 
        wraped_text = "\n".join(wrap(txtparam, 60)) # 60 is line width
        text.textLines(wraped_text)
        pdf.drawText(text) 
        pdf.save()
        
        #poistetaan checkboksin valinta 5 sekunnin jälkeen 
        time.sleep(5)
        cbparam.deselect()
      
   
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
    
    #tarkistetaan sähköpostin oikea muoto validateemail Apin kutsulla
    def emailFieldFocus(self):
        api_url = 'https://api.api-ninjas.com/v1/validateemail?email={}'.format(self.emailEntry.get())
        response = requests.get(api_url, headers={'X-Api-Key': apk})
        if response.status_code == requests.codes.ok:
              #luodaan respdict sanakirja, että saavaan talletettua avain-arvo pareja
              respDict=json.loads(response.text)

              #valid-muutujan arvoksi talletetaan sanakirjan is_valid avaimen arvo
              self.valid = respDict.get("is_valid")
              if self.valid==True:
                  self.sendBtn.configure(state='enabled')
             
        else:
            print("Error:", response.status_code, response.text)
       

    def emailOption(self):
        self.inputField=ctk.StringVar()
        self.mainComponents()
        self.titleLbl=ctk.CTkLabel(self.topWIn,text="Send email with attachments")
        self.titleLbl.grid(row=1)
        self.emailEntry=ctk.CTkEntry(self.topWIn,placeholder_text="email address",validate="focusout",validatecommand=self.emailFieldFocus)
        
        self.emailEntry.grid(row=2,sticky="ew")
        self.sendBtn=ctk.CTkButton(self.topWIn,text="Send",command=self.sendEmailPdf)
        self.sendBtn.configure(state='disabled')
        self.sendBtn.grid(row=3, sticky="ew")
     
      
    #haeetaan apista kaikki krypto tunnukset ja talletetaan ne csv-tiedostoon muodossa yksi symboli/rivi + symbols ja timestamp
    #otsikoilla.
    def getCryptos(self):
        api_url = "https://api.api-ninjas.com/v1/cryptosymbols"
        response = requests.get(api_url, headers={'X-Api-Key':apk})
        if response.status_code == requests.codes.ok:
            
            df=pd.read_json(response.text)
            df.to_csv('crypto.csv')
        else:
            print("Error:", response.status_code, response.text)
    
    def convertTts(self,text):
        
        client = OpenAI(api_key=oakey)
        speech_file_path = Path(__file__).parent / "tts.mp3"
        response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
        )
        response.stream_to_file(speech_file_path)
    
    def openTts(self,event):

        mp=vlc.MediaPlayer()
        media=vlc.Media("tts.mp3")
        mp.set_media(media)
        mp.play()
    
    def podcast(self,item):
        pods={"Talking Real Money":"https://traffic.megaphone.fm/APC9117150470.mp3?updated=1741723584","The Real Investment Show Podcast":"https://traffic.libsyn.com/secure/lancerobertsshow/RIS_3-11-25_TUESDAY_Best-of_Show.mp3?dest-id=797352"}
        self.p=vlc.MediaPlayer(pods[item])
        self.p.play()
    
    def stopPodcast(self):
        self.p.stop()
    
    

    def createMetals(self,preciousmenu,codefield):
       
         preciousmenu.grid(row=4, column=1,padx=10, pady=10,columnspan=1, sticky="ew")
         codefield.grid_forget()
    
    
    
            

    
   
    

    

    
    
   
    
   
   

       
    
   
    


        
        
    
      
