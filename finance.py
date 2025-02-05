# Import customtkinter module
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
from PIL import Image
from databaseConnection import DatabaseConnection
#Api-avain on talletettu env-muuttujaan, tässä haetaan sen sisältämä merkkijono
apk=os.environ.get('apk')
#Asettaa sovelluksen ulkoasutilan System määrittää ulkoasun saman kuin järjestelmän. dark on tumma teema
ctk.set_appearance_mode("Dark")        
 
# Sets the color of the widgets
# Supported themes: green, dark-blue, blue
ctk.set_default_color_theme("green")    
 
# Create App class
class App(ctk.CTk,tk.Menu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.words=['Crypto','Stocks','Precious metals']
        self.title("Finance App")
        self.menubar=tk.Menu(self)
        self.config(menu=self.menubar)
        self.opt=Options()
        self.news=NewsAPI()
        self.dbconn=DatabaseConnection()
    
      
        #App luokan textbox voidaan lähettää  options luokalle parametria command=lambda:o.currencyWidgets(self.textbox))
        self.menubar.add_command(label='Cur. convert',command=lambda:self.opt.currencyWidgets())
        self.menubar.add_command(label='Exchange rate',command=lambda:self.opt.createExcWidgets())
        self.menubar.add_command(label='Business news',command=lambda:self.news.businessNews(self.textbox))
       
        
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
        self.optMenu = ctk.CTkOptionMenu(self,
                                        values=['Select',"Crypto","Stocks",'Commodities','Precious metals','Business news'],command=self.optionmenu_callback)
        self.optMenu.grid(row=3, column=1,padx=5, pady=10,columnspan=1, sticky="ew")

        self.codeEntry = ctk.CTkEntry(self,placeholder_text="crypto/stock code",textvariable=self.inputField,validate="focusout", validatecommand=self.showInput)
        self.earningsSV=ctk.StringVar()
        self.earnings=ctk.CTkCheckBox(self,text="Show earnings?", onvalue="on", offvalue="off", variable=self.earningsSV)
        self.newsAboutComp=ctk.CTkCheckBox(self,text="News?",command=lambda:self.news.companyNews(self.codeEntry.get()))
        self.getBtn=ctk.CTkButton(self,text="Get data",command=self.selectMethods,width=5)
        self.getBtn.grid(row=7,column=1,columnspan=3,sticky="ew",padx=10,pady=10)
        self.textbox=ctk.CTkTextbox(self,width=200,corner_radius=5,height=105)
        self.textbox.grid(row=9,column=1,sticky="ew",columnspan=1)
        #lambdan avulla voidaan antaa metodille parametri, ilman lambdaa metodi jossa on () merkit
        #suoritetaan heti
        self.rssSV=ctk.StringVar()
        self.klUrl=ctk.StringVar(value="https://feeds.kauppalehti.fi/rss/main")
        self.klRss=ctk.CTkCheckBox(self,text="Kauppalehti RSS",command=lambda:self.selRssSource(self.klUrl.get()),onvalue="on",offvalue="off")
        self.klRss.grid(row=3,column=7,columnspan=3)
        self.clearBtn=ctk.CTkButton(self,text="Clear",command=self.clearTextBox)
        self.clearBtn.grid(row=10,column=1,pady=(10,10),sticky="w")
        self.saveBtn=ctk.CTkButton(self,text='Save',command=lambda:self.dbconn.DBsave(self.textbox.get('1.0',END)))
        self.saveBtn.grid(row=11,column=1,sticky="w")
        ''''
        self.urlInput=ctk.CTkEntry(self)
        self.urlInput.grid(row=6,column=8,columnspan=3)
        '''
        self.invUrl=ctk.StringVar(value='https://fi.investing.com/rss/news_25.rss')
        self.invRss=ctk.CTkCheckBox(self,text="Investing RSS",command=lambda:self.selRssSource(self.invUrl.get()),variable=self.rssSV,onvalue="on",offvalue="off")
        self.invRss.grid(row=5,column=7,columnspan=2)

        self.wUrl=ctk.StringVar()
        self.writeUrl=ctk.CTkCheckBox(self,text="Own RSS url?",variable=self.wUrl,onvalue="on",offvalue="off",command=self.showInput)
        #pady(10,0) tarkoittaa, että ylös lisätään 10 pikseliä tyhjää tilaa ja alas 0 pikseliä
        self.writeUrl.grid(row=6,column=6,columnspan=3,pady=(10,0))

        self.valueCB=ctk.CTkCheckBox(self,text="Graphics",command=self.DrawGraphics)
    
  

    def clearTextBox(self):
        self.textbox.delete("0.0","end")
        self.klRss.deselect()
        self.invRss.deselect()
        self.writeUrl.deselect()

    def showInput(self):
        if self.wUrl.get()=="on":

            self.urlInput=ctk.CTkEntry(self)
            self.urlInput.grid(row=7,column=8,columnspan=3)
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
        #tarkistus, onko valittu arvo words-listassa
        if self.choice in self.words:
            self.codeEntry.grid(row=5, column=1,columnspan=1, padx=20,pady=20, sticky="ew")
            if self.choice=="Stocks":
                self.earnings.grid(row=6,column=1,sticky="W")
                self.newsAboutComp.grid(row=6,column=1,sticky="E")
            if self.choice=="Precious metals":
                self.createMetals()
            
        elif self.choice=="Commodities":
            self.createCommodity()    
        else:
            #piilottaa gridit
            self.codeEntry.grid_forget()
            self.earnings.grid_forget()
            self.preciousMenu.grid_forget()
            
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
        print(url)
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
        if self.choice=="Stocks" and self.earningsSV.get()=="on":
            self.fetchData()
            self.fetchEarnings()
        elif self.choice=="Stocks":
            self.fetchData()
        elif self.choice=="Crypto":
            self.fetchCryptoData()
        

    def fetchData(self):
            #self.codeEntry.get() = tekstikentän sisältö
            api_url = 'https://api.api-ninjas.com/v1/stockprice?ticker={}'.format(self.codeEntry.get())
            response = requests.get(api_url, headers={'X-Api-Key': apk})
            if response.status_code == requests.codes.ok:
            #json-vastaus muunnetaan python dictionary objektiksi.
                respDict=json.loads(response.text)
                utime=respDict.get("updated")
                utimeInt=int(utime)
                datetimeStr=datetime.fromtimestamp(utimeInt).strftime('%d-%m-%Y %H:%M:%S')
                self.price = respDict.get("price")
                self.name=respDict.get("name")
                self.currency=respDict.get("currency")
                self.textbox.insert("end","UPDATED:")
                self.textbox.insert("end",datetimeStr+"\n" )
                self.textbox.insert("end",self.name+"\n")
                self.textbox.insert("end",self.price,"\n")
                self.textbox.insert("end",self.currency)
                '''
                for r in respDict:
                
                    self.textbox.insert('end',respDict[r])
                    self.textbox.insert('end',"\n")
                '''
          
                self.valueCB.grid(row=11,column=1,columnspan=3)
                self.valueCB.configure(text=self.name+" Graphics")
          
    
    def fetchEarnings(self):

        api_url='https://api.api-ninjas.com/v1/earningscalendar?ticker={}'.format(self.codeEntry.get())
        response = requests.get(api_url, headers={'X-Api-Key': apk})
        if response.status_code == requests.codes.ok:
            self.textbox.insert("end",response.text)

    def createMetals(self):
         self.preciousMenu = ctk.CTkOptionMenu(self,
                                        values=["Gold"],command=self.gold_callback)
         self.preciousMenu.grid(row=4, column=1,padx=10, pady=10,columnspan=1, sticky="ew")
         self.codeEntry.grid_forget()

    
    def createCommodity(self):
         self.comMenu = ctk.CTkOptionMenu(self,
                                        values=["Oat","Platinum",'Gold','Palladium'],command=self.commodity_callback)
         self.comMenu.grid(row=4, column=1,padx=10, pady=10,columnspan=1, sticky="ew")
   
    def fetchCryptoData(self):
        api_url ='https://api.api-ninjas.com/v1/cryptoprice?symbol={}'.format(self.codeEntry.get())
        response = requests.get(api_url, headers={'X-Api-Key': apk})
        if response.status_code == requests.codes.ok:

            #json-vastaus muunnetaan python dictionary objektiksi.
            respDict=json.loads(response.text)
            #unix timestampin muunto luettavaksi päivämääräksi
            utime=respDict.get("timestamp")
            utimeInt=int(utime)
            datetimesSter=datetime.fromtimestamp(utimeInt).strftime('%d-%m-%Y %H:%M:%S')
            self.textbox.insert("end",datetimesSter)
            self.textbox.insert("end","\n")
            for r in respDict:
                
                self.textbox.insert('end',respDict[r])
                self.textbox.insert('end',"\n")
            #talletetaan muuttujaan sanakirjan price avaimen arvo
            self.price = respDict.get("price")
            self.name=respDict.get("symbol")
            
            self.valueCB.grid(row=11,column=1)
            self.valueCB.configure(text=self.name+" Graphics")
        else:
            print("Error:", response.status_code, response.text)
    
    def DrawGraphics(self):
        plt.bar(self.name,self.price,width=0.5)
        plt.show()
 
if __name__ == "__main__":

    app = App()
    # Runs the app
    app.mainloop()    