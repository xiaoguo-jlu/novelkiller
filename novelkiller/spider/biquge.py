import time
import random

from bs4 import BeautifulSoup as bs
import requests

from spider import base
from log import log
from model.novel import Novel
from model.author import Author

spider_log = log.Log()

class Spider():
    def __init__(self, url):
        self.url = url
        self.page = None
        self.log = spider_log
        self.session = requests.session()
        self.timeout = 3
        
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

class Biquge(base.AbstractSpider):
    def __init__(self):
        super().__init__(["https://www.biquge.com.cn/"])
        self.attachLog(log.Log())

    def parsePage(self):
        self.log.debug("Getting data from %s"%self.currentUrl)
        
    def joinUrl(self,url):
        if url.startswith("/"):
            return "https://www.biquge.com.cn" + url
        else:
            return "https://www.biquge.com.cn/" + url
    
    def getCategoryUrlsFromPage(self):
        print("getting urls ...")
        body = bs(self.responseBody)
        urlList = []
        for li in body.find("div",class_ = "nav").find_all("li"):
            [urlList.append(self.joinUrl(url['href'])) for url in (li.find_all("a"))]
        return urlList
    
    def getUrlsFromPage(self):
        category = self.getCategoryUrlsFromPage()
        urlList = []
        for i in category:
            urlList.append(i)
            
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