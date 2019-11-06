from dao.read import *

def test_check_is_existed():
    author = Author()
    author.id = 1
    print("------------ author test ---------------")
    print("理想结果为True，实际结果为" , check_author_is_existed(author))
    author.id = 10
    print("理想结果为False，实际结果为" , check_author_is_existed(author))
    author.id = ""
    author.name = 'liguo'
    print("理想结果为True，实际结果为" , check_author_is_existed(author))
    author.name = 'jiang'
    print("理想结果为False，实际结果为" , check_author_is_existed(author))

    print("------------ novel test ---------------")
    novel = Novel()
    novel.id = 1
    print("理想结果为True，实际结果为" , check_novel_is_existed(novel))
    novel.id = 5
    print("理想结果为False，实际结果为" , check_novel_is_existed(novel))
    novel.id = ""
    novel.name = 'kkkkk'
    novel.author_id = 2
    print("理想结果为True，实际结果为" , check_novel_is_existed(novel))
    novel.name = 'kkkkk'
    novel.author_id = 3
    print("理想结果为False，实际结果为" , check_novel_is_existed(novel))
    novel.name = '4343'
    novel.author_id = 2
    print("理想结果为False，实际结果为" , check_novel_is_existed(novel))
    novel.name = 'liguo'
    
def test_get_id():
    category = Category()
    category.text = "玄幻"
    category.site = "novel"
    assert '2' == get_id(category)
    novel = Novel()
    novel.name = 'kkkkk'
    novel.author_id = 2
    assert '3' == get_id(novel)
    author = Author()
    author.name = 'liguo'
    assert '1' == get_id(author)
    chapter = Chapter()
    chapter.serial = 783
    chapter.novel_id = 1
    assert '1' == get_id(chapter)

    
if __name__ == "__main__":
    print("test begin ")
    test_get_id()
    print("test done")