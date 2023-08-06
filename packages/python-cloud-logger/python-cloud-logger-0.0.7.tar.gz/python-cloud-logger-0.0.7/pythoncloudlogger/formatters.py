import logging
import os, threading, copy

from pythonjsonlogger import jsonlogger

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
