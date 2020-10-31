import requests
from bs4 import BeautifulSoup

#crawler per bufale.net
f = open("links.txt", "a")
for i in range(1, 10):
    URL = f"https://www.bufale.net/bufala/page/{str(i)}/"

    page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find_all(class_="single-archive-post")

    for result in results:
        children = result.find('div', class_='img-notizia col-md-7 col-sm-5 col-xs-5')
        children = children.find('a')
        f.write(children.get("href"))
        f.write("\n")

f.close()
