import requests
from bs4 import BeautifulSoup
import pandas as pd
import json;
import pprint;

'''
page= requests.get("https://en.wikipedia.org/wiki/List_of_Golden_Globe_winners")
soup= BeautifulSoup(page.text, "html.parser")
'''

with open("testJ.json", encoding='UTF-8') as file:
    jsonTest = json.load(file)
    file.close()

nfrom=0
nsize=5575
nomilink_ = f"https://www.goldenglobes.com/__es/elasticsearch_index_pantheon_live_nominations_s8hj4qdd/_search?source={{\"query\":{{\"bool\":{{\"must\":[false,{{\"match\":{{\"status\":true}}}},{{\"match\":{{\"category_type\":\"3\"}}}}]}}}},\"sort\":[{{\"year\":\"desc\"}}],\"_source\":[\"url\",\"winner\",\"year\",\"category_name\",\"category_type\",\"name\",\"person_nominations\",\"person_wins\",\"film_nominations\",\"film_wins\"]}}&size={nsize}&from={nfrom}&source_content_type=application/json"
nomijson_ = requests.get(nomilink_).json()
pprint.pprint(len(nomijson_["hits"]["hits"]))

'''
with open("page-data.json", encoding='UTF-8') as file:
    pagedata = json.load(file)
    file.close()

print("----")
pprint.pprint(pagedata['result']["data"])
pprint.pprint(pagedata['result'].keys())
'''
#documentliste = jsonTest["hits"]["hits"]
documentliste = nomijson_["hits"]["hits"]

#Nom de la personne, nominé ou gagnant dans la catégorie , dans quel film/série
def lecteurPersonne(document):
    k=0
    for i in range(len(document)):
        entree = document[i]["_source"]

        y = entree["year"][0]
        ctg = entree["category_name"][0]
        print(entree["name"][0])
        if entree["winner"][0]:
            print(f"Gagnant.e {y}")
        else:
            print(f"Nominee.e {y}")
        print(f"Catégorie: {ctg}")

        if not(ctg== "Cecil B. deMille Award" or ctg == "Carol Burnett Award" ):
            nomipath= entree["url"][0]
            nomilink = "https://www.goldenglobes.com/page-data" + nomipath + "/page-data.json"
            nomijson = requests.get(nomilink).json()
            #probleme nexiste pas si la categorie cest "Carol Burnett Award"
            media = nomijson["result"]["data"]["nodeNomination"]["relationships"]['field_film_tv_show']["title"]
            print(f"Pour sa performance dans: {media}")
        k=k+1
        print(k)
        print("---")

def lecteurPersonnePD(document):
    k=0
    personlist, winnerlist, catlist, medialist, yearlist = [], [], [], [], []
    for i in range(len(document)):
        entree = document[i]["_source"]

        y = entree["year"][0]
        ctg = entree["category_name"][0]


        #print(entree["name"][0])
        personlist.append(entree["name"][0])

        if entree["winner"][0]:
            #print(f"Gagnant.e {y}")
            winnerlist.append(1)
        else:
            #print(f"Nominee.e {y}")
            winnerlist.append(0)
        yearlist.append(y)
        #print(f"Catégorie: {ctg}")
        catlist.append(ctg)

        if not(ctg== "Cecil B. deMille Award" or ctg == "Carol Burnett Award" ):
            nomipath= entree["url"][0]
            nomilink = "https://www.goldenglobes.com/page-data" + nomipath + "/page-data.json"
            nomijson = requests.get(nomilink).json()
            #probleme nexiste pas si la categorie cest "Carol Burnett Award"
            media = nomijson["result"]["data"]["nodeNomination"]["relationships"]['field_film_tv_show']["title"]
            #print(f"Pour sa performance dans: {media}")
            medialist.append(media)
        else :
            medialist.append(None)
        k=k+1
        print(k)
    d = {'Person': personlist, 'Winner': winnerlist, 'Year': yearlist, 'Category': catlist, 'Media': medialist}
    #d = {'Person': personlist, 'Winner': winnerlist, 'Year': yearlist, 'Category': catlist}
    return pd.DataFrame(data=d)

#5575
dataframe = lecteurPersonnePD(documentliste)

