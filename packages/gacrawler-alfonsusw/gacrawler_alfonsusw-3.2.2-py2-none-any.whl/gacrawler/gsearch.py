from googleapiclient.discovery import build
import sys
from .config import getConfig
import requests

# https://developers.google.com/apis-explorer/#p/customsearch/v1/search.cse.list
# https://developers.google.com/resources/api-libraries/documentation/customsearch/v1/python/latest/customsearch_v1.cse.html#list

def google_search(search_term, **kwargs):
    my_api_key = getConfig('API', "google_search_api")
    my_cse_id = getConfig('API', "google_cse_id")
    service = build("customsearch", "v1", developerKey=my_api_key)
    res = service.cse().list(q=search_term, cx=my_cse_id, **kwargs).execute()
    return res

def BingWebSearch(search, site):
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key" : getConfig('API', "bing_subs_key")}
    params = {
        "q": search + " (site:" + site + ")",
        "textDecorations": True,
        "responseFilter": "webpages",
        "cc": "ID"
    }
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    ret = []
    for item in search_results['webPages']['value']:
        ret.append(item['url'])
    return ret


def search(query, site):
    ret = []
    try:
        # sort='date:r:20190101:20190105'
        results = google_search(str(query), siteSearch=site)
        for item in results['items']:
            ret.append(item['link'])
        next_response = google_search(
            str(query),
            siteSearch=site,
            num=10,
            start=results['queries']['nextPage'][0]['startIndex'],
        )
        for item in next_response['items']:
            ret.append(item['link'])

        # print ret.__len__()

        # bing search
        results = BingWebSearch(str(query), site)
        for item in results:
            ret.append(item)

    except Exception as ex:
        sys.exc_clear()
        print str(ex)
        ret = None
        pass
    return ret


# print search('debat capres jokowi', 'detik.com')
# print search('jokowi', 'detik.com')
