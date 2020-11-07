from datetime import datetime

import re

import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import os


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
    mese = re.compile(" (.*?) ")  # per prendere tutto quello che c'è tra gli spazi, ovvero il mese
    mese = mese.search(date).group().strip()  # prendo il mese con la regex
    date = date.replace(mese, month.get(mese)) # costruisco la stringa in un formato leggibile
    return datetime.strptime(date, '%d %m %Y') # ritorno l'oggetto costruito


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


links = open("links.txt", "r")
counter = 0

for URL in links:

    page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})

    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find("div", class_="titleArticle").find("h1").contents[0]

    s = URL
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
        image = soup.find("img", class_="img-responsive wp-post-image")
        s += f"{image['data-src']}\n"
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

    f.write(s)
    f.close()
    counter += 1

links.close()
