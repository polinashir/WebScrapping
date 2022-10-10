# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 15:01:42 2022

@author: polin
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from jsontest import JsonTest
import time

response = requests.get("https://en.wikipedia.org/wiki/List_of_Golden_Globe_winners")
#print(response.text)
soup=BeautifulSoup(response.text, "lxml")
titles=soup.findAll('th')
indiatable=soup.find('table',{'class':"wikitable"})
#print(titles)
info=soup.findAll('td')
info2=soup.findAll('a')
table_contentsAll=soup.findAll(attrs={'class':'wikitable'})
df_Film1=pd.read_html(str(table_contentsAll[0]))
df_Film1=pd.DataFrame(df_Film1[0])
df_Film2=pd.read_html(str(table_contentsAll[1]))
df_Film2=pd.DataFrame(df_Film2[0])
df_Film3=pd.read_html(str(table_contentsAll[2]))
df_Film3=pd.DataFrame(df_Film3[0])                    

df_Series=pd.read_html(str(table_contentsAll[3]))
df_Series=pd.DataFrame(df_Series[0])



with open('C:\\Users\\polin\\Documents\\IMT\\Cours actuels\\Data\\web_scrapping\\file_anim.json', encoding='UTF-8') as json_file:
    data = json.load(json_file)
    json_file.close()
    
    
documentliste=data["hits"]["hits"]
print(documentliste[0]["_source"])


def lecteurMeilleureDrama(doc):
    for i in range(len(doc)):
        entree=doc[i]["_source"]
        y=entree["year"][0]
        print(y)
        ctg=entree["category_name"][0]
        print(ctg)
        url=entree["url"][0]
        media="https://www.goldenglobes.com/page-data"+url+"/page-data.json"
        resp = requests.get(media)
        small_soup=BeautifulSoup(resp.text, "lxml")
        print()
        
        if entree["winner"]==False:
            print(f"Nominee.e {y}")
        else:
            print(f"Gagnant.e {y}")


lecteurMeilleureDrama(documentliste)















