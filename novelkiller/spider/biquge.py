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
from dao.read import get_id

spider_log = log.Log()

class Spider():
    def __init__(self, url):
        self.url = url
        self.page = None
        self.log = spider_log
        self.session = requests.session()
        self.timeout = 3
        self.history_url = []
        self.url_quene = []
        self.data = []
        
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
        self.history_url.append(url)
        if status_code == 200:
            self.page = bs(response.content)
        else:
            self.log.debug("Failed to visit the page %s, error_code : %s"%(self.url,status_code))
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
        self.fetch_next()

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
        self.url_quene = []

    def parse_page(self):
        main_div = self.page.find("div", id = "main")
        hotcontent = main_div.find("div", id = "ll")
        newscontent = main_div.find("div", id = "newscontent")
        if hotcontent:
            for item in hotcontent.find("div", class_ = "ll").find_all("div", class_ = "item"):
                self.url_quene.append(item.find("dt").find("a")["href"])
        if newscontent:
            for item_left in newscontent.find("div", class_ = "l").find_all("li"):
                novel_url = item_left.find("span", class_ = "s3").find("a")["href"]
                self.url_quene.append(novel_url)
            for item_right in newscontent.find("div", class_ = "r").find_all("li"):
                novel_url = item_right.find("span", class_ = "s2").find("a")["href"]
                self.url_quene.append(novel_url)

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
        self.author.name = p_labels[0].text.split("：")[1]
        try:
            get_id(self.author)
        except IndexError:
            write_model(self.author)
        author_id = get_id(self.author)
        self.novel.author_id = author_id
        self.novel.name = info.find("h1").text
        self.novel.state = p_labels[1].text.split("：")[1].split(",")[0]
        self.novel.last_update_date = p_labels[2].text.split("：")[1]
        self.novel.last_update_chapter = p_labels[3].find("a").text
        self.novel.description = self.page.find(id="intro").find("p").text.replace("<br>","\n")
        self.novel.image_path = self.page.find(id="fmimg").find("img")['src']
        self.novel.download_from = self.url
        self.novel.last_download_chapter = 0
        write_model(self.novel)
        
    def parse_chapter_list(self):
        for chapter_item in self.page.find("div", class_ = "box_con").find("div", class_ = "list").find_all("dd"):
            href = chapter_item.find("a")["href"]
            self.history_url.append(href)
        
    def parse_page(self):
        if self.page is not None:
            self.parse_novel_data()

    def process_data(self):
        pass
            
    
if __name__ == "__main__":
    novel_spider = NovelSpider("https://www.biquge.com.cn/book/32883/","玄幻")
    novel_spider.run()