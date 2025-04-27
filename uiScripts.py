import customtkinter as ctk
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteEntry
from tkcalendar import DateEntry
class UiScripts():
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def historyComponents(self,codeEntry,historyOptions,fromDate,toDate,quantity,getBtn):
           self.fromDate=fromDate
           self.toDate=toDate
           codeEntry.grid(row=5, column=1,sticky="W")
           historyOptions.grid(row=7,column=1,sticky="W",pady=10)
           #fromDate=ctk.CTkEntry(self,placeholder_text="FROM (YYYY-MM-DD)")
           self.fromDate.grid(row=6,column=1,sticky="W",pady=10)
           self.fromDate.bind("<Button>",self.calendarMethod)
           #toDate=ctk.CTkEntry(self,placeholder_text="TO (YYYY-MM-DD)")
           self.toDate.bind("<Button>",self.setCalDateToEnd)
           self.toDate.grid(row=6,column=1,sticky="E")
           quantity.grid(row=7,column=1,sticky="E",padx=5)
           getBtn.grid_forget()
    
    def createCommodity(self,commenu,codeEntry,getBtn):
         codeEntry.grid_forget()
         getBtn.grid_forget()
         commenu.grid(row=4, column=1,padx=10, pady=10, sticky="w")
    
    def createDictionary(self,codeEntry,getBtn,getTermBtn,financeDict):
         codeEntry.grid(row=6,column=1,sticky="W",pady=5)
         getBtn.grid_forget()
         getTermBtn.grid(row=5,column=1,sticky="E")
         financeDict.grid(row=5,column=1,sticky="W")
    def calendarMethod(self,event):
        self.cal = DateEntry(date_pattern="yyyy-mm-dd")
        self.cal.grid(row=8,column=1,sticky="W",pady=10)
        #näytää press tab tekstin, kun aloituskenttä on täytetty
        
        self.cal.bind("<Tab>",self.setCalDate) 
        
    
    def setCalDate(self,event):
        
        self.fromDate.delete(0,END)
        self.selected_date = self.cal.get()
        self.fromDate.insert(0,self.selected_date)
        self.cal.grid_forget()
        self.pressTab.grid(row=8,column=1)
        
    def setCalDateToEnd(self,event):
         #self.pressTab.grid_forget()
         self.cal = DateEntry(date_pattern="yyyy-mm-dd")
         self.cal.grid(row=8,column=1,sticky="W",pady=10)
         self.cal.bind("<Tab>",self.setCalDateToEndField)
            
    def setCalDateToEndField(self,event):
        self.toDate.delete(0,END)
        self.selected_date2 = self.cal.get()
        self.toDate.insert(0,self.selected_date2)
        self.cal.grid_forget()