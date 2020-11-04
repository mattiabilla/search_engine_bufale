import requests
from bs4 import BeautifulSoup

# crawler per butac.it
f = open("links.txt", "w")
for i in range(1, 5):
    URL = "https://www.butac.it/category/bufala/page/" + str(i) + "/"

    page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find("div", class_="archives").find_all(
        class_="j-title")  # .find("h3").find_all('a', class_='blackText')

    for result in results:
        result = result.find('h3')
        result = result.find("a")

        f.write(result.get("href"))

        f.write("\n")

f.close()
