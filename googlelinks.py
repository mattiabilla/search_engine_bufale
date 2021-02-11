#
import json

ass = {
    'open.online': 'linkopen.txt',
    'butac.it': 'linkbutac.txt',
    'bufale.net': 'linkbufale.txt'
}

fdata = open('query_0.json', 'r', encoding='utf-8')
fopen = open('linkopen.txt', 'r', encoding='utf-8')
fbutac = open('linkbutac.txt', 'r', encoding='utf-8')
fbufale = open('linkbufale.txt', 'r', encoding='utf-8')

dopen = fopen.read()
dbutac = fbutac.read()
dbufale = fbufale.read()

data = json.load(fdata)
for i in data['organic_results']:
    tmp = i['link'][:len(i['link'])-1]
    if tmp in dopen or tmp in dbutac or tmp in dbufale:
        print(i['link'])
