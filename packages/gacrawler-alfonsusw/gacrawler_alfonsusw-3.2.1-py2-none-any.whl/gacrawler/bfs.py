from . import gsearch
from . import function as fn
from .connection import trash_page
from .config import getConfig
from bs4 import BeautifulSoup

crawlingQueue = gsearch.search("pemilu 2019", "detik.com")
while True:
    for url in crawlingQueue:
        response = fn.curl(url)
        # print (response)

        if response is None:
            continue

        soup = BeautifulSoup(response, 'html.parser')

        # clean tag yang tidak diperlukan
        # bisa ditambah dengan tag iklan atau sisipan
        fn.clean_tag(soup=soup, selector=getConfig('BS4', 'bs4.decompose_selector').split(','))


        # coba semua tag yang ada di const
        for tag in getConfig('BS4', 'bs4.text_selector').split(','):
            text = soup.select_one(tag)
            text = text.get_text() if text is not None else None

            # mengatasi kalau ada tag yang isi text nya kurang dari const
            if (text is not None and len(text) > getConfig('BS4', 'bs4.min_news_word_count', int)):
                break

        # kalau tidak ketemu dengan selector yang ada di const
        # continue url
        if (text is None):
            # trashed += 1
            continue

        
        for _url in soup.find_all('a', href=fn.filter_links):
            crawlingQueue.append(_url)

        with open("bfs/" + fn.preprocess(soup.title.string).replace(" ", "-") + ".txt", "a+") as f:
            f.write(fn.preprocess(text))

        print 'Webpage Created: ', url