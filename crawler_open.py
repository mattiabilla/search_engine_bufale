"""
Script per ottenere tutti gli articoli presenti sul sito open.online e scriverli in un file.
"""
import requests
from bs4 import BeautifulSoup

# crawler per bufale.net
f = open("linkopen.txt", "w", encoding='utf-8')
# per ogni pagina che contiene notizie, si scaricano tutti i link degli articoli presenti e si scrivono in un file
for i in range(1, 94):
    URL = f"https://www.open.online/c/fact-checking/page/{str(i)}/"

    page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find_all("figure", class_="news__thumbnail image-wrap")

    for result in results:
        children = result.find("a")
        # scrittura di URL e img separati da virgola nel file
        f.write(children.get("href"))

        children = result.find("img")
        f.write(",")
        f.write(children.get("src"))

        f.write("\n")
    print(i)
f.close()
