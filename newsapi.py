import os
import requests


newsapk=os.environ.get('newsapk')
class NewsAPI():
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

    def businessNews(self,tbox):
        api_url=f'https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapk}'
        response = requests.get(api_url, headers={'X-Api-Key': newsapk})
        tbox.insert("end",response.json())
        print(response.json())
    
    def companyNews(self,company):
        
        print(company)
        
