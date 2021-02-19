"""
script con cui vengono scaricati tutti gli articoli del sito open.online, prendendoli dal file linkopen.txt
e inseriti nella cartella "corpus"
"""
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import os

# dizionario per la traduzione del nome del mese nel corrispondente valore numerico
month = {
    "Gen": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "Mag": "05",
    "Giu": "06",
    "Lug": "07",
    "Ago": "08",
    "Set": "09",
    "Ott": "10",
    "Nov": "11",
    "Dic": "12"
}


def convertdate(date):
    """
    Funzione per convertire la data letta in un formato a piacere.
    :param date: Data letta dal sito.
    :return: Data da inserire nel file del corpus.
    """
    return datetime.strptime(date, '%Y-%m-%d %H:%M') # ritorno il formato corretto


def tag_visible(element):
    """
    Filtro utilizzato per prendere tutti e solo i tag di una pagina web che contengono qualcosa di visibile.
    :param element: Il tag da controllare.
    :return: True se il tag è tra i "visibili", False altrimenti.
    """
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


links = open("linkopen.txt", "r",encoding='utf-8')
counter = 0

# per ogni link che è contenuto nel file, si ottengono le parti che ci interessano
for URL in links:
    counter += 1

    parts = URL.split(",")  # ogni riga è composta dal link della pagina e dal link della sua immagine, separati da ","
    URL = parts[0]
    img = parts[1]

    page = requests.get(URL.rstrip(), headers={"User-Agent": "Mozilla/5.0"})

    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find("h1", class_="news__title").contents[0]

    s = URL+"\n"
    s += f"{title}\n"

    try:
        categories = soup.find("span", class_="news__tags").find_all("a")
        for cat in categories:
            cat = cat.contents[0]
            s += cat + ", "
    except:
        pass

    s += "\n"
    try:
        image = img
        s += f"{image}\n"
    except:
        s += "https://storage.avalanches.com/it/6303/images/avatar_domain_open.online.jpg\n"

    s += f"{convertdate(soup.find('time').attrs['datetime'])}\n"

    s += "\n\n"

    # controllo che esista la cartella corpus, se no la creo
    if not os.path.exists("corpus"):
        os.mkdir("corpus/")
    f = open(f"corpus/open_{counter}.txt", "w", encoding='utf-8')

    try:
        texts = soup.find("div", class_="article").findAll(text=True)
        visible_texts = filter(tag_visible, texts)

        for t in visible_texts:
            if "Leggi anche:" in t:
                break
            s += t
    except:
        pass

    # qui la variabile "s" conterrà tutto il contenuto del sito selezionato, così è scritta su file
    f.write(s)
    f.close()

    print(str(counter)+" "+URL)

links.close()
