import logging
import time
import datetime

class ExqUtils(object):
    INFO=logging.INFO
    WARN=logging.WARN
    ERROR=logging.ERROR
    DEBUG=logging.DEBUG
    def __init__(self):
        pass
    
    @staticmethod
    def loadFileAsIter(path):
        with open(path,"r+") as f:
            for i in f:
                yield i
    
    @staticmethod
    def zprint(message):
        new_m = "|{}| {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),message)
        print(new_m)
    
    @staticmethod
    def get_logger(log_file):
        logger = logging.Logger("logger to {}".format(log_file))
        hdlr = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(levelname)s %(lineno)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr) 
        return logger
    
    @staticmethod
    def log2file(message,logger,level=logging.INFO,verbose=False):
        new_m = "|{}| {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),message)
        logger.log(level,new_m)
        if verbose: print(new_m)
        
