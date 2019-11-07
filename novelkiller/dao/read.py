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
        return get_category_id(model)
    if isinstance(model, Author):
        return get_author_id(model)
    if isinstance(model, Novel):
        return get_novel_id(model)
    if isinstance(model, Chapter):
        return get_chapter_id(model)
    if isinstance(model, Text):
        return get_text_id(model)
    raise TypeError("未知的类型")
        
def get_category_id(category):
    query = '''
        select id from category_t
        where text = '%s'
        and site = '%s'
    '''%(category.text, category.site)
    rows = global_session.query(query)
    return str(rows[0].id)

def get_author_id(author):
    query = '''
        select id from author
        where name = '%s'
    '''%(author.name)
    rows = global_session.query(query)
    return str(rows[0].id)

def get_novel_id(novel):
    query = '''
        select id from novel
        where name = '%s'
        and author_id = '%s'
    '''%(novel.name, novel.author_id)
    rows = global_session.query(query)
    return str(rows[0].id)

def get_chapter_id(chapter):
    query = '''
        select id from chapter
        where novel_id = '%s'
        and serial = '%s'
    '''%(chapter.novel_id, chapter.serial)
    rows = global_session.query(query)
    return str(rows[0].id)

def get_text_id(text):
    pass