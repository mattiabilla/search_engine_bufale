import urllib.request

from bs4 import BeautifulSoup, Comment


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t for t in visible_texts)


html = urllib.request.urlopen('https://www.bufale.net/la-finta-lettera-di-sean-connery-a-steve-jobs-bufale-che-tornano-virali/').read()
print(text_from_html(html))
