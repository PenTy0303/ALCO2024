from sqlalchemy import create_engine
import os

# sqlalchemy.create_engineを使ってデータベース作成用接続用のエンジンを返却するクラス．
class CreateEngine():
    
    # コンストラクタ
    def __init__(self):
        # dialect, userName, passWord, host, database = "mysql", "alco", "alco2024", "localhost", "alcodb"
        # self._engine = create_engine(f"{dialect}://{userName}:{passWord}@{host}/{database}", echo=True)
        dialect, fn = "sqlite", "ALCOAPI/" + "v2_0_0" + "/DB/alcodb.sqlite"
        self._engine = create_engine(f"{dialect}:///{fn}")
    
    # getter
    def getEngine(self):
        return self._engine