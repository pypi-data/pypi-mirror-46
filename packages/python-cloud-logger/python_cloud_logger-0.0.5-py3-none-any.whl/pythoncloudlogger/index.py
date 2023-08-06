import logging
import os, threading, copy

from pythonjsonlogger import jsonlogger

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


class RedactJsonFormatter(jsonlogger.JsonFormatter):
    def __init__(self,*args,**kargs):
        self.redactionKeyString = kargs.pop("redactionKeys",os.environ.get("redactionKeys",""))
        self.redactionString = kargs.pop("redactionString",os.environ.get("redactionString","<Secret>"))
        self.skipRedactForDebug = kargs.pop("skipRedactForDebug",os.environ.get("skipRedactForDebug","False"))
        jsonlogger.JsonFormatter.__init__(self,*args,**kargs)
        self.redactionKeys = self.redactionKeyString.split(",")

    def format(self,record):
        message_dict = {}
        if isinstance(record.msg, dict):
            message_dict = copy.deepcopy(record.msg)
            if self.skipRedactForDebug != "True":
                message_dict = self.redact(message_dict)
                record.msg = message_dict
        return jsonlogger.JsonFormatter.format(self,record)
    def redact(self,msg):
        for k in msg:
            if isinstance(msg.get(k),dict):
                msg.update({
                    k : self.redact(msg.get(k))
                })
            else:
                if k.lower() in self.redactionKeys:
                    msg.update({
                        k : self.redactionString
                    })
        return msg


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
