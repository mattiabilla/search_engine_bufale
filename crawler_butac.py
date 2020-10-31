import requests
from bs4 import BeautifulSoup

# crawler per butac.it
f = open("links.txt", "a")
for i in range(1, 15):
    URL = "https://www.butac.it/category/bufala/page/" + str(i) + "/"

    page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(class_="td-main-content-wrap td-container-wrap").find_all('a', class_='td-image-wrap')

    for result in results:
        f.write(result.get("href"))
        f.write("\n")

f.close()
