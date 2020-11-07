from datetime import datetime

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
    return datetime.strptime(date, '%Y-%m-%d %H:%M') # ritorno il formato corretto


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


links = open("links.txt", "r")
counter = 0

for URL in links:

    page = requests.get(URL.rstrip(), headers={"User-Agent": "Mozilla/5.0"})

    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find("h1", class_="news__title").contents[0]

    s = URL
    s += f"{title}\n"

    categories = soup.find("span", class_="news__tags").find_all("a")
    for cat in categories:
        cat = cat.contents[0]
        s += cat + ", "

    s += "\n\n"

    image = soup.find("img", class_="news-image image--large")
    s += f"{image['src']}\n"

    s += f"{convertdate(soup.find('time').attrs['datetime'])}\n"

    # controllo che esista la cartella corpus, se no la creo
    if not os.path.exists("corpus"):
        os.mkdir("corpus/")
    f = open(f"corpus/open_{counter}.txt", "w", encoding='utf-8')

    texts = soup.find("div", class_="article").findAll(text=True)
    visible_texts = filter(tag_visible, texts)

    for t in visible_texts:
        s += t

    f.write(s)
    f.close()
    counter += 1

links.close()
