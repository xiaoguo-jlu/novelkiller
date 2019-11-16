import time
import random
from urllib.parse import urljoin
import threading

from bs4 import BeautifulSoup as bs
import requests
from sqlalchemy.exc import StatementError

from log import log
from model.category import Category
from model.novel import Novel
from model.author import Author
from model.download_result import DownloadResult
from dao.write import write_model
from dao.read import get_id, check_novel_download_finished
from model.chapter import Chapter
from model.text import Text
from parsers.category import CategoryParser
from parsers.novel import NovelParser
from parsers.chapter import ChapterParser

spider_log = log.Log()
error_log = log.Log("error.log")
download_history = []

class Spider():
    def __init__(self, url = ""):
        self.url = url
        self.page = None
        self.log = spider_log
        self.timeout = 15
        self.download_result_list = []
        self.url_quene = []
        self.data = []
        
    def wait_seconds(self):
        time.sleep(random.random()*2 + 1)

    def fetch_page(self,url=""):
        if url:
            self.url = url
        spider_log.debug("current url is " + self.url)
        header = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        }
        response = requests.get(self.url, headers = header)
        status_code = response.status_code
        if status_code == 200:
            self.page = bs(response.content)
        else:
            self.log.debug("Failed to visit the page %s, error_code : %s"%(self.url,status_code))
        spider_log.debug("Done")
        download_result = DownloadResult(url = self.url, result = status_code)
        write_model(download_result)
        return self.page

    def fetch_next(self):
        if not self.url_quene:
            return
        self.url = self.url_quene.pop(0)
        if self.url:
            self.fetch_page()
            self.parse_page()
            self.process_data()
            self.wait_seconds()
            self.fetch_next(self)

    # 将解析出的url队列添加到self.url_quene
    # 将解析出的数据添加到self.data
    def parse_page(self):
        raise NotImplementedError

    # 处理数据，将self.data中的模型持久化写入数据库
    def process_data(self):
        raise NotImplementedError

    def run(self):
        self.fetch_page()
        self.parse_page()
        self.process_data()
        self.wait_seconds()
    
class NovelSpider(Spider):
    def __init__(self):
        super().__init__("https://www.biquge.com.cn/xuanhuan/")

    def parse_page(self):
        pass

    def process_data(self):
        pass

    def run(self):
        self.fetch_page()
        category_result = CategoryParser(self.page).parse()
        category = Category()
        category.id = 2
        for novel_url in category_result.url_quene:
            self.fetch_page(novel_url)
            novel_parser_result = NovelParser(self.page).parse()
            author = novel_parser_result.data['author']
            novel = novel_parser_result.data['novel']
            spider_log.debug("fetching novel %s"%novel.name)
            try:
                get_id(author)
            except IndexError:
                write_model(author)
            author.id = get_id(author)
            novel.author_id = author.id
            if check_novel_download_finished(novel):
                continue
            try:
                get_id(novel)
            except IndexError:
                write_model(novel)
            novel.id = get_id(novel)
            novel.category_id = category.id
            serial = 0
            for chapter_url in novel_parser_result.url_quene:
                serial = serial + 1
                self.fetch_page(chapter_url)
                chapter_result = ChapterParser(self.page).parse()
                chapter = chapter_result.data['chapter']
                spider_log.debug("fetching chapter %s"%chapter.name)
                chapter.novel_id = novel.id
                chapter.serial = serial
                try:
                    get_id(chapter)
                except IndexError:
                    write_model(chapter)
                chapter.id = get_id(chapter)
                text = chapter_result.data['text']
                text.chapter_id = chapter.id
                try:
                    write_model(text)
                except sqlalchemy.exc.StatementError:
                    error_log.write("Error in novel %s %s chapter"%(novel.name, chapter.name))
                spider_log.debug("succeed in fetching chapter %s"%chapter.name)
            novel.finished = 'Y'
            spider_log.debug("succeed in fetching novel %s"%novel.name)
            write_model(novel)




def test():
    a = NovelSpider()
    a.run()

if __name__ == "__main__":
    test()