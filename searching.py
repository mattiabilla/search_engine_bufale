"""
file vecchio di prove, inutile ai fini del progetto finale
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
