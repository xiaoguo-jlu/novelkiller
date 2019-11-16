import sys
import os
from urllib.parse import urljoin

from parsers.base import ResultSet, ParseException, Parser
from model.author import Author
from model.novel import Novel
from dao.read import get_id, check_novel_download_finished
from dao.write import write_model

class NovelParser(Parser):
    def __init__(self, page):
        super().__init__(page)

    def parse(self):
        result_set = ResultSet()
        author = self.__parse_author()
        result_set.data['author'] = author
        novel = self.__parse_novel()
        result_set.data['novel'] = novel
        chapter_url_list = self.__parse_chapter_url_list()
        result_set.url_quene = chapter_url_list
        return result_set

    def __parse_author(self):
        author = Author()
        info = self.page.find(id="info")
        if info:
            p_labels = info.find_all("p")
            author.name = p_labels[0].text.split("：")[1]
        else:
            raise ParseException("Failed to parse novel page")
        return author

    def __parse_novel(self):
        novel = Novel()
        info = self.page.find(id="info")
        if info:
            p_labels = info.find_all("p")
            novel.name = info.find("h1").text
            novel.state = p_labels[1].text.split("：")[1].split(",")[0]
            novel.last_update_date = p_labels[2].text.split("：")[1]
            # novel.last_update_chapter = p_labels[3].find("a").text
            novel.description = self.page.find(id="intro").find("p").text.replace("<br>","\n")
            novel.image_path = self.page.find(id="fmimg").find("img")['src']
        else:
            raise ParseException("Failed to parse novel page")
        return novel

    def __parse_chapter_url_list(self):
        chapter_url_list = []
        root_url = "https://www.biquge.com.cn/"
        for chapter_item in self.page.find("div", id = "list").find_all("dd"):
            href = chapter_item.find("a")["href"]
            url = urljoin(root_url, href)
            chapter_url_list.append(url)
        return chapter_url_list

def test():
    from bs4 import BeautifulSoup as bs
    import requests
    test_url = "https://www.biquge.com.cn/book/40888/"
    page = bs(requests.get(test_url).content)
    parser = NovelParser(page)
    result_set = parser.parse()
    print(result_set.data)
    print(result_set.url_quene)
    

if __name__ == "__main__":
    test()