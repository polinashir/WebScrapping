import requests
from bs4 import BeautifulSoup
import pandas as pd
import json;
import pprint;
from sqlalchemy import create_engine

def prettyprinter(list):
    for e in list:
        #print(e.prettify())
        pprint.pprint(e)
        print("---")

with open("movies.json", encoding='UTF-8') as file:
    jsonTest = json.load(file)
    file.close()

nfrom=0
nsize=1500
nomilink_=f"https://www.goldenglobes.com/__es/elasticsearch_index_pantheon_live_nominations_s8hj4qdd/_search?source={{\"query\":{{\"bool\":{{\"must\":[false,{{\"match\":{{\"status\":true}}}},{{\"match\":{{\"category_type\":\"1\"}}}}]}}}},\"sort\":[{{\"year\":\"desc\"}}],\"_source\":[\"url\",\"winner\",\"year\",\"category_name\",\"category_type\",\"name\",\"person_nominations\",\"person_wins\",\"film_nominations\",\"film_wins\"]}}&size={nsize}&from={nfrom}&source_content_type=application/json"

nomijson_ = requests.get(nomilink_).json()
pprint.pprint(len(nomijson_["hits"]["hits"]))

documentliste = nomijson_["hits"]["hits"]
entree = documentliste[1]["_source"]

print(entree["winner"])

nomipath = entree["url"][0]
nomilink = "https://www.goldenglobes.com/page-data" + nomipath + "/page-data.json"
nomijson = requests.get(nomilink).json()

def lecteurMovies(document):
    k = 0
    for i in range(len(document)):
        
        # probleme nexiste pas si la categorie cest "Carol Burnett Award"
        name = nomijson["result"]["data"]["nodeNomination"]["relationships"]["field_film_tv_show"]["title"]
        print(f"Name: {name}")
        y = entree["year"][0]
        ctg = entree["category_name"][0]
        if entree["winner"][0]:
            print(f"Gagnant.e {y}")
        else:
            print(f"Nominee.e {y}")
        print(f"Catégorie: {ctg}")

        k = k + 1
        print(k)
        print("---")



def lecteurMoviesPD(document):
    k=0
    movielist, winnerlist, catlist, medialist, yearlist = [],[],[],[],[]
    for i in range(len(document)):
        entree = document[i]["_source"]

        
        # probleme nexiste pas si la categorie cest "Carol Burnett Award"
        name = nomijson["result"]["data"]["nodeNomination"]["relationships"]["field_film_tv_show"]["title"]

        y = entree["year"][0]
        ctg = entree["category_name"][0]
        

        #print(entree["name"][0])
        movielist.append(name)

        if entree["winner"][0]:
            #print(f"Gagnant.e {y}")
            winnerlist.append(1)
        else:
            #print(f"Nominee.e {y}")
            winnerlist.append(0)
        yearlist.append(y)
        #print(f"Catégorie: {ctg}")
        catlist.append(ctg)

        k=k+1
        print(k)
        print("---")
    d = {'Name': movielist, 'Winner': winnerlist, 'Year': yearlist, 'Category': catlist}
    return pd.DataFrame(data=d)

movies = lecteurMoviesPD(documentliste)

engine = create_engine('sqlite://', echo=False)
movies.to_sql('Movies', con=engine)
engine.execute("SELECT * FROM Movies").fetchall()
