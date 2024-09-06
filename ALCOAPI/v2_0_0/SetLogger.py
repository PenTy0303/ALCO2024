from logging import getLogger, StreamHandler, Formatter, DEBUG
from logging.handlers import TimedRotatingFileHandler
import datetime
# Loggerインスタンスの生成
def SetLogger():
    logger = getLogger("MainLog")
    logger.setLevel(DEBUG)
    
    handler_formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    
    streamHandler = StreamHandler()
    streamHandler.setLevel(DEBUG)
    streamHandler.setFormatter(handler_formatter)
    
    fn = str(datetime.datetime.now()).split(' ')[0] # + "-" +  str(datetime.datetime.now()).split(' ')[1].replace(".", "-").replace(":", "-")
    
    fileHandler = TimedRotatingFileHandler(f"ALCOAPI/log/{str(fn)}.log", when="midnight", interval=1, backupCount=7)
    fileHandler.setLevel(DEBUG)
    fileHandler.setFormatter(handler_formatter)
    
    logger.addHandler(streamHandler)
    logger.addHandler(fileHandler)
    
    logger.debug("create any handlers sucseeded!")