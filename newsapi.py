import json
import os
import requests


newsapk=os.environ.get('newsapk')
class NewsAPI():
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

    def cryptoNews(self,keyword,tbox):
        pass
        # https://newsapi.org/v2/everything?q=Apple&from=2025-02-05&sortBy=popularity&apiKey=API_KEY
       
    
    def companyNews(self,keyword,tbox):
        api_url=f'https://newsapi.org/v2/everything?q={keyword}&sortBy=relevancy&us&apiKey={newsapk}&pageSize=5'
        response = requests.get(api_url, headers={'X-Api-Key': newsapk})
        data=response.json()
       
        tbox.insert("end",data)
       
        
       
