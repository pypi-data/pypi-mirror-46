import logging
import os, threading, copy

class ThreadDataManager():
    data = {}
    def __init__(self):
        pass
    @staticmethod
    def getData():
        ident = threading.currentThread().ident
        if (ThreadDataManager.data.get(ident) == None):
            ThreadDataManager.data[ident]={}
        return ThreadDataManager.data.get(ident)

    @staticmethod
    def setData(data):
        ident = threading.currentThread().ident
        if (ThreadDataManager.data.get(ident) == None):
            ThreadDataManager.data[ident]={}
        ThreadDataManager.data[ident].update(data)
        return ThreadDataManager.data.get(ident)

    @staticmethod
    def clearData(data):
        ident = threading.currentThread().ident
        if (ThreadDataManager.data.get(ident) == None):
            ThreadDataManager.data[ident]={}
        ThreadDataManager.data[ident].clear()

_origFunc = logging.getLogger

class _MyAdapter(logging.LoggerAdapter):
    def __init__(self,logger,extra):
        super().__init__(logger,extra)
        self.logger = logger
        self.handlers = logger.handlers
        self.level = logger.level
        self.propagate = logger.propagate
        self.parent = logger.parent
    def hasHandlers(self,*args,**kargs):
        return self.logger.hasHandlers(*args,**kargs)
    def addHandler(self,*args,**kargs):
        return self.logger.addHandler(*args,**kargs)
    def addFilter(self,*args,**kargs):
        return self.logger.addFilter(*args,**kargs)
    def removeHandler(self,*args,**kargs):
        return self.logger.removeHandler(*args,**kargs)
    def removeHandler(self,*args,**kargs):
        return self.logger.removeHandler(*args,**kargs)
    def updateContext(self,context):
        ThreadDataManager.setData(context)
    def clearContext(self,context):
        ThreadDataManager.clearData()

def newFunc(*args,**kargs):
    logger =  _origFunc(*args,**kargs)
    return _MyAdapter(logger,ThreadDataManager.getData())
logging.getLogger = newFunc
