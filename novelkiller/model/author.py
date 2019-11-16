# 作者类
from model.novel import Novel

class Author():
    def __init__(self):
        self.id = ""
        self.name = "无名"
        self.description = ""

    def attach_novel(self, novel):
        if isinstance(novel, Novel):
            novel.author_id = self.id
        else:
            raise TypeError("Author can't attach %s"%(type(novel)))