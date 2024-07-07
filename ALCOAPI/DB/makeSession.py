# 標準モジュール系
from sqlalchemy.orm import sessionmaker

# 自作モジュール
from ALCOAPI.DB.CreateEngine import CreateEngine
from logging import getLogger

class MakeSession():
    
    # セッションを作成する
    def __init__(self):
        
        # ベタ打ちにはしたくない
        CE = CreateEngine()
        self._SessionClass = sessionmaker(autocommig=False, autoflush=False, bind=CE.getEngine())
        
        # loggerの管理
        self.logger = getLogger("MainLog").getChild("Session")
    
    # getter
    def getSession(self):
        session = self._SessionClass()
        try:
            yield session
        except Exception as e:
            self.logger.error("セッション関連でエラーが発生したのでロールバックして当該セッションをクローズします : {e}")
            session.rollback()
            raise
        finally:
            session.close()
            
        