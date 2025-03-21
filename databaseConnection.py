
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import pandas as pd
import customtkinter as ctk
from openai import OpenAI

gptAPk=os.environ.get('oakey')


user = os.environ.get('mongoUser')
psw=os.environ.get("mongoPsw")
dbName=os.environ.get('dbName')
colName=os.environ.get("colName")
fdCol=os.environ.get('fdName')

class DatabaseConnection():
     def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        
    
    #data-parametri sisältää textboxin arvot
     def DBsave(self,data):
        #muunto dict-tyypiksi
        dataDict={"data":data}
        print(dataDict)   
        self.uri="mongodb+srv://{}:{}@cluster0.gfnzlpq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0".format(user,psw)
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        self.collection = self.client[dbName][colName]
        self.collection.insert_one(dataDict)
        self.client.close()
      
     def getFinanceTerm(self,term):
         self.term=term
              
      
     def getData(self,tbox,codeinput):
          if codeinput !='':
              self.askGpt(codeinput,tbox)
          else:
              
            self.uri="mongodb+srv://{}:{}@cluster0.gfnzlpq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0".format(user,psw)
            self.client = MongoClient(self.uri, server_api=ServerApi('1'))
            self.collection = self.client[dbName][fdCol]
          #haku siten, että self.term muuttuja vastaa kokoelman key kenttää, tuloksesta poistetaan _id ja key kentät,
          #vain txt kenttä näytetään
            self.doc=self.collection.find({"key":self.term},{"_id":0,"key":0})
            for d in self.doc:
                tbox.insert("end",d)

     def getFontSize(self,fsize):
         
         self.fsize=fsize
         print(self.fsize)
         
   
     def CsvSave(self,financedata):
         financeDataList=[]
         #parametrina saatu textboksin sisältö talletetaan listaan, 
         financeDataList.append(financedata)
         
         #dict objekti, data avaimen arvo on financedatalist
         dataDict={'data':financeDataList}
         df=pd.DataFrame(dataDict)
         filename = ctk.filedialog.asksaveasfile(filetypes=[('csv', '*.csv')])
         df.to_csv(filename,index=False,header=False,sep="\t")
    
     def askGpt(self,codeinput,tbox):
         from openai import OpenAI
         client = OpenAI(api_key=gptAPk)
         #tällä rajoitetaan api vastamaan vain sijoittamiseen liittyviin kysymyksiin.
         system_message="If the user's question is not related to investing, dismiss it."
         completion = client.chat.completions.create(
         model="gpt-4o",
         messages=[
             
            {
                "role": "user",
                "content": codeinput,
                
            },
            {
                "role":"system",
                "content":system_message,
            }
        ]
    
)        
         answer=str(completion.choices[0].message.content)
         tbox.insert("end",answer)

        
         
        
     
         
         

        
        
         
      
