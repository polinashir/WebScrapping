import pandas as pd
import requests
import json
import pprint
outputdir = "jsonPersons"

with open(outputdir+"/"+"200 - 400.json", encoding='UTF-8') as file:
    jsonTest = json.load(file)
    file.close()

#url du json nomination
nomipath=jsonTest["hits"]["hits"][0]["_source"]["url"][0]


nomilink = "https://www.goldenglobes.com/page-data" + nomipath + "/page-data.json"

print(nomipath)

#extrait un fichier .json correspondants aux personnes
def extractPeople(nfrom,samplesize):
    nomilink_ = f"https://www.goldenglobes.com/__es/elasticsearch_index_pantheon_live_nominations_s8hj4qdd/_search?source={{\"query\":{{\"bool\":{{\"must\":[false,{{\"match\":{{\"status\":true}}}},{{\"match\":{{\"category_type\":\"3\"}}}}]}}}},\"sort\":[{{\"year\":\"desc\"}}],\"_source\":[\"url\",\"winner\",\"year\",\"category_name\",\"category_type\",\"name\",\"person_nominations\",\"person_wins\",\"film_nominations\",\"film_wins\"]}}&size={samplesize}&from={nfrom}&source_content_type=application/json"
    nomijson_ = requests.get(nomilink_).json()
    filename = str(nfrom)+" - "+str(nfrom+samplesize)+".json"

    with open(outputdir + '/'+filename, 'w') as json_file:
        json.dump(nomijson_, json_file)
        json_file.close()
    return 0

#Extrait les json mentionnés dans un fichier filename
def getNomiLink(filename):
    path = outputdir+"/"+filename

    return 0


#for i in range (33):
#    extractPeople(200*i,200)

'''
#5826 entrées dans Persons
#5576
'''