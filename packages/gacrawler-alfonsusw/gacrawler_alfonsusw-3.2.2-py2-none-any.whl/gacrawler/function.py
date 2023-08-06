import urllib2
import random
from .config import getConfig
import re
import math
import unicodedata
import sys
from furl import furl
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

agents= [
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
]

def curl(url=None):
    if url is None:
        return
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', random.choice(agents))]
    response = opener.open(url)
    return response


def selectOne(individuList, exceptIndex=[]):
    mul_val = 100
    fit_sum = 0
    arr_element = []
    ctr = 0
    for i in individuList:
        if ctr in exceptIndex:
            ctr += 1
            continue

        num_element = int(i[1] * mul_val)
        fit_sum += num_element
        for j in range(num_element):
            arr_element.append(ctr)
        ctr += 1
    return arr_element[random.randint(0, fit_sum - 1)]

def acceptReject(population, maxFitness, attribute=True):
    while True:
        partner = random.choice(population)
        r = random.uniform(0, maxFitness)
        if attribute:
            if (r < partner.fitness):
                return partner
        else:
            if(r < partner[1]):
                return partner


def roulette(individuList, exceptIndex=[]):
    mul_val = 100
    fit_sum = 0
    arr_element = []
    ctr = 0
    for i in individuList:
        if ctr in exceptIndex:
            ctr += 1
            continue

        num_element = int(i.fitness*mul_val)
        fit_sum += num_element
        for j in range(num_element):
            arr_element.append(ctr)
        ctr += 1
    return arr_element[random.randint(0, fit_sum-1)]

def clean_tag(soup, selector):
    for sc in soup.find_all('script'):
        sc.decompose()
    for sc in soup.find_all('style'):
        sc.decompose()
    for tag in selector:
        for sc in soup.select(tag):
            sc.decompose()
    return

def preprocess(_berita):
    factory  = StemmerFactory()
    stemmer  = factory.create_stemmer()

    factory  = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()

    contents = _berita.replace(".", " ")

    striped = re.sub('[^\w\s]','',contents)
    striped = re.sub('_','',striped)
    striped = re.sub('\s',' ',striped)
    # striped = re.sub('[0-9]','',striped)

    striped = striped.strip()
    stop    = stopword.remove(striped)
    output  = stemmer.stem(stop)

    return output

def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def get_jaccard_sim(str1, str2):
    a = set(str1.split())
    b = set(str2.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))

def get_jaccard_sim_binary(a, b):
    AdotB = 0
    for i, j in zip(a, b):
        AdotB = AdotB + (i*j)
    A = sum(a)
    B = sum(b)
    return float(AdotB) / (A + B - AdotB)

def get_href_text(str1):
    maxStr = ''
    str2 = str1.split('/')
    for i in range(len(str2)):
        if(len(str2[-(i+1)]) > len(maxStr)):
            maxStr = str2[-(i + 1)]
    return preprocess(maxStr.replace('-', ' '))


def filter_links(href):
    if href is None:
        return False
    return all([
        href,
        any([
            href.startswith('http'),
            href.startswith('https')
        ]),
        href.find('foto') == -1,
        (len(href) >= getConfig('BS4', 'bs4.min_url_length', int))
    ])

def check_url(url, con, output_prefix=None, href_text=None):
    # outlink criteria
    _ = [
        con.find_page(url, output_prefix) is False
    ]
    if href_text is not None:
        _.append(len(href_text) >= getConfig('BS4', 'bs4.min_url_length', int))

    return True if all(_) else False


def zipdir(path, ziph):
    import os
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(
                os.path.join(root, file),
                os.path.relpath(
                    os.path.join(root, file), os.path.join(path, '..')))