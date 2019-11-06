from log import log

class Tree():
    def __init__(self,name,data = "",logger = None):
        self.name = name
        self.data = data
        self.children = []
        if logger is None:
            logger = log.Log()
        self.logger = logger
        
    def addChild(self,node):
        self.children.append(node)
        
    def removeChild(self, node):
        self.children.remove(node)
    
    def setData(self, data):
        self.data = data

class SiteTree(Tree):
    def __init__(self, name, siteUrl):
        super().__init__(name,siteUrl)
        

class CategoryTree(Tree):
    def __init__(self, name,data = ""):
        super().__init__(name,data)
        

class NovelTree(Tree):
    def __init__(self, name,data = ""):
        super().__init__(name,data)
        

class Chapter(Tree):
    def __init__(self, name):
        self.name = name
        super().__init__(name)