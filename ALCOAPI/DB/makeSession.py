# 標準モジュール系
from sqlalchemy.orm import sessionmaker

# 自作モジュール
from CreateEngine import CreateEngine

class MakeSession():
    
    # セッションを作成する
    def __init__(self):
        
        # ベタ打ちにはしたくない
        CE = CreateEngine()
        SessionClass = sessionmaker(CE.getEngine())
        self._session = SessionClass()
    
    # getter
    def getSession(self):
        return self._session