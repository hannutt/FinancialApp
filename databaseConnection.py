
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
user = os.environ.get('mongoUser')
psw=os.environ.get("mongoPsw")
dbName=os.environ.get('dbName')
colName=os.environ.get("colName")
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
        
        
         
      
