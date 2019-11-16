from parsers.base import ResultSet, ParseException, Parser

class CategoryParser(Parser):
    def __init__(self, page):
        super().__init__(page) 

    def parse(self):
        result = ResultSet()
        main_div = self.page.find("div", id = "main")
        if not main_div:
            raise ParseException("failed to parse category page")
        hotcontent = main_div.find("div", id = "hotcontent")
        newscontent = main_div.find("div", id = "newscontent")
        if hotcontent:
            ll_content = hotcontent.find("div", class_ = "ll")
            if ll_content:
                novel_items = ll_content.find_all("div", class_ = "item")
                if novel_items:
                    for item in novel_items:
                        result.url_quene.append(item.find("dt").find("a")["href"])
        if newscontent:
            l_content = newscontent.find("div", class_ = "l")
            if l_content:
                for item_left in l_content.find_all("li"):
                    novel_url = item_left.find("span", class_ = "s2").find("a")["href"]
                    result.url_quene.append(novel_url)
            r_content = newscontent.find("div", class_ = "r")
            if r_content:
                for item_right in r_content.find_all("li"):
                    novel_url = item_right.find("span", class_ = "s2").find("a")["href"]
                    result.url_quene.append(novel_url)
        return result

def test():
    from bs4 import BeautifulSoup as bs
    import requests
    test_url = "https://www.biquge.com.cn"
    page = bs(requests.get(test_url).content)
    parser = CategoryParser(page)
    result_set = parser.parse()
    print(result_set.data)
    print(result_set.url_quene)
    
if __name__ == "__main__":
    test()