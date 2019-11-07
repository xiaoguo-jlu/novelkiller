import time
import random

from bs4 import BeautifulSoup as bs
import requests

from spider import base
from log import log
from model.category import Category
from model.novel import Novel
from model.author import Author
from dao.write import write_model

spider_log = log.Log()

class Spider():
    def __init__(self, url):
        self.url = url
        self.page = None
        self.log = spider_log
        self.session = requests.session()
        self.timeout = 3
        self.history_url = []
        
    def wait_seconds(self):
        time.sleep(random.random()*2 + 1)

    def fetch_page(self,url=""):
        if url:
            self.url = url
        header = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        }
        response = self.session.get(self.url, headers = header)
        status_code = response.status_code
        if status_code == 200:
            self.page = bs(response.content)
        else:
            self.log.debug("Failed to visit the page %s, error_code : %s"%(self.url,status_code))
        return self.page

    def parse_page(self):
        raise NotImplementedError

    def process_data(self):
        raise NotImplementedError

    def run(self):
        self.fetch_page()
        self.parse_page()
        self.wait_seconds()

class BiqugeSiteSpider(Spider):
    def __init__(self):
        super().__init__("https://www.biquge.com.cn")
        self.category_list = []

    def parse_page(self):
        self.get_category_list()
        self.process_data()
        self.parse_category_page()

    def get_category_list(self):
        body = self.page
        for li_label in body.find("div",class_ = "nav").find_all("li"):
            href = li_label.find("a")['href']
            text = li_label.find("a").text
            category_url = self.join_url(href)
            category = Category(site = self.url,
                                text = text,
                                url = category_url,
                                short_url = href)
            self.category_list.append(category)
        return self.category_list
    
    def join_url(self,url):
        if url.startswith("/"):
            return "https://www.biquge.com.cn" + url
        else:
            return "https://www.biquge.com.cn/" + url

    def process_data(self):
        for category in self.category_list:
            write_model(category)

    def parse_category_page(self):
        for category in self.category_list:
            category_spider = CategorySpider(category)
            category_spider.run()
    

class CategorySpider(Spider):
    def __init__(self, category):
        self.category = category
        self.id = category.id
        self.url = category.url

    def parse_page(self):
        main_div = self.page.find(id = "main")
        hotcontent = main_div.find(id = "ll")
        newscontent = main_div.find(id = "newscontent")
        if hotcontent:
            pass
        if newscontent:
            pass

    def process_data(self):
        pass

            
class NovelSpider(Spider):
    def __init__(self, novel_url, category):
        super().__init__(novel_url)
        self.category = category
        self.novel = Novel()
        self.author = Author()
        self.chapter_list_iter = None
        
    def parse_novel_data(self):
        info = self.page.find(id="info")
        p_labels = info.find_all("p")
        self.novel.name = info.find("h1").text
        self.author.name = p_labels[0].text.split("：")[1]
        self.novel.state = p_labels[1].text.split("：")[1].split(",")[0]
        self.novel.last_update_date = p_labels[2].text.split("：")[1]
        self.novel.last_update_chapter = p_labels[3].find("a").text
        self.novel.description = self.page.find(id="intro").find("p").text.replace("<br>","\n")
        self.novel.image_path = self.page.find(id="fmimg").find("img")['src']
        self.novel.download_from = self.url
        self.novel.last_download_chapter = 0
        
    def parse_chapter_list(self):
        self.novel
        
    def parse_page(self):
        if self.page is not None:
            self.parse_novel_data()
            
    def run(self):
        self.fetch_page()
        self.parse_page()
    
if __name__ == "__main__":
    novel_spider = NovelSpider("https://www.biquge.com.cn/book/32883/","玄幻")
    novel_spider.run()