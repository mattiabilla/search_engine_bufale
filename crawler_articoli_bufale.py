import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
import os

links = open("links.txt", "r")
counter = 0

for URL in links:

    page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(class_="text-article")

    texts = results.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h5", "i", "li", "b", "strong", "blockquote"])

    title = soup.find(class_="title").findChildren('h1')
    title = title[0]

    s = URL
    s += f"{title.contents[0]}\n"

    categories = soup.find_all(class_="tag")
    for cat in categories:
        cat = cat.contents
        cat = cat[1].findChildren('a', recursive=True)
        for _ in cat:
            s += _.contents[0] + ", "
    s += "\n\n"
    # controllo che esista la cartella corpus, se no la creo
    if not os.path.exists("corpus"):
        os.mkdir("corpus/")

    f = open(f"corpus/bufale_{counter}.txt", "w", encoding='utf-8')
    for i in texts:
        for _ in i:
            try:
                if isinstance(_, NavigableString):
                    s += _.string + "\n"

                    # QUI VIENE LANCIATO L'ERRORE
                elif isinstance(_, Tag):
                    if _.name == 'a':
                        s += _.contents[0] + "\n"
                    elif _.name == 'strong':
                        s += _.contents[0] + "\n"
            except TypeError:
                print(_)

    f.write(s)
    f.close()
    counter += 1

links.close()
