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

    page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})

    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find("div",class_="titleArticle").find("h1").contents
    title = title[0]

    s = URL
    s += f"{title}\n"

    categories=soup.find("div",class_="tags").find("ul").find_all("li")
    for cat in categories:
        cat = cat.find("a").contents[0]
        s += cat + ", "

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
