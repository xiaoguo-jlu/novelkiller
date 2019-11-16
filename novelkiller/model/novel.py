# 小说类
from model.category import Category
from model.chapter import Chapter

class Novel():
    def __init__(self):
        self.id = ""
        self.name = "无名"
        self.author_id = "-1"
        self.chapters_count = -1
        self.category_id = "-1"
        self.image_path = "-1"
        self.description = "-1"
        self.last_update_date = ""
        self.last_update_chapter = -1
        self.download_from = "-1"
        self.download_date = ""
        self.last_download_chapter = -1
        self.finished = 'N'
        self.state = "-1" #状态字段，0代表完结，1代表连载中

    def attach_chapter(self, chapter):
        chapter.novel_id = self.id

    def attach_category(self, category):
        self.category_id = category.id

    def attach(self, model):
        if isinstance(model, Category):
            self.attach_category(model)
        elif isinstance(model, Chapter):
            self.attach_chapter(model)
        else:
            raise TypeError("Novel can't attach %s"%(type(model)))
