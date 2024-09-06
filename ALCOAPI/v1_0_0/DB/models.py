# sqlalchemyにおけるテーブルのベースクラス
from sqlalchemy.orm import declarative_base, relationship

# 制約
from sqlalchemy import ForeignKey

# テーブルの各カラムに対するデータ型
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Float, BigInteger, DateTime

# グローバルメソッド

# 自作メソッド


Base = declarative_base()

# USER テーブル作成
class USER(Base):
    
    # metadata
    __tablename__ = "USER"
    
    # columns
    userID = Column(String(8), primary_key=True, nullable=False, autoincrement=False, unique=True)
    auth = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    salt = Column(String(255), nullable=False)
    userDataID = Column(String(8), nullable=False, unique=True)
    
    # USERDataテーブルとのリレーション
    userData = relationship("USERData")
    userSession = relationship("USERSession")
    
    # CRUDMethods


# USERDataテーブル作成
class USERData(Base):
    
    # metadata
    __tablename__ = "USERData"
    
    # columns
    userDataID = Column(String(8), ForeignKey("USER.userDataID", ondelete="CASCADE", onupdate="CASCADE") , primary_key=True, nullable=False, autoincrement=False)
    totalSteps = Column(BigInteger)
    todaySteps = Column(BigInteger)
    ltdReliefDate = Column(Float)
    lastInterfereDate = Column(Float)
    totalReliefTimes = Column(Integer)
    currentSeasonReliefTimes = Column(Integer)
    lastReliefTimesUpdate = Column(Float)
    property = Column(Integer)
    destructionRate = Column(Integer)
    civilizationRate = Column(Integer)
    currentDebuff = Column(Integer)
    ownedItems = Column(String(2^16))
    unlockedAchievement = Column(String(2*16))
    lastUpdate = Column(Float)
    
    # CURDMethods       

# USERSessionテーブル作成
class USERSession(Base):
    
    # metadata
    __tablename__  = "USERSession"
    
    # columns
    sessionID = Column(String(8), primary_key=True, nullable=False, autoincrement=False)
    userID = Column(String(8), ForeignKey("USER.userID", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    expiredDate = Column(DateTime, nullable=False)
    state = Column(String(255), nullable=False)
    
    # CRUDMethods

# CLIENTHistoryテーブル作成
class CLIENTHistory(Base):
    
    # metadata
    __tablename__ = "CLIENTHistory"
    
    # columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False)
    type = Column(String(255), nullable=False)
    method = Column(String(255), nullable=False)
    payload = Column(String(1024), nullable=False)
    
    # CRUDMethods



if(__name__ == "__main__"):
    from sqlalchemy import create_engine
    dialect, fn = "sqlite", "ALCOAPI/" + "v1_0_0" + "/DB/alcodb.db"
    CE = create_engine(f"{dialect}:///{fn}")
    Base.metadata.create_all(CE)