from bs4 import BeautifulSoup as bs
class Parser(object):
    def __init__(self,  page):
        if isinstance(page, bs):
            self.page = page
        elif isinstance(page, str):
            self.page = bs(page)
        else:
            raise TypeError("Failed to parse %s type data"%(type(page)))

    def parse(self):
        raise NotImplementedError


class ResultList(object):
    def __init__(self):
        self.data = []
        self.url_quene = []

    
class ParseException(Exception):
    pass