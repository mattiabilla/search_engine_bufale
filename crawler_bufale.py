"""
Script per ottenere tutti gli articoli presenti sul sito bufale.net e scriverli in un file.
"""
import requests
from bs4 import BeautifulSoup
import re

# crawler per bufale.net
f = open("linkbufale.txt", "w", encoding='utf-8')
# per ogni pagina che contiene notizie, si scaricano tutti i link degli articoli presenti e si scrivono in un file
for i in range(1, 381):
    URL = f"https://www.bufale.net/bufala/page/{str(i)}/"

    page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find_all(class_="single-archive-post")

    for result in results:
        # scrittura di URL e img separati da virgola nel file
        children = result.find('div', class_='img-notizia col-md-7 col-sm-5 col-xs-5')
        children = children.find('a')
        f.write(children.get("href"))
        children = children.find("div", class_="image-background-container")

        f.write(",")
        img = children.get("data-src")

        f.write(img)
        f.write("\n")

    print(i)

f.close()
