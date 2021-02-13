# tool per leggere i risultati delle ricerche google da un file .json, ottenuto con l'utilizzo del sito
# scaleserp.com

import json


file = 'query_9'
output = 'google_' + file + '.txt'
fdata = open(file+'.json', 'r', encoding='utf-8')
fopen = open('linkopen.txt', 'r', encoding='utf-8')
fbutac = open('linkbutac.txt', 'r', encoding='utf-8')
fbufale = open('linkbufale.txt', 'r', encoding='utf-8')
out = open(output, 'w', encoding='utf-8')

dopen = fopen.read()
dbutac = fbutac.read()
dbufale = fbufale.read()

data = json.load(fdata)
for i in data['organic_results']:
    tmp = i['link'][:len(i['link'])-1]
    if tmp in dopen or tmp in dbutac or tmp in dbufale:
        out.write(i['link'] + '\n')
