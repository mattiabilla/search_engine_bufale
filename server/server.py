# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 23:06:58 2020

@author: Mattia
"""
from whoosh.qparser import QueryParser
from whoosh.index import open_dir



from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home_results():
    #data = request.form.get('query', "")
    data=""
    if request.method == 'GET' and 'query' in request.args:  #this block is only entered when the form is submitted
        data = request.args.get('query')
        print(data)
        
    
    s=f"""
        <form action="/" method="GET">
          
          <input type="text" id="query" name="query" value="{data}"><br>
          
          <input type="submit" value="Submit">
        </form>
    
    """
    print(data)
    ix = open_dir("../indexdir")
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(data)
        results = searcher.search(query)
        for i in results:
            link=i["url"]
            s+= f"<div><a href='{link}'>"+i["title"]+"</a></div>"
    return s