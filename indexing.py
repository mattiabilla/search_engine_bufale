import os
from os import listdir
from os.path import isfile, join

from whoosh.index import create_in
from whoosh.fields import *

schema = Schema(title=TEXT(stored=True), url=ID(stored=True), content=TEXT)
if not os.path.exists("indexdir"):
    os.mkdir("indexdir/")
ix = create_in("indexdir", schema)

filelist = [f for f in listdir("corpus") if isfile(join("corpus", f))]

writer = ix.writer()

for i in filelist:
    f = open("corpus/" + i, "r", encoding='utf-8')
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
