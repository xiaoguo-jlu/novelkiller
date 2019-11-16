from model.chapter import Chapter
from model.text import Text
from parsers.base import Parser, ResultSet, ParseException

class ChapterParser(Parser):
    def __init__(self, page):
        super().__init__(page)

    def __encode_text(self, text):
        if text.endswith("\\"):
            text = text.replace("\\"," ")
        text = text.replace("'","\\'")
        return text

    def parse(self):
        result = ResultSet()
        chapter = Chapter()
        box = self.page.find("div", class_ = "box_con")
        if not box:
            raise ParseException("Failed to parse chapter page")
        chapter.name = box.find("div", class_ = "bookname").find("h1").text
        result.data['chapter'] = chapter
        text = Text()
        chapter_text = box.find("div", id = "content").text
        text.text = self.__encode_text(chapter_text)
        result.data['text'] = text
        return result