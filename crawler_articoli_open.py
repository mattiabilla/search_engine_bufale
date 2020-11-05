import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import os


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
