# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 23:06:58 2020

@author: Mattia
"""
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser

from whoosh.index import open_dir

import re
from flask import Flask, request, render_template

from whoosh.highlight import SentenceFragmenter

from nltk.corpus import wordnet as wn

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home_results():
    data = ""
    if request.method == 'GET' and 'query' in request.args:  # this block is only entered when the form is submitted
        data = request.args.get('query')
        # print(data)

    # print(data)
    retrieved = []
    did_you_mean = None
    ix = open_dir("../indexdir")
    with ix.searcher() as searcher:
        qp = None
        thterm = ""
        # provvisorio ricerca con thesaurus con []
        if "[" in data and "]" in data:
            qp = MultifieldParser(["categories", "content"], ix.schema)
            thterm = data[data.find("["):data.find("]")]
            wn.synsets(thterm)

        else:
            qp = QueryParser("content", ix.schema)
        query = qp.parse(data)
        corrected = searcher.correct_query(query, data)
        if corrected.query != query:
            did_you_mean = corrected.string
        results = searcher.search(query)
        results.fragmenter = SentenceFragmenter()
        for i in results:
            link = i["url"]
            title = i["title"]
            linkimage = i["urlimage"]
            date = i["date"]
            date = date.strftime("%d/%m/%Y")
            snippet = i.highlights("content", top=1)#, scorer=BasicFragmentScorer, order=SCORE)
            print(snippet)

            p = re.compile("www\.[^\/]+")
            match = p.search(link)
            site = match.group(0)
            print(site)

            retrieved.append({"link": link, "title": title, "site": site, "urlimage": linkimage, "date": date, "snippet":snippet})

    return render_template("index.html", results=retrieved, correction=did_you_mean)
