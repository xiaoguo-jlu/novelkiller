# 爬虫基类，依赖于requests库

import requests

class AbstractSpider():
    def __init__(self,startUrl = []):
        self.startUrl = startUrl
        self.currentUrl = ""
        self.targetQueue = []
        self.historyQueue = []
        self.header = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
            }
        self.responseBody = ""
        self.startFlag = False
        self.runFlag = False
        self.log = None
        
    def attachLog(self,log):
        self.log = log
        
    def __sendRequest(self,url):
        response = requests.get(url, headers = self.header)
        self.currentUrl = url
        if response.status_code == 200:
            self.responseBody = response.content
            self.historyQueue.append(url)
            self.targetQueue.remove(url)
        else:
            self.responseBody = ""
            
    def getUrlsFromPage(self):
        raise NotImplementedError
    
    def __putUrlsIntoTargetQueue(self, urlList):
        for url in urlList:
            if url not in self.historyQueue:
                self.targetQueue.append(url)
        
    def start(self):
        self.log.debug("Spider is starting ...")
        self.startFlag = True
        self.log.debug("Spider started successfully!")
            
    def parsePage(self):
        raise NotImplementedError
    
    def saveDate(self):
        raise NotImplementedError
    
    def run(self):
        self.runFlag = True
        self.start()

    def pause(self):
        self.runFlag = False
        
    def stop(self):
        self.startFlag = False
        self.runFlag = False
        if not self.log:
            self.log.debug("spider is exiting ...")
            
if __name__ == "__main__":
    AbstractSpider(["https://www.biquge.com.cn/"]).run()