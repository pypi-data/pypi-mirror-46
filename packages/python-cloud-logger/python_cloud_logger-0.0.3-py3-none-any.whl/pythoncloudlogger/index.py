import logging
import os, threading

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

class RedactingFilter(logging.Filter):

    def __init__(self, patterns,keys={}):
        super(RedactingFilter, self).__init__()
        self._patterns = patterns
        self._keys=keys

    def filter(self, record):
        record.msg = self.redact(record.msg)
        if isinstance(record.args, dict):
            for k in record.args.keys():
                record.args[k] = self.redact(record.args[k])
        else:
            record.args = tuple(self.redact(arg) for arg in record.args)
        return True

    def redact(self, msg):

        if isinstance(msg,dict):
            for k in msg:
                if isinstance(msg.get(k),dict):
                    msg.update({
                        k : self.redact(msg.get(k))
                    })
                if k.lower() in self._keys:
                    msg.update({
                            k:"<<TOP SECRET!>>"
                    })
            
        else:
            msg = isinstance(msg, str) and msg or str(msg)
            for pattern in self._patterns:
                msg = msg.replace(pattern, "<<TOP SECRET!>>")
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
