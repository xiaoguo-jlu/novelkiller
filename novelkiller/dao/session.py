import records

class MysqlConfig():
    def __init__(self):
        username = "spider"
        password = "12345678"
        host = "localhost"
        instance = "novel"
        self.description = "mysql://%s:%s@%s/%s"%(
            username,password,host,instance)
        self.connect_args = {"charset":"utf8"}
        
class SessionFactory():
    def __init__(self):
        pass
        
class MysqlSessionFactory(SessionFactory):
    config = MysqlConfig()
    free_session_pool = []
    busy_session_pool = []
    def __init__(self):
        pass
        
    @classmethod
    def create_session(cls):
        session = records.Database(cls.config.description, connect_args=cls.config.connect_args)
        cls.free_session_pool.append(session)
        return session
    
    @classmethod
    def get_session(cls):
        if not cls.free_session_pool:
            cls.create_session()
        session = cls.free_session_pool.pop()
        cls.busy_session_pool.append(session)
        return session
    
if __name__ == "__main__":
    session1 = MysqlSessionFactory.get_session()
    a = session1.query("select * from category_t")
    session2 = MysqlSessionFactory.get_session()
    session3 = MysqlSessionFactory.get_session()
    session4 = MysqlSessionFactory.get_session()
    session5 = MysqlSessionFactory.get_session()
