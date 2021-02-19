"""
script con cui vengono scaricati tutti gli articoli del sito bufale.net, prendendoli dal file linkbufale.txt
e inseriti nella cartella "corpus".
"""
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from bs4.element import Comment
import os

# dizionario per la traduzione del nome del mese nel corrispondente valore numerico
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
    """
    Funzione per convertire la data letta in un formato a piacere.
    :param date: Data letta dal sito.
    :return: Data da inserire nel file del corpus.
    """
    mese = (date[0])[:date[0].find(' ')]  # per prendere il mese dalla stringa
    mese = month.get(mese)  # sostituisco il mese con la sua traduzione dal dizionario
    mese = date[0].replace((date[0])[:date[0].find(' ')], mese)  # costruisco la stringa in un formato leggibile
    return datetime.strptime(mese, '%m %d, %Y')  # ritorno l'oggetto costruito


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


links = open("linkbufale.txt", "r", encoding='utf-8')
counter = 0

# per ogni link che è contenuto nel file, si ottengono le parti che ci interessano
for URL in links:
    parts = URL.split(",")  # ogni riga è composta dal link della pagina e dal link della sua immagine, separati da ","
    URL = parts[0]
    img = parts[1]
    page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})

    soup = BeautifulSoup(page.content, "html.parser")

    # si prende il titolo della pagina
    title = soup.find(class_="title").findChildren('h1')[0]

    s = URL + "\n"
    s += f"{title.contents[0]}\n"

    categories = soup.find_all(class_="tag")
    for cat in categories:
        cat = cat.contents
        cat = cat[1].findChildren('a', recursive=True)
        for _ in cat:
            s += _.contents[0] + ", "

    s += "\n"
    try:
        image = img
        s += image + "\n"
    except:
        s += "https://static.nexilia.it/bufale/2016/10/logo_bufale.png\n"

    s += f"{convertdate(soup.find('time').contents)}\n"

    s += "\n\n"

    # controllo che esista la cartella corpus, se no la creo
    if not os.path.exists("corpus"):
        os.mkdir("corpus/")

    f = open(f"corpus/bufale_{counter}.txt", "w", encoding='utf-8')
    try:
        texts = soup.find(class_="text-article").findAll(text=True)
        visible_texts = filter(tag_visible, texts)

        for t in visible_texts:
            s += t
    except:
        pass

    # qui la variabile "s" conterrà tutto il contenuto del sito selezionato, così è scritta su file
    f.write(s)
    f.close()
    counter += 1
    print(str(counter) + " " + URL)

links.close()
