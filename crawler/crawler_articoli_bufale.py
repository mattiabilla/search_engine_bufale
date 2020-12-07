import requests
from datetime import datetime
from bs4 import BeautifulSoup
from bs4.element import Comment
import os

month = {
    "Gennaio": "01",
    "Febbraio": "02",
    "Marzo": "03",
    "Aprile": "04",
    "Maggio": "05",
    "Giugno": "06",
    "Luglio": "07",
    "Agosto": "08",
    "Settembre": "09",
    "Ottobre": "10",
    "Novembre": "11",
    "Dicembre": "12"
}


def convertdate(date):
    mese = (date[0])[:date[0].find(' ')]  # per prendere il mese dalla stringa
    mese = month.get(mese)  #sostituisco il mese con la sua traduzione dal dizionario
    mese = date[0].replace((date[0])[:date[0].find(' ')], mese) # costruisco la stringa in un formato leggibile
    return datetime.strptime(mese, '%m %d, %Y') # ritorno l'oggetto costruito


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

#links = open("links.txt", "r")
#counter = 0

#for URL in links:
def getpage(URL, counter):
    page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})

    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find(class_="title").findChildren('h1')[0]

    s = URL
    s += f"{title.contents[0]}\n"

    categories = soup.find_all(class_="tag")
    for cat in categories:
        cat = cat.contents
        cat = cat[1].findChildren('a', recursive=True)
        for _ in cat:
            s += _.contents[0] + ", "

    s += "\n"
    try:
        image = soup.find(id="post-thumbnail").find("figure").find("img", class_="img-responsive wp-post-image")
        s += f"{image['data-src']}\n"
    except:
        s += "https://static.nexilia.it/bufale/2016/10/logo_bufale.png\n"


    s += f"{convertdate(soup.find('time').contents)}\n"

    s += "\n\n"

    # controllo che esista la cartella corpus, se no la creo
    if not os.path.exists("../corpus"):
        os.mkdir("../corpus/")

    f = open(f"../corpus/bufale_{counter}.txt", "w", encoding='utf-8')

    texts = soup.find(class_="text-article").findAll(text=True)
    visible_texts = filter(tag_visible, texts)

    for t in visible_texts:
        s += t

    f.write(s)
    f.close()
    counter += 1

#links.close()
