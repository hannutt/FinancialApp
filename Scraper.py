from bs4 import BeautifulSoup
import requests


class Scrape():
      def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

      def stockIndex(self,indexname,tbox):
        indexs={'NASDAQ 100':'https://www.investing.com/indices/nq-100-historical-data','DAX':'https://www.investing.com/indices/germany-30-historical-data'}
        
        response = requests.get(indexs[indexname])
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find(class_='freeze-column-w-1 w-full overflow-x-auto text-xs leading-4')
        rows=table.find_all('tr')
        for r in rows:

            res=r.text
            tbox.insert("end",res)
            #lisätään rivinvaihto, että csv-tiedostoon voidaan tallentaa data muodossa rivi + rivinvaihto
            tbox.insert("end","\n")

      def scrapeIndex(self,indexname,tbox):
 
          indexs={"Finland":{'url':'https://www.investing.com/indices/world-indices',"id":"16"},
                  "Germany":{'url':'https://www.investing.com/indices/world-indices',"id":"4"}}
          #print(indexs[indexname]['url'])
          
          response = requests.get(indexs[indexname]['url'])
          soup = BeautifulSoup(response.text, 'html.parser')
          table = soup.find(id='indice_table_'+indexs[indexname]['id'])
          rows=table.find_all('tr')
          for r in rows:

            res=r.text
            tbox.insert("end",res)
            tbox.insert("end","\n")
        
          
     