"""
Script che è utilizzato per creare l'intero indice utilizzando whoosh.
"""
import os
from os import listdir
from os.path import isfile, join

import re

from whoosh.analysis import LanguageAnalyzer
from whoosh.fields import *
from whoosh.index import create_in

schema = Schema(title=TEXT(analyzer=LanguageAnalyzer("it"), stored=True), url=ID(stored=True),
                urlimage=TEXT(stored=True), date=DATETIME(stored=True),
                content=TEXT(analyzer=LanguageAnalyzer("it"), stored=True), categories=TEXT(stored=True),
                site=TEXT(stored=True))
if not os.path.exists("indexdir"):
    os.mkdir("indexdir/")
ix = create_in("indexdir", schema)

# si crea una lista di file prendendoli dalla cartella corpus
filelist = [f for f in listdir("corpus") if isfile(join("corpus", f))]

writer = ix.writer()

# per ogni file ottenuto, si prendono le sue parti e si aggiungono nell'indice
for i in filelist:
    f = open("corpus/" + i, "r", encoding='utf-8')
    furl = f.readline()
    furl = furl.rstrip()

    p = re.compile(r"www\.[^\/]+")
    match = p.search(furl)
    fsite = match.group(0)[4:]  # così si prende il sito a cui appartiene l'articolo, senza il "www." all'inizio

    ftitle = f.readline()
    ftitle = ftitle.rstrip()

    fkeyword = f.readline()
    fkeyword = fkeyword.rstrip()

    furlimage = f.readline()
    furlimage = furlimage.rstrip()

    f.readline()
    date = f.readline()
    date = date.rstrip()
    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    fcontent = f.read()

    writer.add_document(title=ftitle, url=furl, urlimage=furlimage, date=date_obj, content=fcontent,
                        categories=fkeyword, site=fsite)
    f.close()

writer.commit()
