from crawler.crawler_bufale import searchlinkbufale
from crawler.crawler_open import searchlinkopen
from crawler.crawler_butac import searchlinkbutac
import crawler.crawler_articoli_bufale as cbufale
import crawler.crawler_articoli_open as copen
import crawler.crawler_articoli_butac as cbutac

fonti = [
    'www.bufale.net',
    'www.open.online',
    'www.butac.it'
]
def crawl():
    counter_bufale = counter_open = counter_butac = 0
    searchlinkbufale()
    searchlinkbutac()
    searchlinkopen()

    for URL in open("links.txt", 'r'):
        if fonti[0] in URL:
            cbufale.getpage(URL, counter_bufale)
        elif fonti[1] in URL:
            copen.getpage(URL, counter_open)
        elif fonti[2] in URL:
            cbutac.getpage(URL, counter_butac)