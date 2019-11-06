import requests
from spider import website
from bs4 import BeautifulSoup as bs
from random import random
import time

site_tree = website.SiteTree("笔趣阁","https://www.biquge.com.cn/")

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}
req = requests.get("https://www.biquge.com.cn/",headers = headers)

def get_category_urls_from_page(page):
    print("getting urls ...")
    body = bs(page)
    for li in body.find("div",class_ = "nav").find_all("li"):
        name = li.find("a").text
        url = joinUrl(li.find("a")['href'])
        site_tree.addChild(website.CategoryTree(name,url))

def joinUrl(url):
    if url.startswith("/"):
        return "https://www.biquge.com.cn" + url
    else:
        return "https://www.biquge.com.cn/" + url
    
def fetch_novel(callback = lambda x : x):
    for category_node in site_tree.children:
        category_page = requests.get(category_node.data).content
        novel_list = category_page.find

get_category_urls_from_page(req.content)
categoryPages = []