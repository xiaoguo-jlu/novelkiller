# 小说类

class Novel():
    def __init__(self):
        self.id = ""
        self.name = ""
        self.author_id = ""
        self.chapters_count = 0
        self.category_id = ""
        self.image_path = ""
        self.description = ""
        self.last_update_date = ""
        self.last_update_chapter = 0
        self.download_from = ""
        self.download_date = ""
        self.last_download_chapter = 0
        self.finished = 'N'
        self.state = "" #状态字段，0代表完结，1代表连载中