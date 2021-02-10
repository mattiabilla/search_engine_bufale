import requests
from bs4 import BeautifulSoup
import re

# crawler per butac.it
f = open("linkbutac.txt", "w",encoding='utf-8')
for i in range(1, 252):
    URL = "https://www.butac.it/category/bufala/page/" + str(i) + "/"

    page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find("div", class_="archives").find_all(
        class_="j-title")  # .find("h3").find_all('a', class_='blackText')

    for result in results:
        try:
            img = result
            img = img.find_parent('div')
            img = img.find_parent('div')
            #print(img)
            img = img.find("div", class_="image")

            style = img.get("style")
            #print(style)
            p = re.compile(r'http.*\)')
            match = p.search(style)
            img = match.group(0)[:len(match.group(0))-1]
        except:
            img="https://www.butac.it/wp-content/themes/butac/images/LOGO_DESKTOP_WHITE-2.png"
        #print(img)

        result = result.find('h3')
        result = result.find("a")

        f.write(result.get("href"))
        f.write(",")
        f.write(img)

        f.write("\n")
    print(i)
f.close()
