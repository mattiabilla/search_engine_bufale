# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 23:06:58 2020

@author: Mattia
"""
from whoosh.qparser import QueryParser
from whoosh.index import open_dir


import re
from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home_results():

    data = ""
    if request.method == 'GET' and 'query' in request.args:  #this block is only entered when the form is submitted
        data = request.args.get('query')
        print(data)

    print(data)
    retrieved = []
    ix = open_dir("../indexdir")
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(data)
        results = searcher.search(query)
        for i in results:
            link = i["url"]
            title = i["title"]
            linkimage = i["urlimage"]
            date = i["date"]
            date = date.strftime("%d/%m/%Y")

            p = re.compile("www\.[^\/]+")
            match = p.search(link)
            site=match.group(0)
            print(site)

            retrieved.append({"link":link,"title":title,"site":site, "urlimage":linkimage, "date":date})

    return render_template("index.html", results=retrieved)