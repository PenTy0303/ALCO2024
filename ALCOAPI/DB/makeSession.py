# 標準モジュール系
from sqlalchemy.orm import sessionmaker

# 自作モジュール
from logging import getLogger

class MakeSession():
    
    # セッションを作成する
    def __init__(self, CE):
        
        # ベタ打ちにはしたくない
        self.Session = sessionmaker(autocommit=False, autoflush=False, bind=CE.getEngine())
        
        # loggerの管理
        self.logger = getLogger("MainLog").getChild("Session")
    
    # getter
    def getSession(self):
        session = self.Session()
        return session
            
        