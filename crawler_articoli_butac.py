"""
script con cui vengono scaricati tutti gli articoli del sito butac.it, prendendoli dal file linkbutac.txt
e inseriti nella cartella "corpus"
"""
from datetime import datetime

import re

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
    mese = re.compile(" (.*?) ")  # per prendere tutto quello che c'è tra gli spazi, ovvero il mese
    mese = mese.search(date).group().strip()  # prendo il mese con la regex
    date = date.replace(mese, month.get(mese))  # costruisco la stringa in un formato leggibile
    return datetime.strptime(date, '%d %m %Y')  # ritorno l'oggetto costruito


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


links = open("linkbutac.txt", "r", encoding='utf-8')
counter = 0

# per ogni link che è contenuto nel file, si ottengono le parti che ci interessano
for URL in links:
    parts = URL.split(",") # ogni riga è composta dal link della pagina e dal link della sua immagine, separati da ","
    URL = parts[0]
    img = parts[1]

    page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})

    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find("div", class_="titleArticle").find("h1").contents[0]

    s = URL + "\n"
    s += f"{title}\n"

    try:
        categories = soup.find("div", class_="tags").find("ul").find_all("li")
        for cat in categories:
            cat = cat.find("a").contents[0]
            s += cat + ", "
    except:
        s += ""

    s += "\n"

    try:
        image = img
        s += f"{image}\n"
    except:
        s += "https://www.butac.it/wp-content/themes/butac/images/LOGO_DESKTOP_WHITE-2.png\n"

    s += f"{convertdate(soup.find('time').attrs['datetime'])}\n"

    s += "\n\n"

    # controllo che esista la cartella corpus, se no la creo
    if not os.path.exists("corpus"):
        os.mkdir("corpus/")
    f = open(f"corpus/butac_{counter}.txt", "w", encoding='utf-8')

    texts = soup.find(class_="textArticle").findAll(text=True)
    visible_texts = filter(tag_visible, texts)

    for t in visible_texts:
        s += t

    # qui la variabile "s" conterrà tutto il contenuto del sito selezionato, così è scritta su file
    f.write(s)
    f.close()
    counter += 1
    print(counter)

links.close()
