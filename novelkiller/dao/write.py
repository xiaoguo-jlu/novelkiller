from dao.session import MysqlSessionFactory
from model.category import Category
from model.novel import Novel
from model.author import Author
from model.chapter import Chapter
from model.text import Text

global_session = MysqlSessionFactory.get_session()

def write_category(category):
    if not isinstance(category, Category):
        raise TypeError("Cannot write %s into database!"%type(category))
    if not category.id:
        insert_category(category)
    else:
        update_category(category)
    
def insert_category(category):
    query = '''
    insert into category_t
    (
        site,
        text,
        url
    )
    values
    ('%s','%s','%s')
    '''%(
            category.site,
            category.text,
            category.url
        )
    global_session.query(query)
    
def update_category(category):
    query = '''
    update category_t 
    set
        site = '%s',
        url = '%s',
        text = '%s'
    where id = '%s'
    '''%(
            category.site,
            category.url,
            category.text,
            category.id
        )
    global_session.query(query)
    
def write_novel(novel):
    if not isinstance(novel, Novel):
        raise TypeError("Cannot write %s into database!"%type(novel))
    if not novel.id:
        insert_novel(novel)
    else:
        update_novel(novel)
    
def insert_novel(novel):
    query = '''
    insert into novel
    (
        name,
        author_id,
        chapters_count,
        category_id,
        image_path,
        description,
        last_update_date,
        last_update_chapter,
        download_from,
        download_date,
        state
    )
    values
    (
        '%s','%s','%s','%s','%s',
        '%s',NOW(),'%s','%s',NOW(),'%s'
    )
    '''%(
            novel.name,
            novel.author_id,
            novel.chapters_count,
            novel.category_id,
            novel.image_path,
            novel.description,
            novel.last_update_chapter,
            novel.download_from,
            novel.state
        )
    global_session.query(query)
    
def update_novel(novel):
    query = '''
    update novel 
    set
        name = '%s',
        author_id = '%s',
        category_id = '%s',
        image_path = '%s',
        description = '%s',
        last_update_date = NOW(),
        last_update_chapter = '%s',
        download_from = '%s',
        download_date = NOW(),
        last_download_chapter = '%s',
        state = '%s'
    where id = '%s'
    '''%(
            novel.name,
            novel.author_id,
            novel.category_id,
            novel.image_path,
            novel.description,
            novel.last_update_chapter,
            novel.download_from,
            novel.last_update_chapter,
            novel.state,
            novel.id
        )
    global_session.query(query)
    
def update_novel_chapter(novel):
    query = '''
    update novel 
    set
        last_update_date = NOW(),
        last_update_chapter = '%s',
        last_download_chapter = '%s',
        state = '%s'
    where id = '%s'
    '''%(
            novel.last_update_chapter,
            novel.download_from,
            novel.last_update_chapter,
            novel.state,
            novel.id
        )
    global_session.query(query)
    
def write_author(author):
    if not isinstance(author, Author):
        raise TypeError("Cannot write %s into database!"%type(author))
    if not author.id:
        insert_author(author)
    else:
        update_author(author)
        
def insert_author(author):
    query = '''
    insert into author
    (
        name,
        description
    )
    values
    ('%s','%s')
    '''%(
            author.name,
            author.description
        )
    global_session.query(query)

def update_author(author):
    pass

def write_chapter(chapter):
    if not isinstance(chapter, Chapter):
        raise TypeError("Cannot write %s into database!"%type(chapter))
    if not chapter.id:
        insert_chapter(chapter)
    else:
        update_chapter(chapter)
        
def insert_chapter(chapter):
    query = '''
    insert into chapter
    (
        name,
        novel_id,
        text_id,
        serial,
        download_date,
        word_count
    )
    values
    ('%s','%s','%s',
     '%s',now(),'%s')
    '''%(
            chapter.name,
            chapter.novel_id,
            chapter.text_id,
            chapter.serial,
            chapter.word_count
        )
    global_session.query(query)

def update_chapter(chapter):
    pass

def write_text(text):
    if not isinstance(text, Text):
        raise TypeError("Cannot write %s into database!"%type(text))
    if not text.id:
        insert_text(text)
    else:
        update_text(text)
        
def insert_text(text):
    query = '''
    insert into chapter_text
    (
        chapter_id,
        text
    )
    values
    ('%s','%s')
    '''%(
            text.text,
            text.chapter_id
        )
    global_session.query(query)

def update_text(text):
    pass

