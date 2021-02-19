"""
Script per ottenere tutti gli articoli presenti sul sito butac.it e scriverli in un file.
"""
import requests
from bs4 import BeautifulSoup
import re

# crawler per butac.it
f = open("linkbutac.txt", "w", encoding='utf-8')
# per ogni pagina che contiene notizie, si scaricano tutti i link degli articoli presenti e si scrivono in un file
for i in range(1, 252):
    URL = "https://www.butac.it/category/bufala/page/" + str(i) + "/"

    page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find("div", class_="archives").find_all(class_="j-title")

    for result in results:
        try:
            # si ottiene l'URL dell'immagine dell'articolo
            img = result
            img = img.find_parent('div')
            img = img.find_parent('div')
            img = img.find("div", class_="image")

            style = img.get("style")
            p = re.compile(r'http.*\)')
            match = p.search(style)
            img = match.group(0)[:len(match.group(0)) - 1]
        except:
            img = "https://www.butac.it/wp-content/themes/butac/images/LOGO_DESKTOP_WHITE-2.png"

        result = result.find('h3')
        result = result.find("a")

        # scrittura di URL e img separati da virgola nel file
        f.write(result.get("href"))
        f.write(",")
        f.write(img)

        f.write("\n")
    print(i)
f.close()
