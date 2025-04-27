
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
from ttkwidgets.autocomplete import AutocompleteEntry
from options import Options
from newsapi import NewsAPI
from marketStack import MarketStack
from PIL import Image
from databaseConnection import DatabaseConnection
from ApiNinjas import Apininjas
import speech_recognition as sr
from datetime import datetime
from uiScripts import UiScripts

import vlc
from Scraper import Scrape
from CTkMessagebox import CTkMessagebox
from yahooFinance import YahooFinance
from googleDrive import GDrive


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
        self.words=['Crypto','Stocks','Commodities','History','Finance Dictionary','Listen podcasts','Index history','Stock index by country','Yahoo Finance']
        self.title("Finance App")
        self.menubar=tk.Menu(self)
        self.config(menu=self.menubar)
        self.opt=Options()
        self.news=NewsAPI()
        self.dbconn=DatabaseConnection()
        self.ms=MarketStack()
        self.an=Apininjas()
        self.sc=Scrape()
        self.ytf=YahooFinance()
        self.gd=GDrive()
        self.us=UiScripts()

        self.tickerPath=""
        
        
        #App luokan textbox voidaan lähettää  options luokalle parametria command=lambda:o.currencyWidgets(self.textbox))
        #self.menubar.add_command(label='Cur. convert',command=lambda:self.opt.currencyWidgets())
        #self.menubar.add_command(label='Exchange rate',command=lambda:self.opt.createExcWidgets())
        self.menubar.add_command(label='Give voice comm.',command=lambda:self.speechReg())
        self.menubar.add_command(label='earnings',command=lambda:self.an.fetchOnlyEarnings(self.codeEntry.get()))
        self.menubar.add_command(label='Send email',command=lambda:self.opt.emailOption())
        self.menubar.add_command(label='Newest ETFs',command=lambda:self.showDialog())
        
     
     
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
       
        self.optMenu = ctk.CTkOptionMenu(self,
                                        values=['Select',"Crypto","Stocks",'Commodities','History','Finance Dictionary','Listen podcasts','Index history','Stock index by country','Yahoo Finance'],command=self.optionmenu_callback,width=200)
        self.optMenu.grid(row=3, column=1, pady=10,columnspan=1, sticky="w")

        self.comMenu = ctk.CTkOptionMenu(self,
                                        values=["Oat","Platinum",'Gold','Palladium'],command=self.commodity_callback)

        self.codeEntry = ctk.CTkEntry(self,placeholder_text="crypto/stock code",textvariable=self.inputField,validate="focusout", validatecommand=self.showInput,width=200)
        self.earningsSV=ctk.StringVar()
        self.earnings=ctk.CTkCheckBox(self,text="Show earnings?", onvalue="on", offvalue="off", variable=self.earningsSV)
        self.newsAboutComp=ctk.CTkCheckBox(self,text="News?",command=lambda:self.news.companyNews(self.codeEntry.get(),self.textbox))
        
      
        self.getBtn=ctk.CTkButton(self,text="Get data",command=self.selectMethods,width=200)
        self.getBtn.grid(row=7,column=1,columnspan=3,sticky="w",pady=10)
        self.textbox=ctk.CTkTextbox(self,width=200,corner_radius=5,height=105,font=self.font)

        self.acVar=StringVar()
        self.useAC=ctk.CTkCheckBox(self,text="Autocomplete",variable=self.acVar, onvalue="on",offvalue="off",command=self.showAc)
        
     
        self.textbox.grid(row=9,column=1,sticky="ew",columnspan=1)
        self.podcasts=ctk.CTkOptionMenu(self,values=['Select','Talking Real Money','The Real Investment Show Podcast'],command=self.opt.podcast)
        self.podstop=ctk.CTkButton(self,text='Stop',width=20,command=self.opt.stopPodcast)
        #pikanäppäin bindaus, ctrl+m suoritaa majorIndexes metodin
        self.bind("<Control-m>",lambda x:self.sc.majorIndexes(x,self.textbox))
        self.bind("<Control-s>",self.opt.openTts)
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
        self.tts.grid(row=9,column=2,sticky="n")
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
        self.financeDict=ctk.CTkOptionMenu(self,values=['Select','p/e','eps','adr','bear market'],command=self.dbconn.getFinanceTerm)
        self.getTermBtn=ctk.CTkButton(self,text='Get data',command=lambda:self.dbconn.getData(self.textbox,self.codeEntry.get()))

        self.valueCB=ctk.CTkCheckBox(self,text="Graphics",command=self.an.DrawGraphics)

        self.cryptoCsv=ctk.CTkCheckBox(self,text="Save cryptos to CSV",command=lambda:self.opt.getCryptos())

        self.indexMenuByCountry=ctk.CTkOptionMenu(self,values=['Select','Finland','Germany','Japan','Poland'],command=lambda x:self.sc.scrapeIndex(x,self.textbox))
       
        self.yfOptions=ctk.CTkOptionMenu(self,values=['Select','Recommendations','Major Holders','Mutual fund hold.','Dividends','Multiple tickers','General'],command=lambda x: self.ytf.getOption(x,self.codeEntry.get(),self.textbox,self.valueCB,self.tickerBtn,self.codeEntry,self.getMultipleBtn))
        #self.historyCB=ctk.CTkCheckBox(self,text="Get history",command=lambda:self.ms.historicalData(self.codeEntry.get(),self.textbox,self.fromDate.get(),self.toDate.get()))
        self.historyOptions=ctk.CTkSegmentedButton(self,values=['Get history','History graph','Intraday'],command=lambda sel:self.ytf.yfHistory(sel,self.fromDate.get(),self.toDate.get(),self.codeEntry.get(),self.textbox))
        self.stockOptions=ctk.CTkSegmentedButton(self, values=['Earnings','News','Dividends','Earning call'],command=self.getStockOption)
        self.cryptoOptions=ctk.CTkSegmentedButton(self,values=['Save cryptos to CSV'],command=self.getStockOption)
        self.quantity=ctk.CTkComboBox(self,values=['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '4h', '1d', '5d', '1wk', '1mo', '3mo'],command=self.ytf.getComboBoxValue,width=70)
        self.quantity.set('1m')
        self.pressTab=ctk.CTkLabel(self,text="Press tab",fg_color="red")
        self.fromDate=ctk.CTkEntry(self,placeholder_text="FROM (YYYY-MM-DD)")
        self.toDate=ctk.CTkEntry(self,placeholder_text="TO (YYYY-MM-DD)")
        #lambda x: voidaan lähettää option menun valinnan lisäksi muita parametreja.
        self.indexMenu=ctk.CTkOptionMenu(self,values=['Select','NASDAQ 100','DAX'],command=lambda x:self.sc.stockIndex(x,self.textbox))
        self.tickerBtn=ctk.CTkButton(self,text="Set",command=self.ytf.setTickerToList)
        self.getMultipleBtn=ctk.CTkButton(self,text="Get multiple",command=lambda:self.ytf.getMultipleTickers)
        
        
   

    def getStockOption(self,val):
        if val=="News":
            self.news.companyNews(self.codeEntry.get(),self.textbox)
        elif val=='Dividends':
            self.ms.getDividends(self.codeEntry.get(),self.textbox)
        elif val=="Earning call":
            self.an.earningCalls(self.codeEntry.get(),self.textbox)
        elif val=="Save cryptos to CSV":
            self.opt.getCryptos()


 #luetaan kaikki data tickers.txt tiedostosta ja lisätään data tickerlist listaan.
    def setAcText(self):
         self.tickerFile=open("tickers.txt","r")
         self.tickerData=self.tickerFile.read()
         self.tickerList=self.tickerData.split("\n")
         self.tickerFile.close()
         self.cryptoFile=open("cryptos.txt","r")
         self.cryptoData=self.cryptoFile.read()
         self.cryptoList=self.cryptoData.split("\n")
         self.cryptoFile.close()
        

    def showDialog(self):
            
            self.dialog = ctk.CTkInputDialog(text="Enter the number of ETFs to display or an individual ETF ID to view its details:", title="Question")
            response=self.dialog.get_input()
            #isdigit tarkistaa, sisältääkö merkkijono numeroita
            if response.isdigit():
                self.sc.listEtfs(self.textbox,response)
            
            if response.isdigit()==False:
                self.sc.getEtfData(self.textbox,response)
            
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
        self.codeEntry.delete(0,"end")

    #käyttäjän antama rss-syötteen osoite
    def showInput(self):
        if self.wUrl.get()=="on":

            self.urlInput=ctk.CTkEntry(self)
            self.urlInput.grid(row=4,column=7,sticky="EW")
            #focuosut eventin ja metodin sitominen toisiinsa.
            self.urlInput.bind('<FocusOut>',self.inputFocusOut)
       
        else:
            self.urlInput.grid_forget()
          
    #event parametri on tapahtuma eli se kun kursori poistuu entry kentästä.
    def inputFocusOut(self,event):
        
        self.url=self.urlInput.get()
        self.fetchRssData()
    
        
    def optionmenu_callback(self,choice):
       
        self.choice=choice
        print(self.choice)
        #tarkistus, onko valittu arvo words-listassa
        if self.choice in self.words:
            self.codeEntry.grid(row=5, column=1, sticky="ew",pady=10)
            if self.choice=="Stocks":
                self.us.createStock(self.stockOptions,self.useAC)
              
            elif self.choice=="Crypto":
                self.us.createCrypto(self.cryptoOptions,self.useAC)
                
            elif self.choice=="Commodities":
                self.us.createCommodity(self.comMenu,self.codeEntry,self.getBtn)

            elif self.choice=="History":
                self.us.historyComponents(self.codeEntry,self.historyOptions,self.fromDate,self.toDate,self.quantity,self.getBtn,self.useAC,self.pressTab)
               
            elif self.choice=="Finance Dictionary":
                self.us.createDictionary(self.codeEntry,self.getBtn,self.getTermBtn,self.financeDict)
           
            elif choice=="Listen podcasts":
                self.us.createPodcast(self.codeEntry,self.getBtn,self.podcasts,self.podstop)
             
            elif choice=='Index history':
                 self.indexMenu.grid(row=5,column=1,sticky="W")
                 self.codeEntry.grid_forget()
                 self.getBtn.grid_forget()
                 
            elif choice=='Stock index by country':
                self.us.createIndex(self.indexMenuByCountry,self.codeEntry,self.getBtn)
            
            elif choice=="Yahoo Finance":
                self.us.createYahooFinance(self.getBtn,self.useAC,self.yfOptions,self.codeEntry)

         #piilottaa dict oliossa olevat gridit              
        else:
            self.grids={'grid':self.codeEntry.grid_forget(),'grid':self.earnings.grid_forget(),'grid':self.comMenu.grid_forget(),'grid':self.newsAboutComp.grid_forget()
                        ,'grid':self.podcasts.grid_forget(),'grid':self.podstop.grid_forget()
                        ,'grid':self.financeDict.grid_forget(),'grid':self.getTermBtn.grid_forget(),'grid':self.indexMenuByCountry.grid_forget()
                        ,'grid':self.useAC.grid_forget(),'grid':self.yfOptions.grid_forget(),'grid':self.fromDate.grid_forget(),
                         'grid':self.toDate.grid_forget(),'grid':self.cryptoOptions.grid_forget(),'grid':self.historyOptions.grid_forget(),'grid':self.quantity.grid_forget()
                         ,'grid':self.stockOptions.grid_forget()}
                        
            self.grids['grid']
            
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
    
    def showAc(self):
        #jos tiedostot on olemassa
        if os.path.exists("tickers.txt") and os.path.exists("cryptos.txt"):
            self.setAcText()
        #jos tiedostoja ei ole olemassa
        if not os.path.exists("tickers.txt") and not os.path.exists("cryptos.txt"):
            self.gd.connect()
            self.setAcText()
        
        if self.acVar.get()=="on":
            self.codeEntry.grid_forget()
            self.codeentryAc=AutocompleteEntry(self,completevalues=self.tickerList)
            self.codeentryAc.grid(row=5, column=1, sticky="ew")
        
        if self.acVar.get()=="off":
            self.codeentryAc.grid_forget()
            self.codeEntry.grid(row=5, column=1, sticky="ew")
            

    def selectMethods(self):
        
        if self.choice=="Stocks":   
            self.an.fetchData(self.textbox,self.codeEntry.get(),self.valueCB)
        elif self.choice=="Crypto":
            self.an.fetchCryptoData(self.textbox,self.valueCB,self.codeEntry.get())
    
    
    def voice_stocks(self):
         self.codeEntry.grid(row=5, column=1,columnspan=1, padx=20,pady=20, sticky="ew")
         self.earnings.grid(row=6,column=1,sticky="W")
         self.newsAboutComp.grid(row=6,column=1,sticky="E")
    
if __name__ == "__main__":

    app = App()
    # Runs the app
    app.mainloop()    