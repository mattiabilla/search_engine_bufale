# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 22:48:34 2020

@author: Mattia
"""

from whoosh.qparser import QueryParser
from whoosh.index import open_dir

ix = open_dir("indexdir")

with ix.searcher() as searcher:
    corrector = searcher.corrector("content")
    s = "Salvini"
    query = QueryParser("content", ix.schema).parse(s)
    print(corrector.suggest(s, limit=1))
    results = searcher.search(query)
    for i in results:
        print(i)
