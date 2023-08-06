#!/usr/bin/env python

import multiprocessing as mp
import os, sys, argparse
from functools import partial
from time import time
from bs4 import BeautifulSoup
from urllib2 import urlopen
from . import function as fn
from . import const
from . import gsearch
from .config import getConfig
from .connection import trash_page
from .Genetic import Population, Webpage

sys.setrecursionlimit(int(getConfig('GA', 'ga.max_crawling_queue', int) * 200))

# set current timestamp
TIMESTAMP = str(int(time()))
# seedUrl = []

def fetch(globalDict, url):
    _ = ''
    soup = ''
    try:
        response = fn.curl(url)

        # print (response)

        if response is None:
            trash_page(url, globalDict['output_prefix'])
            return None

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
            trash_page(url, globalDict['output_prefix'])
            return None

        _ = Webpage(url)
        
        for url in soup.find_all('a', href=fn.filter_links):
            _.append_raw_outlinks(url)

        _.set_text(fn.preprocess(text))
        _.set_title(fn.preprocess(soup.title.string))

        print 'Webpage Created: ', _.url
        return _
    except Exception as ex:
        print str(ex)


# FIX 1
# seedUrl.append(Berita("Antara News", "https://www.antaranews.com/search", 'q'))
# seedUrl[-1].set_time_string('startDate', 'endDate', '%d-%m-%Y')
# seedUrl[-1].set_property(
#     parent_selector='.post-content',
#     article_selector='.simple-post'
# )

# FIX 2
# seedUrl.append(Berita("JawaPos", "https://www.jawapos.com/news/search", 'keyword'))
# seedUrl[-1].set_property(
#     parent_selector='.news-thumbnail',
#     article_selector='.thumbnail-article'
# )

# FIX 3
# seedUrl.append(Berita("Detik ", "https://www.detik.com/search/searchall", 'query'))
# seedUrl[-1].set_time_string('fromdatex', 'todatex', '%d/%m/%Y')
# seedUrl[-1].set_property(
#     parent_selector='.list-berita',
#     article_selector='article'
# )

# FIX 4
# seedUrl.append(Berita("CNN Indonesia ", "https://www.cnnindonesia.com/search/", 'query'))
# seedUrl[-1].set_property(
#     parent_selector='.list',
#     article_selector='article'
# )

def detik_remove_class(css_class):
    return css_class != 'video_tag' or css_class != 'foto_tag'

# for url in seedUrl:
#     contents = urllib2.urlopen(url).read()
#     soup = BeautifulSoup(contents, 'html.parser')
#     listBerita = soup.find('div', class_="list-berita").find_all('article', class_=detik_remove_class)
#     for berita in listBerita:
#         pprint(berita.find('a')['href'])

# for url in seedUrl:
#     contents = urllib2.urlopen(url).read()
#     soup = BeautifulSoup(contents, 'html.parser')
#     listBerita = soup.find('div', class_= "list").find_all('article')
#     for berita in listBerita:
#         pprint(berita.find('a')['href'])

# for url in seedUrl:
#     contents = urllib2.urlopen(url).read()
#     soup = BeautifulSoup(contents, 'html.parser')
#     listBerita = soup.find('div', class_='articles--iridescent-list').find_all('article', { 'class': 'articles--iridescent-list--item articles--iridescent-list--text-item' })
#     for berita in listBerita:
#         pprint(berita.find('a')['href'])

def main():
    if const.COMMAND_LINE_MODE:
        parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument("query", type=str, help="Query given to the crawler")
        parser.add_argument("domain", type=str, help="Domain used to crawl (example: detik.com)")
        parser.add_argument("-v", "--verbose", help="Verbose output from the crawler", action="store_true")
        parser.add_argument("-f", "--fake", help="Crawl only, no files created (Useful for debugging).", action="store_true")
        parser.add_argument("-z", "--zip", help="Zip output folder", action="store_true")
        parser.add_argument("--pause", help="Crawler will stop every iteration (Useful for debugging).", action="store_true")
        parser.add_argument("--count", type=int, help="Maximum document to crawl", metavar="c", default=400)
        parser.add_argument("--output", type=str, help="Output folder (without trailing slash), created if not exist", metavar="o", default=TIMESTAMP)

        args = parser.parse_args()
        QUERY = args.query
        DOMAIN = args.domain
        OUTPUT_PREFIX = str(args.output) + "/"

        # BOOL Parameter
        VERBOSE = args.verbose
        FAKE = args.fake
        ZIP = args.zip
        PAUSE = args.pause

        # Create target Directory if don't exist
        if not os.path.exists(OUTPUT_PREFIX):
            os.mkdir(OUTPUT_PREFIX)
            open(OUTPUT_PREFIX + 'relevant.txt', 'a').close()
            open(OUTPUT_PREFIX + 'irrelevant.txt', 'a').close()
        if not os.path.exists(OUTPUT_PREFIX + "documents"):
            os.mkdir(OUTPUT_PREFIX + "documents")

    # building front news url from given seed URL
    startTime = time()
    if(const.DEBUG_MODE):
        frontUrl = [
            'https://sport.detik.com/moto-gp/d-4239130/hasil-tes-bagus-zarco-antusias-tatap-motogp-thailand',
            'https://sport.detik.com/moto-gp/d-4441129/lorenzo-belum-nyaman-dengan-motor-honda',
            'https://sport.detik.com/moto-gp/d-4418103/vinales-tercepat-di-hari-kedua-tes-motogp-sepang',
            'https://sport.detik.com/moto-gp/d-4421450/repsol-honda-tak-impresif-di-tes-sepang-marquez-kalem-saja',
            'https://sport.detik.com/moto-gp/d-3891818/pedrosa-bicara-soal-rekayasa-trek-basah-dalam-tes-motogp-qatar',
            'https://sport.detik.com/moto-gp/d-4444618/balapan-kurang-dari-2-minggu-ini-pr-yamaha-menurut-vinales',
            'https://sport.detik.com/moto-gp/d-4368274/jadwal-tes-pramusim-motogp-2019',
            'https://sport.detik.com/moto-gp/d-4419792/petrucci-kuasai-hari-terakhir-tes-motogp-sepang',
            'https://sport.detik.com/moto-gp/d-4442052/alex-rins-ungguli-vinales-di-tes-motogp-qatar-hari-kedua',
            'https://sport.detik.com/moto-gp/d-4325521/marquez-tes-motogp-berjalan-bagus-tapi-honda-harus-waspada',
            'https://sport.detik.com/moto-gp/d-4443729/vinales-tercepat-di-hari-terakhir-tes-motogp-qatar',
            'https://sport.detik.com/moto-gp/d-4416465/marquez-tercepat-di-hari-pertama-tes-motogp-sepang',
            'https://sport.detik.com/moto-gp/d-4330361/rossi-lorenzo-akan-kencang-di-tes-motogp-sepang',
            'https://sport.detik.com/moto-gp/d-4441080/vinales-tercepat-di-hari-pertama-tes-motogp-qatar',
            'https://sport.detik.com/moto-gp/d-4309960/tes-motogp-valencia-vinales-tercepat-di-hari-pertama',
            'https://sport.detik.com/moto-gp/d-3893950/vinales-percaya-diri-pada-hari-pertama-tes-di-losail',
            'https://sport.detik.com/moto-gp/d-3896978/zarco-tercepat-di-hari-terakhir-rossi-kedua'
        ]
    else:
        frontUrl = []
        # for webpage in seedUrl:
        #     endUrl = webpage.endUrl(query)
        #     soup = BeautifulSoup(fn.curl(url=endUrl), 'html.parser')

        #     # listBerita = soup.find('div', class_="list-berita").find_all('article', class_=detik_remove_class)
        #     listBerita = soup.select_one(webpage.parent_selector).select(webpage.article_selector)
        #     for berita in listBerita:
        #         frontUrl.append(berita.select_one('a[href]')['href'])
        frontUrl = gsearch.search(QUERY, DOMAIN)

    frontUrl = set(frontUrl)
    for url in frontUrl:
        if fn.filter_links is False: frontUrl.remove(url)
    pop = Population(_crawlingQueue=frontUrl, _query=QUERY)

    # extra attribute for genetic
    pop.DICT['output_prefix'] = OUTPUT_PREFIX
    pop.DICT['domain'] = DOMAIN
    pop.DICT['count'] = args.count

    # final front Url = ambil semua url dari hasil search setiap portal berita
    for i in range(getConfig('GA', 'ga.max_generation', int)):
        if pop.start is False:
            print pop.stop_reason
            break

        trashed = 0
        processes = []
        results = []

        globalDict = {'output_prefix': OUTPUT_PREFIX}
        p = mp.Pool(mp.cpu_count())
        # results = p.map(fetch, pop.crawlingQueue)
        results = p.map(partial(fetch, globalDict), pop.crawlingQueue)
        p.close()

        for result in results:
            if result is None: continue
            pop.append(result)

        print "Crawling Queue: ", str(pop.crawlingQueue.__len__())

        # update crawling queue dari population
        pop.generate()
        if PAUSE: os.system("pause")
    
    _ = time() - startTime
    print "Elapsed Time: " + str(_) + "s"
    _ = pop.relevant_count + pop.irrelevant_count
    print "Crawled Pages: " + str(_)
    print "Predicted Relevant: " + str(pop.relevant_count)
    _ = pop.relevant_count/_
    print "Harvest Rate: " + str(_)

    if ZIP:
        import zipfile
        zipf = zipfile.ZipFile(OUTPUT_PREFIX + '.zip', 'w', zipfile.ZIP_DEFLATED)
        fn.zipdir(OUTPUT_PREFIX, zipf)
        zipf.close()

# pprint (len(listWebpage))
# # listUrl = set(listUrl)
# pprint (listWebpage)
