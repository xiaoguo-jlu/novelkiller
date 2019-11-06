from dao.session import MysqlSessionFactory
from model.category import Category
from model.novel import Novel
from model.author import Author
from model.chapter import Chapter
from model.text import Text

global_session = MysqlSessionFactory.get_session()

def check_novel_is_existed(novel):
    if novel.id:
        query = '''
            select count(1) as num from novel
            where id = '%s'
        '''%(novel.id)
    else:
        query = '''
            select count(1) as num from novel
            where name = '%s'
            and author_id = '%s'
        '''%(novel.name, novel.author_id)
    rows = global_session.query(query)
    return (True if rows[0].num  else False)

def check_author_is_existed(author):
    if author.id:
        query = '''
            select count(1) as num from author
            where id = '%s'
        '''%(author.id)
    else:
        query = '''
            select count(1) as num from author
            where name = '%s'
        '''%(author.name)
    rows = global_session.query(query)
    return (True if rows[0].num  else False)

def get_id(model):
    if isinstance(model, Category):
        get_category_id(model)
    if isinstance(model, Author):
        get_author_id(model)
    if isinstance(model, Novel):
        get_novel_id(model)
    if isinstance(model, Chapter):
        get_chapter_id(model)
    if isinstance(model, Text):
        get_text_id(model)
        
def get_category_id(category):
    pass

def get_author_id(author):
    pass

def get_novel_id(novel):
    pass

def get_chapter_id(chapter):
    pass

def get_text_id(text):
    pass

if __name__ == "__main__":
    query = "select * from novel"
