from dao.write import *

def test_update_category():
    category = Category()
    category.id = 1
    category.site = "update"
    category.text = "玄幻"
    category.url = "www.liguo.com/xuanhuan"
    update_category(category)
    
def test_update_novel():
    novel = Novel()
    novel.id = 1
    novel.name = "update-test"
    novel.author_id = 1290
    novel.chapters_count = 328
    novel.category_id = 32
    novel.image_path = "http://lfd.com/img"
    novel.description = ''' jldfjslfjsklafjlas'''
    novel.last_update_date = '2019-09-18'
    novel.last_update_chapter = "897"
    novel.download_from = "biquge"
    novel.state = "连载中"
    update_novel(novel)

def test_update_author():
    author = Author()
    author.name = 'liguo'
    author.description = '靓仔'
    insert_author(author)
    author.id = 1
    author.name = "update"
    update_author(author)
    
def test_update_chapter():
    chapter = Chapter()
    chapter.name = 'jiuren'
    chapter.novel_id = 1
    chapter.serial = 783
    chapter.text_id = 7832
    chapter.word_count = 999
    insert_chapter(chapter)

def test_update_text():
    text = Text()
    text.text = '''很久很久以前16273298732！￥#%￥@！……%@！#……！&（！&@!@^&#@^#%^$*&@$()*{}:"<>?<>MLKJBNMCJHGDSGFDJ+_[],./?: '''
    insert_text(text)


if __name__ == "__main__":
    test_update_author()
    test_update_chapter()
    test_update_text()
    print("finish!")