from logging import getLogger, StreamHandler, Formatter, ERROR
from logging.handlers import TimedRotatingFileHandler

# Loggerインスタンスの生成
def SetLogger():
    logger = getLogger("MainLog")
    logger.setLevel(ERROR)
    
    handler_formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    
    streamHandler = StreamHandler()
    streamHandler.setLevel(ERROR)
    streamHandler.setFormatter(handler_formatter)
    
    fileHandler = TimedRotatingFileHandler("ALCOAPI/log/ALCOAPI.log", when="midnight", interval=1, backupCount=7)
    fileHandler.setLevel(ERROR)
    fileHandler.setFormatter(handler_formatter)
    
    logger.addHandler(streamHandler)
    logger.addHandler(fileHandler)
    
    logger.debug("create any handlers sucseeded!")