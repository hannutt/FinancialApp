
from bs4 import BeautifulSoup
from tkcalendar import DateEntry
import customtkinter as ctk
import requests
import feedparser
import ssl
from dotenv import load_dotenv
import os
import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from options import Options
from newsapi import NewsAPI
from marketStack import MarketStack
from PIL import Image
from databaseConnection import DatabaseConnection
from ApiNinjas import Apininjas
import speech_recognition as sr
from datetime import datetime
from pytube import YouTube
import webbrowser
import vlc
from Scraper import Scrape



#Api-avain on talletettu env-muuttujaan, tässä haetaan sen sisältämä merkkijono
apk=os.environ.get('apk')
#Asettaa sovelluksen ulkoasutilan System määrittää ulkoasun saman kuin järjestelmän. dark on tumma teema
ctk.set_appearance_mode("Dark")        
 
# Sets the color of the widgets
# Supported themes: green, dark-blue, blue
ctk.set_default_color_theme("green")    
 
class App(ctk.CTk,tk.Menu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font = ctk.CTkFont(family="Times", size=14)
        self.words=['Crypto','Stocks','Precious metals','Commodities','History','Finance Dictionary','Inflation','Listen podcasts','Index history','Stock index by country']
        self.title("Finance App")
        self.menubar=tk.Menu(self)
        self.config(menu=self.menubar)
        self.opt=Options()
        self.news=NewsAPI()
        self.dbconn=DatabaseConnection()
        self.ms=MarketStack()
        self.an=Apininjas()
        self.sc=Scrape()
       
        #App luokan textbox voidaan lähettää  options luokalle parametria command=lambda:o.currencyWidgets(self.textbox))
        self.menubar.add_command(label='Cur. convert',command=lambda:self.opt.currencyWidgets())
        self.menubar.add_command(label='Exchange rate',command=lambda:self.opt.createExcWidgets())
        self.menubar.add_command(label='Give voice comm.',command=lambda:self.speechReg())
        self.menubar.add_command(label='earnings',command=lambda:self.an.fetchOnlyEarnings(self.codeEntry.get()))
        self.menubar.add_command(label='email',command=lambda:self.opt.emailOption())
        
          
        #self.add_cascade()
        self.graph=False
        self.inputField=ctk.StringVar()
        #ikkunan koko
        self.geometry("450x450")
        self.appname=ctk.CTkLabel(self,text='FINACIAL DATA FROM API-SOURCES')
        self.appname.grid(row=1,column=1,sticky='e')
        #kuvan lisäys
        self.appImage=ctk.CTkImage(light_image=Image.open('images/financeAppImg.jpg'),dark_image=Image.open('images/financeAppImg.jpg'),size=(300,80))
        #kuva näytetään label komponentissa
        self.appimageLbl=ctk.CTkLabel(self,text="",image=self.appImage)
        self.appimageLbl.grid(row=2,column=1,sticky="e")
        
        #pudotusvalikko
        self.preciousMenu = ctk.CTkOptionMenu(self,
                                        values=["Gold"],command=self.gold_callback)
        self.optMenu = ctk.CTkOptionMenu(self,
                                        values=['Select',"Crypto","Stocks",'Commodities','Precious metals','History','Finance Dictionary','Inflation','Listen podcasts','Index history','Stock index by county'],command=self.optionmenu_callback,width=200)
        self.optMenu.grid(row=3, column=1, pady=10,columnspan=1, sticky="w")

        self.comMenu = ctk.CTkOptionMenu(self,
                                        values=["Oat","Platinum",'Gold','Palladium'],command=self.commodity_callback)

        self.codeEntry = ctk.CTkEntry(self,placeholder_text="crypto/stock code",textvariable=self.inputField,validate="focusout", validatecommand=self.showInput)
        self.earningsSV=ctk.StringVar()
        self.earnings=ctk.CTkCheckBox(self,text="Show earnings?", onvalue="on", offvalue="off", variable=self.earningsSV)
        self.newsAboutComp=ctk.CTkCheckBox(self,text="News?",command=lambda:self.news.companyNews(self.codeEntry.get(),self.textbox))
        
        self.createStockBars=ctk.CTkCheckBox(self,text="EOD data",command=lambda:self.ms.showEod(self.codeEntry.get()))
        self.dividends=ctk.CTkCheckBox(self,text="Dividends",command=lambda:self.ms.getDividends(self.codeEntry.get(),self.textbox))

        self.getBtn=ctk.CTkButton(self,text="Get data",command=self.selectMethods,width=200)
        self.getBtn.grid(row=7,column=1,columnspan=3,sticky="w",pady=10)
        self.textbox=ctk.CTkTextbox(self,width=200,corner_radius=5,height=105,font=self.font)
     
        self.textbox.grid(row=9,column=1,sticky="ew",columnspan=1)
        #lambdan avulla voidaan antaa metodille parametri, ilman lambdaa metodi jossa on () merkit
        #suoritetaan heti
        self.rssSV=ctk.StringVar()
        self.klUrl=ctk.StringVar(value="https://feeds.kauppalehti.fi/rss/main")
        self.klRss=ctk.CTkCheckBox(self,text="Kauppalehti RSS",command=lambda:self.selRssSource(self.klUrl.get()),onvalue="on",offvalue="off")
        self.klRss.grid(row=1,column=7,columnspan=3)
        self.clearBtn=ctk.CTkButton(self,text="Clear",command=self.clearTextBox)
        self.clearBtn.grid(row=10,column=1,pady=(10,10),sticky="w")
        self.saveBtn=ctk.CTkButton(self,text='Save',command=lambda:self.dbconn.DBsave(self.textbox.get('1.0',END)))
        self.saveBtn.grid(row=10,column=1,sticky="e")
        self.saveToCsv=ctk.CTkCheckBox(self,text="Save to CSV file?",command=lambda:self.dbconn.CsvSave(self.textbox.get('1.0',END)))
        self.saveToCsv.grid(row=11,column=1,sticky="w")
        self.saveToCsv=ctk.CTkCheckBox(self,text="Save to PDF file?",command=lambda:self.opt.createPdf(self.textbox.get('1.0',END),self.saveToCsv))
        self.saveToCsv.grid(row=12,column=1,sticky="w")
        self.fontMenu = ctk.CTkOptionMenu(self,
                                        values=['Courier',"Helvetica","Times-Roman"],width=100,command=self.opt.deliveryFont)
        self.fontMenu.grid(row=13, column=1,sticky="w")
        #self.fontMenu.set("Courier")

        self.fontSizeMenu=ctk.CTkOptionMenu(self,values=['12','14','16','18','20'], width=100, command=self.opt.deliveryFontSize)
        self.fontSizeMenu.grid(row=13,column=1,sticky="E")

        #zoomintext metodi saa parametrina fontin tyypin (self.font) ja fontin koon (self.font._size)
        self.tts=ctk.CTkButton(self,width=20,text="TTS",command=lambda:self.opt.convertTts(self.textbox.get('1.0',END)))
        self.tts.grid(row=8,column=2)
        self.zoomIn=ctk.CTkButton(self,text="+",width=50,command=lambda:self.opt.zoomInText(self.font,self.font._size))
        self.zoomIn.grid(row=9,column=2,padx=10)
        self.zoomOut=ctk.CTkButton(self,text="-",width=50,command=lambda:self.opt.zoomOutText(self.font,self.font._size))
        self.zoomOut.grid(row=9,column=2,sticky="s")
    
        self.invUrl=ctk.StringVar(value='https://fi.investing.com/rss/news_25.rss')
        self.invRss=ctk.CTkCheckBox(self,text="Investing RSS",command=lambda:self.selRssSource(self.invUrl.get()),variable=self.rssSV,onvalue="on",offvalue="off")
        self.invRss.grid(row=2,column=7,sticky="nw")

        self.wUrl=ctk.StringVar()
        self.writeUrl=ctk.CTkCheckBox(self,text="Own RSS url?",variable=self.wUrl,onvalue="on",offvalue="off",command=self.showInput)
        #pady(10,0) tarkoittaa, että ylös lisätään 10 pikseliä tyhjää tilaa ja alas 0 pikseliä
        self.writeUrl.grid(row=2,column=7,sticky="ew")
        self.ytUrl=ctk.StringVar()
        self.youtubeUrl=ctk.CTkCheckBox(self,text="Youtube video",variable=self.ytUrl,onvalue="on",offvalue="off",command=self.showInput)
        self.youtubeUrl.grid(row=3,column=7,sticky="ew")

        self.valueCB=ctk.CTkCheckBox(self,text="Graphics",command=self.an.DrawGraphics)
    
    def speechReg(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio_text = r.listen(source,timeout=8.0)
    
        try:
            if r.recognize_google(audio_text)=="stocks":
                self.voice_stocks()
            if r.recognize_google(audio_text)=="clear":
                self.clearTextBox()
            if r.recognize_google(audio_text)=="crypto":
                self.codeEntry.grid(row=5, column=1,columnspan=1, padx=20,pady=20, sticky="ew")
            if r.recognize_google(audio_text)=="stock info":
                 self.an.fetchData()
            if r.recognize_google(audio_text)=="save":
                 self.dbconn.DBsave(self.textbox.get('1.0',END))
            
        except:
             print("error")

    def clearTextBox(self):
        self.textbox.delete("0.0","end")
        self.klRss.deselect()
        self.invRss.deselect()
        self.writeUrl.deselect()

    #käyttäjän antama rss-syötteen osoite
    def showInput(self):
        if self.wUrl.get()=="on":

            self.urlInput=ctk.CTkEntry(self)
            self.urlInput.grid(row=4,column=7,sticky="EW")
            #focuosut eventin ja metodin sitominen toisiinsa.
            self.urlInput.bind('<FocusOut>',self.inputFocusOut)
        elif self.ytUrl.get()=="on":
            self.urlInput.grid(row=4,column=7,sticky="EW")
            self.urlInput.bind('<FocusOut>',self.showYoutubeVideo)
        else:
            self.urlInput.grid_forget()
        
        
    def showYoutubeVideo(self,event):
            url = self.urlInput.get()
            yt = YouTube(url)
            webbrowser.open(url)
          
    #event parametri on tapahtuma eli se kun kursori poistuu entry kentästä.
    def inputFocusOut(self,event):
        
        self.url=self.urlInput.get()
        self.fetchRssData()
    
        
    def optionmenu_callback(self,choice):
        self.choice=choice
        #tarkistus, onko valittu arvo words-listassa
        if self.choice in self.words:
            self.codeEntry.grid(row=5, column=1, sticky="ew")
            if self.choice=="Stocks":
                self.earnings.grid(row=6,column=1,sticky="W")
                self.newsAboutComp.grid(row=6,column=1,sticky="E")
                self.createStockBars.grid(row=6,column=2,sticky="E")
                self.dividends.grid(row=6,column=3,sticky="E")
            elif self.choice=="Precious metals":
                self.opt.createMetals(self.preciousMenu,self.codeEntry)
            elif self.choice=="Crypto":
                self.cryptoCsv=ctk.CTkCheckBox(self,text="Save cryptos to CSV",command=lambda:self.opt.getCryptos())
                self.newsAboutComp.grid(row=6,column=1,sticky="W")
                self.cryptoCsv.grid(row=6,column=1,sticky="E")
            
            elif self.choice=="Commodities":
                
                self.codeEntry.grid_forget()
                self.opt.createCommodity(self.comMenu)

            elif self.choice=="History":
                self.codeEntry.grid(row=5, column=1,sticky="W")
                self.historyCB=ctk.CTkCheckBox(self,text="Get history",command=lambda:self.ms.historicalData(self.codeEntry.get(),self.textbox,self.fromDate.get(),self.toDate.get()))
                
                self.historyCB.grid(row=5,column=1,sticky="E")
                self.fromDate=ctk.CTkEntry(self,placeholder_text="FROM (YYYY-MM-DD)")
                self.fromDate.grid(row=6,column=1,sticky="W")
                self.fromDate.bind("<Button>",self.calendarMethod)
                self.toDate=ctk.CTkEntry(self,placeholder_text="TO (YYYY-MM-DD)")
                self.toDate.bind("<Button>",self.setCalDateToEnd)
                self.toDate.grid(row=6,column=1,sticky="E")
                self.getBtn.grid_forget()
            elif self.choice=="Finance Dictionary":
                self.codeEntry.grid_forget()
                self.getBtn.grid_forget()
                self.getTermBtn=ctk.CTkButton(self,text='Get data',command=lambda:self.dbconn.getData(self.textbox))
                self.getTermBtn.grid(row=5,column=1,sticky="E")
                self.financeDict=ctk.CTkOptionMenu(self,values=['Select','p/e','eps','adr','bear market'],command=self.dbconn.getFinanceTerm)
                self.financeDict.grid(row=5,column=1,sticky="W")
            elif choice=="Inflation":
                self.getBtn.grid_forget()
                self.getInflationBtn=ctk.CTkButton(self,text="Get inflation",command=lambda:self.ms.getInflation(self.codeEntry.get(),self.textbox))
                self.getInflationBtn.grid(row=7,column=1,columnspan=3,sticky="w",pady=10)
                self.codeEntry.grid(row=5, column=1, sticky="ew")
            elif choice=="Listen podcasts":
                self.podcasts=ctk.CTkOptionMenu(self,values=['Select','Talking Real Money','The Real Investment Show Podcast'],command=self.opt.podcast)
                self.codeEntry.grid_forget()
                self.getBtn.grid_forget()
                self.podcasts.grid(row=5,column=1,sticky="W")
                self.podstop=ctk.CTkButton(self,text='Stop',width=20,command=self.opt.stopPodcast)
                self.podstop.grid(row=6,column=1,sticky="W",pady=10)

            elif choice=='Index history':
                 self.userSelection=ctk.StringVar()
                 #lambda x: voidaan lähettää option menun valinnan lisäksi muita parametreja.
                 self.indexMenu=ctk.CTkOptionMenu(self,values=['Select','NASDAQ 100','DAX'],command=lambda x:self.sc.stockIndex(x,self.textbox))
                 self.indexMenu.grid(row=5,column=1,sticky="W")
                 self.codeEntry.grid_forget()
                 self.getBtn.grid_forget()
                
                
        else:
            #piilottaa gridit
            self.codeEntry.grid_forget()
            self.earnings.grid_forget()
            self.preciousMenu.grid_forget()
            self.comMenu.grid_forget()
            
            self.newsAboutComp.grid_forget()
            self.createStockBars.grid_forget()
            self.podcasts.grid_forget()
            self.podstop.grid_forget()
            self.cryptoCsv.grid_forget()
            
            #muutetaan buttonin tekstiä configuren avulla
            self.getBtn.configure(text="Get " +self.choice+" data")
    #commodity metodi suoritetaan heti, kun pudotusvalikosta on valittu jokin arvo, comm parametri
    # sisältää valitun arvon.

        
            
    def commodity_callback(self,comm):
        api_url="https://api.api-ninjas.com/v1/commodityprice?name={}".format(comm)
        response = requests.get(api_url, headers={'X-Api-Key': apk})
        if response.status_code == requests.codes.ok:
             respDict=json.loads(response.text)
             for r in respDict:

                self.textbox.insert('end',respDict[r])
                self.textbox.insert('end',"\n")
             self.price = respDict.get("price")
             self.name=respDict.get("name")
            #unix timestampin muunto luettavaksi päivämääräksi
             utime=respDict.get("updated")
             utimeInt=int(utime)
             datetimesStr=datetime.fromtimestamp(utimeInt).strftime('%d-%m-%Y %H:%M:%S')
             self.textbox.insert("end",datetimesStr)
          
             self.valueCB.grid(row=11,column=1,columnspan=3)
             self.valueCB.configure(text=self.name+" Graphics")     
        else:
            print("Error:", response.status_code, response.text)
    
    def gold_callback(self,val):
        api_url='https://api.api-ninjas.com/v1/goldprice'
        response = requests.get(api_url, headers={'X-Api-Key': apk})
        if response.status_code == requests.codes.ok:
             respDict=json.loads(response.text)
             for r in respDict:

                self.textbox.insert('end',respDict[r])
                self.textbox.insert('end',"\n")
             self.price = respDict.get("price")
             self.name=val
             self.valueCB.grid(row=11,column=1,columnspan=3)
             self.valueCB.configure(text=self.name+" Graphics") 

    
    def selRssSource(self,url):
        self.url=url
        self.fetchRssData()
      

    def fetchRssData(self):
        #ssl-handshake
        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context
        feed = feedparser.parse(self.url)
        #entries on syötteen sisältämät tagit
        for f in feed.entries:
            #näytetään kaikki title tagien sisältämä data

            self.textbox.insert("end",f.title)

    def selectMethods(self):
        print(self.earningsSV.get())
        #jos stocks on valittu pudotusvalikosta earning cb on valittu
        if self.choice=="Stocks" and self.earningsSV.get()=="on":
            self.an.fetchData(self.textbox,self.codeEntry.get(),self.valueCB)
            self.an.fetchEarnings(self.textbox,self.codeEntry.get())
        elif self.choice=="Stocks":
           
            self.an.fetchData(self.textbox,self.codeEntry.get(),self.valueCB)
        elif self.choice=="Crypto":
            self.an.fetchCryptoData(self.textbox,self.valueCB,self.codeEntry.get())
    
    
    def voice_stocks(self):
         self.codeEntry.grid(row=5, column=1,columnspan=1, padx=20,pady=20, sticky="ew")
         self.earnings.grid(row=6,column=1,sticky="W")
         self.newsAboutComp.grid(row=6,column=1,sticky="E")
    
    def calendarMethod(self,event):
        self.cal = DateEntry(self, date_pattern="yyyy-mm-dd")
        self.cal.grid(row=7,column=1,sticky="W",pady=10)
        self.cal.bind("<FocusOut>",self.setCalDate) 
    
    def setCalDate(self,event):
        self.fromDate.delete(0,END)
        self.selected_date = self.cal.get()
        self.fromDate.insert(0,self.selected_date)
        self.cal.grid_forget()
        
    def setCalDateToEnd(self,event):
         self.cal = DateEntry(self, date_pattern="yyyy-mm-dd")
         self.cal.grid(row=7,column=1,sticky="W",pady=10)
         self.cal.bind("<FocusOut>",self.setCalDateToEndField)
            
    def setCalDateToEndField(self,event):
        self.toDate.delete(0,END)
        self.selected_date2 = self.cal.get()
        self.toDate.insert(0,self.selected_date2)
        self.cal.grid_forget()
    
  
 
if __name__ == "__main__":

    app = App()
    # Runs the app
    app.mainloop()    