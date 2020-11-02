import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Comment
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

    results = soup.find(class_="td-ss-main-content")

    texts = results.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h5", "i", "li", "b", "strong", "blockquote"])

    title = soup.find(class_="entry-title").contents
    title = title[0]

    s = URL
    s += f"{title}\n"

    categories = soup.find_all(class_="entry-category")
    for cat in categories:
        cat = cat.contents
        print(cat)
        cat = cat[0].contents[0]
        s += cat + ", "
    s += "\n\n"

    # controllo che esista la cartella corpus, se no la creo
    if not os.path.exists("corpus"):
        os.mkdir("corpus/")
    f = open(f"corpus/butac_{counter}.txt", "w", encoding='utf-8')

    texts = soup.find(class_="text-article").findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    # s.join(t for t in visible_texts)
    for t in visible_texts:
        s += t
    '''for i in texts:
        # print("----------------------------------------------------------------------")
        for _ in i:
            if isinstance(_, NavigableString):
                # print(_.string)
                s += _.string + "\n"'''

    f.write(s)
    f.close()
    counter += 1

links.close()