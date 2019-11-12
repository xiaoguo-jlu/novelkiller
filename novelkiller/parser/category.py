from parser.base import Parser, ResultSet, ParseException

class CategoryParser(Parser):
    def __init__(self, page):
        super().__init__(page) 

    def parse(self):
        result = ResultSet()
        main_div = self.page.find("div", id = "main")
        if not main_div:
            raise ParseException("解析失败")
        hotcontent = main_div.find("div", id = "hotcontent")
        newscontent = main_div.find("div", id = "newscontent")
        if hotcontent:
            novel_items = hotcontent.find("div", class_ = "ll").find_all("div", class_ = "item")
            if novel_items:
                for item in novel_items:
                    result.url_quene.append(item.find("dt").find("a")["href"])
        if newscontent:
            for item_left in newscontent.find("div", class_ = "l").find_all("li"):
                novel_url = item_left.find("span", class_ = "s3").find("a")["href"]
                result.url_quene.append(novel_url)
            for item_right in newscontent.find("div", class_ = "r").find_all("li"):
                novel_url = item_right.find("span", class_ = "s2").find("a")["href"]
                result.url_quene.append(novel_url)
        return result