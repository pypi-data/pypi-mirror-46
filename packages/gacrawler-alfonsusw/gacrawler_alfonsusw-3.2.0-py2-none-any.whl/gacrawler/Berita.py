import datetime
import urllib

class Berita:
    """ Class untuk berita """

    def __init__(self, _name, _url, _queryS = 'q'):
        # queryS = query string
        # fromS = from string
        self.name = _name
        self.url = _url

        self.has_date = False

        self.queryS = _queryS

    def endUrl(self, _query, _from=None, _to=None):
        if(_from is None) or (_to is None):
            tTo = datetime.datetime.now()
            tFrom = tTo - datetime.timedelta(days=30)
        else:
            tTo = datetime.datetime.strptime(_to, '%d/%m/%Y')
            tFrom = datetime.datetime.strptime(_from, '%d/%m/%Y')

        if(self.has_date):
            build_query = {
                self.queryS: _query,
                self.fromS: tFrom.strftime(self.date_format),
                self.toS: tTo.strftime(self.date_format)
            }
        else:
            build_query = {
                self.queryS: _query
            }

        return self.url + "?" + urllib.urlencode(build_query)

    def set_time_string(self, _fromS, _toS, _date_format='%d/%m/%Y'):
        self.has_date = True
        self.fromS = _fromS
        self.toS = _toS
        self.date_format = _date_format

    def set_property(self, parent_selector, article_selector):
        self.parent_selector = parent_selector
        self.article_selector = article_selector
