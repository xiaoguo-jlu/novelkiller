from .config import config
from datetime import datetime
import atexit

logContainer = []

class Log():
    def __init__(self, name = ""):
        self.name = name
        self.infoFlag = config["info"]
        self.warningFlag = config["warning"]
        self.debugFlag = config["debug"]
        self.errorFlag = config["error"]
        self.outputToFileFlag = config["outputToFile"]
        self.fileBufferSize = config["fileBuffer"]
        self.fileBuffer = ""
        self.filename = ""
        self.bufferIsFull = lambda : len(self.fileBuffer) >= self.fileBufferSize
        self.__createLogFile()
        logContainer.append(self)
            
    def __getTimeStamp(self):
        currentTime = datetime.now()
        timestamp = "%s-%s-%s %s:%s:%s "%(
            currentTime.year,
            currentTime.month,
            currentTime.day,
            currentTime.hour,
            currentTime.minute,
            currentTime.second)
        return timestamp
            
    def __printMessage(self, message):
        timestamp = self.__getTimeStamp()
        print(timestamp + message)
        if self.outputToFileFlag:
            self.__writeLogFile(timestamp + message)
    
    def __createLogFile(self):
        currentTime = datetime.now()
        self.filename = "%s-%s-%s.log"%(
            currentTime.year,
            currentTime.month,
            currentTime.day)
        with open(self.filename,"a+") as f:
            f.write("This log file is created by system.\n")
        
    def __writeLogFile(self,message):
        if not self.outputToFileFlag:
            return
        if isinstance(message, (str,)):
            if self.bufferIsFull():
                with open(self.filename, "w+") as f:
                    f.write(self.fileBuffer)
            else:
                self.fileBuffer += self.__getTimeStamp() + message + "\n"
        else:
            self.error("Trying to writing a unknown record ...")
    
    def info(self, message):
        message = "info: " + message
        if self.infoFlag:
            self.__printMessage(message)
    
    def warning(self, message):
        message = "warning: " + message
        if self.warningFlag:
            self.__printMessage(message)
    
    def debug(self, message):
        message = "debug: " + message
        if self.debugFlag:
            self.__printMessage(message)
    
    def error(self, message):
        message = "error: " + message
        if self.errorFlag:
            self.__printMessage(message)
        
    def write(self):
        archive(self)
            
@atexit.register
def archive():
    for logInstance in logContainer:
        print("wait a minute, writing log to file ...")
        if logInstance.outputToFileFlag:
            with open(logInstance.filename, "a+") as f:
                f.write(logInstance.fileBuffer)
        print("done!")