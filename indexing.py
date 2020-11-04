# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 21:05:03 2020

@author: Mattia
"""

from whoosh.index import create_in
from whoosh.fields import *

schema = Schema(title=TEXT(stored=True), url=ID(stored=True), content=TEXT)
ix = create_in("indexdir", schema)


writer = ix.writer()

for i in range(0,40):
    f=open(f"corpus/butac_{i}.txt","r", encoding='utf-8')
    furl=f.readline()
    furl=furl.rstrip()
    
    ftitle=f.readline()
    ftitle=ftitle.rstrip()
    
    fkeyword=f.readline()
    fkeyword=fkeyword.rstrip()
    
    fcontent =f.read()
    
    writer.add_document(title=ftitle, url=furl,content=fcontent)
    f.close()

for i in range(0, 39):
    f = open(f"corpus/bufale_{i}.txt", "r", encoding='utf-8')
    furl = f.readline()
    furl = furl.rstrip()

    ftitle = f.readline()
    ftitle = ftitle.rstrip()

    fkeyword = f.readline()
    fkeyword = fkeyword.rstrip()

    fcontent = f.read()

    writer.add_document(title=ftitle, url=furl, content=fcontent)
    f.close()

writer.commit()


